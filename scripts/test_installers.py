"""Smoke-test the documented installer against an isolated destination."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from zipfile import ZipFile

from manage import ROOT, catalog, tree_files


def run(argv, env, expected=0):
    result = subprocess.run(list(map(str, argv)), cwd=ROOT, env=env,
                            capture_output=True, timeout=30)
    if result.returncode != expected:
        raise RuntimeError(f"Unexpected exit {result.returncode}: {result.stderr.decode(errors='replace')}")


def verify_archives(folder, names):
    assert {p.stem for p in folder.glob("*.zip")} == names
    for name in names:
        source = tree_files(ROOT/"skills"/name)
        with ZipFile(folder/(name+".zip")) as archive:
            assert sorted(archive.namelist()) == sorted(f"{name}/{rel}" for rel in source)
            assert archive.testzip() is None
            for rel, path in source.items():
                assert archive.read(f"{name}/{rel}") == path.read_bytes(), f"ZIP mismatch: {name}/{rel}"


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--shell", help="Override the default shell for POSIX installer testing")
    cli.add_argument("--published", action="store_true", help="Also verify the ZIPs checked into dist/")
    args = cli.parse_args()
    env = os.environ | {"AAES_PYTHON": Path(sys.executable).as_posix()}
    names = set(catalog())
    with tempfile.TemporaryDirectory() as temp:
        folder = Path(temp).resolve()
        destination = folder / "destination with spaces"
        if os.name == "nt" and not args.shell:
            powershell = shutil.which("pwsh") or shutil.which("powershell")
            if not powershell:
                cli.error("PowerShell was not found")
            installer = [powershell, "-NoProfile", "-File", ROOT/"scripts/install.ps1",
                         "-Target","codex","-InstallPath",destination]
            single = installer + ["-Skill","process-verifier"]
        else:
            installer = [args.shell or "sh", "scripts/install.sh", "claude", "all", destination]
            single = [args.shell or "sh", "scripts/install.sh", "claude", "process-verifier", destination]
        run(single, env)
        assert {p.name for p in destination.iterdir()} == {"process-verifier"}
        run(installer, env)
        run(installer, env)
        run([sys.executable, ROOT/"scripts/manage.py", "verify", "--destination", destination], env)
        assert {p.name for p in destination.iterdir()} == names
        archives = folder/"archives"
        run([sys.executable, ROOT/"scripts/manage.py", "export", "--destination", archives], env)
        verify_archives(archives, names)
    if args.published:
        verify_archives(ROOT/"dist", names)
    print(json.dumps({"verified_skills":len(names), "portable_zips":len(names),
                      "single_skill_and_resumable_catalog":True,
                      "published_zips_verified":args.published,
                      "wrapper":"powershell" if os.name == "nt" and not args.shell else "posix"}))


if __name__ == "__main__":
    main()
