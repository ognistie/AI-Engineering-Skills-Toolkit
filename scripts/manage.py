"""Manage local AAES skill copies without network access."""
import argparse
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
from uuid import uuid4
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "skills/skill-orchestrator/references/catalog.json"
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")


def catalog():
    return json.loads(CATALOG.read_text(encoding="utf-8"))["skills"]


def safe_path(path):
    for part in (path, *path.parents):
        if part.is_symlink() or part.is_junction():
            raise ValueError(f"Linked path is not supported: {part}")
    return path


def tree_files(folder, source=False):
    safe_path(folder)
    if not folder.is_dir():
        raise ValueError(f"Missing skill folder: {folder}")
    result = {}
    for directory, dirs, files in os.walk(folder, followlinks=False):
        base = Path(directory)
        for name in dirs + files:
            safe_path(base / name)
        if source:
            dirs[:] = [name for name in dirs if name != "__pycache__"]
        for name in files:
            path = base / name
            if not path.is_file():
                raise ValueError(f"Not a regular file: {path}")
            result[path.relative_to(folder).as_posix()] = path
    if "SKILL.md" not in result:
        raise ValueError(f"No SKILL.md in {folder}")
    return dict(sorted(result.items()))


def fingerprint(files):
    return {name: hashlib.sha256(path.read_bytes()).hexdigest() for name, path in files.items()}


def write_manifest(path, data):
    temporary = path.with_name(uuid4().hex + ".json")
    try:
        temporary.write_text(json.dumps(data, sort_keys=True) + "\n", encoding="utf-8")
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def live_path(path):
    return path.exists() or path.is_symlink() or path.is_junction()


@contextmanager
def lock(state):
    marker = state / "lock"
    marker.mkdir()
    try:
        yield
    finally:
        marker.rmdir()


def default_path(target):
    home = Path.home()
    if target == "codex":
        return home / ".agents" / "skills"
    if target == "claude":
        return Path(os.environ.get("CLAUDE_CONFIG_DIR") or home / ".claude") / "skills"
    raise ValueError("Use --destination with generic")


def operate(command, dest, names, sources):
    dest = safe_path(Path(os.path.abspath(dest)))
    if dest == dest.parent:
        raise ValueError("Cannot target a filesystem root")
    state = safe_path(dest.parent / f".{dest.name}.aaes-state")
    records = safe_path(state / "records")
    backup_root = safe_path(state / "backups")
    sources = {name: tree_files(sources / name, source=True) for name in names if command != "remove"}
    if command == "verify":
        for name in names:
            receipt = safe_path(records / (name + ".json"))
            installed = fingerprint(tree_files(dest / name))
            if installed != json.loads(receipt.read_text(encoding="utf-8")) or installed != fingerprint(sources[name]):
                raise ValueError(f"{name}: installed content differs from package or receipt")
            print(f"verified {name}")
        return

    dest.mkdir(parents=True, exist_ok=True)
    state.mkdir(exist_ok=True)
    with lock(state):
        records.mkdir(exist_ok=True)
        backup_root.mkdir(exist_ok=True)
        plan = []
        for name in names:
            target, receipt = safe_path(dest / name), safe_path(records / (name + ".json"))
            exists, managed = live_path(target), live_path(receipt)
            if exists != managed or (command == "install" and exists):
                raise ValueError(f"{name}: existing or inconsistent installation; no files overwritten")
            if command != "install" and not managed:
                raise ValueError(f"{name}: skill not installed by AAES")
            if managed and fingerprint(tree_files(target)) != json.loads(receipt.read_text(encoding="utf-8")):
                raise ValueError(f"{name}: local modifications; preserve or reconcile them before continuing")
            plan.append((name, target, receipt, managed))

        # Commit each skill independently. Multi-skill operations preflight all
        # targets but can partially complete on an I/O failure; each step logs.
        for name, target, receipt, managed in plan:
            work = state / ("transaction-" + uuid4().hex)
            work.mkdir()
            staged = work / "new"
            backup = backup_root / (name + "-" + uuid4().hex) if managed else None
            previous_receipt = receipt.read_bytes() if managed else None
            moved_old = moved_new = False
            try:
                if command != "remove":
                    staged.mkdir()
                    for rel, path in sources[name].items():
                        output = staged / rel
                        output.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copyfile(path, output)
                    snapshot = fingerprint(tree_files(staged))
                    if snapshot != fingerprint(sources[name]):
                        raise ValueError(f"{name}: package changed during copy")
                if backup:
                    target.rename(backup)
                    moved_old = True
                if command == "remove":
                    receipt.unlink()
                else:
                    staged.rename(target)
                    moved_new = True
                    write_manifest(receipt, snapshot)
            except Exception:
                if moved_new:
                    target.rename(staged)
                if moved_old:
                    backup.rename(target)
                    if not receipt.exists():
                        receipt.write_bytes(previous_receipt)
                raise
            finally:
                shutil.rmtree(work)
            print(f"{command} {name}" + (f" | backup: {backup}" if backup else ""))


def select(data, names, group):
    if names:
        if len(names) != len(set(names)) or any(name not in data or not NAME.fullmatch(name) for name in names):
            raise ValueError("Unknown or duplicate skill")
        return names
    selection = sorted(name for name, item in data.items() if not group or item["group"] == group)
    if not selection or any(not NAME.fullmatch(name) for name in selection):
        raise ValueError("Empty or invalid catalog group")
    return selection


def export(dest, names):
    dest = safe_path(Path(os.path.abspath(dest)))
    dest.mkdir(parents=True, exist_ok=True)
    archives = [safe_path(dest / (name + ".zip")) for name in names]
    if any(live_path(path) for path in archives):
        raise ValueError("Export would overwrite an existing archive")
    for name, archive in zip(names, archives):
        files = tree_files(ROOT / "skills" / name, source=True)
        with ZipFile(archive, "x", ZIP_DEFLATED) as out:
            for rel, path in files.items():
                out.write(path, name + "/" + rel)
        print(f"export {archive}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["list", "install", "update", "verify", "remove", "export"])
    parser.add_argument("--target", choices=["codex", "claude", "generic"], default="generic")
    parser.add_argument("--destination", type=Path)
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--skill", action="append")
    selection.add_argument("--group")
    args = parser.parse_args()
    try:
        data = catalog()
        names = select(data, args.skill, args.group)
        if args.command == "list":
            for name in names:
                print(f"{name}\t{data[name]['group']}\t{data[name]['outcome']}")
        elif args.command == "export":
            export(args.destination or ROOT / "dist", names)
        else:
            dest = args.destination or default_path(args.target)
            # Prevent modifying the distribution from which this command runs.
            normalized = Path(os.path.abspath(dest))
            if normalized == ROOT or normalized in ROOT.parents or normalized.is_relative_to(ROOT / "skills"):
                raise ValueError("Destination overlaps package sources")
            operate(args.command, normalized, names, ROOT / "skills")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"AAES: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
