"""AAES portable JSON contract, version 1 (mirrored from tools/production/_contract.py)."""
import argparse
import hashlib
import json
import math
from pathlib import Path


def unique(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError(f"Duplicate key: {key}")
        result[key] = value
    return result


def number(value, label, lo=0):
    if type(value) not in (int, float) or not math.isfinite(value) or value < lo:
        raise ValueError(f"Invalid {label}")
    return value


def integer(value, label, lo=0):
    if type(value) is not int or value < lo:
        raise ValueError(f"Invalid {label}")
    return value


def string(value, label):
    if type(value) is not str or not value.strip():
        raise ValueError(f"Invalid {label}")
    return value


def sequence(value, label, maximum=2000):
    if not isinstance(value, list) or len(value) > maximum:
        raise ValueError(f"Invalid {label} list")
    return value


def strings(value, label):
    items = [string(item, label) for item in sequence(value, label)]
    if len(items) != len(set(items)):
        raise ValueError(f"Duplicate {label}")
    return items


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False, separators=(",", ":")).encode("ascii")


def bounded_read(path, limit=2_000_000):
    with path.open("rb") as stream:
        data = stream.read(limit + 1)
    if len(data) > limit:
        raise ValueError("Input exceeds size limit")
    return data


def contained(root, relative):
    part = Path(string(relative, "relative path"))
    if part.anchor or ":" in relative or ".." in part.parts:
        raise ValueError("Expected a repository-relative path")
    path = (root / part).resolve()
    if not path.is_relative_to(root):
        raise ValueError("Path escapes repository")
    return path


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    def finite(token):
        value = float(token)
        if not math.isfinite(value):
            raise ValueError("Non-finite JSON number")
        return value
    data = json.loads(bounded_read(path), object_pairs_hook=unique, parse_float=finite, parse_constant=finite)
    if not isinstance(data, dict) or type(data.get("schema_version")) is not int or data["schema_version"] != 1:
        raise ValueError("Expected JSON object with schema_version 1")
    return data


def main(analyze, description):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(analyze(read_json(args.input)), allow_nan=False, indent=2))
    except (ValueError, TypeError, KeyError, OSError, ArithmeticError, RecursionError, AttributeError) as exc:
        parser.exit(2, f"Invalid input: {exc}\n")
