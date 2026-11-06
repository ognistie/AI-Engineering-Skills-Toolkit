"""Validate AAES catalog, portable skill metadata and local references."""
import json
from pathlib import Path
import re
import sys

import yaml

from manage import CATALOG, NAME, ROOT, tree_files


class UniqueLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node):
    result = {}
    for key, value in loader.construct_pairs(node):
        if not isinstance(key, str) or key in result:
            raise ValueError(f"Duplicate or non-string YAML key: {key!r}")
        result[key] = value
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def string_list(value, label, *, nonempty=False):
    if (not isinstance(value, list) or nonempty and not value
        or any(type(v) is not str or not v for v in value) or len(value) != len(set(value))):
        raise ValueError(f"{label}: expected unique strings")


def validate():
    root = ROOT / "skills"
    document = json.loads(CATALOG.read_text(encoding="utf-8"), object_pairs_hook=unique_json)
    skills = document["skills"]
    if document.keys() != {"schema_version", "skills"} or document["schema_version"] != 1:
        raise ValueError("Invalid catalog version or fields")
    if not skills or set(skills) != {p.name for p in root.iterdir() if p.is_dir()}:
        raise ValueError("Skill folder inventory differs from registry")
    lists = {"capabilities", "optional_tools", "prerequisites", "dependencies", "conflicts", "compatibility", "modes"}
    fields = lists | {"group", "outcome", "cost", "risk"}
    for name, item in skills.items():
        if not NAME.fullmatch(name) or len(name) > 64 or item.keys() != fields:
            raise ValueError(f"Invalid name or registry fields: {name}")
        for field in lists:
            string_list(item[field], f"{name}.{field}", nonempty=field in {"capabilities", "compatibility", "modes"})
        if (set(item["compatibility"]) - {"codex", "claude", "generic"} or set(item["modes"]) - {"plan", "analyze"}
            or item["risk"] not in ("low", "moderate", "high")
            or type(item["cost"]) is not int or item["cost"] < 1
            or any(type(item[k]) is not str or not item[k].strip() for k in ("outcome", "group"))):
            raise ValueError(f"Invalid registry contract: {name}")
        deps, conflicts = set(item["dependencies"]), set(item["conflicts"])
        if deps & conflicts or (deps | conflicts) - (skills.keys() - {name}):
            raise ValueError(f"Invalid dependency or conflict: {name}")
        folder = root / name
        files = tree_files(folder)
        parts = files["SKILL.md"].read_text(encoding="utf-8").splitlines()
        if not parts or parts[0] != "---" or "---" not in parts[1:]:
            raise ValueError(f"No YAML frontmatter: {name}")
        end = parts.index("---", 1)
        meta = yaml.load("\n".join(parts[1:end]), Loader=UniqueLoader)
        if (not isinstance(meta, dict) or meta.keys() - {"name", "description", "metadata"}
            or meta.get("name") != name or type(meta.get("description")) is not str
            or not 1 <= len(meta["description"].strip()) <= 1024
            or len(parts) <= end + 1 or len(parts) > 500):
            raise ValueError(f"Invalid skill metadata/body: {name}")
        if not isinstance(meta.get("metadata"), dict) or any(type(v) is not str for v in meta["metadata"].values()):
            raise ValueError(f"Expected string metadata: {name}")
        if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", meta["metadata"].get("version", "")):
            raise ValueError(f"Expected version: {name}")
        for required in ("RESEARCH_BASIS.md", "TECHNICAL_GUIDE.md", "USE_CASES.md"):
            if f"references/{required}" not in files:
                raise ValueError(f"Missing {name}/{required}")
        for source in files.values():
            if source.suffix != ".md":
                continue
            for link in re.findall(r"\]\(([^)]+)\)", source.read_text(encoding="utf-8")):
                target = link.split("#", 1)[0]
                if not target or target.startswith(("https://", "http://")):
                    continue
                resolved = (source.parent / target).resolve()
                if not resolved.is_relative_to(folder.resolve()) or not resolved.is_file():
                    raise ValueError(f"Invalid local link {link} in {source}")
    def closure(name, seen):
        if name in seen:
            raise ValueError(f"Cyclic dependencies: {name}")
        result = {name}
        for child in skills[name]["dependencies"]:
            result |= closure(child, seen | {name})
        return result
    for name in skills:
        required = closure(name, set())
        if any(required & set(skills[member]["conflicts"]) for member in required):
            raise ValueError(f"Conflicting dependency closure: {name}")
    return len(skills)


def unique_json(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate registry key: {key}")
        result[key] = value
    return result


if __name__ == "__main__":
    try:
        print(f"Validated {validate()} skills and their registry/resources")
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError) as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
