"""Check compacted task state against a trusted checkpoint and local artifacts."""
from pathlib import Path
import re
from _contract import bounded_read, canonical, contained, digest, main, sequence, string, strings

FIELDS = ("objective","constraints","state","decisions","artifacts","evidence","next_actions","errors")


def validate(checkpoint):
    if type(checkpoint.get("schema_version")) is not int or checkpoint["schema_version"] != 1:
        raise ValueError("Invalid checkpoint version")
    string(checkpoint["objective"], "objective")
    strings(checkpoint["constraints"], "constraint")
    if not isinstance(checkpoint["state"], dict):
        raise ValueError("Expected operational state object")
    for key in ("decisions","evidence","next_actions","errors"):
        sequence(checkpoint[key], key)
    artifacts = sequence(checkpoint["artifacts"], "artifacts")
    strings([row["path"] for row in artifacts], "artifact path")
    for row in artifacts:
        if not re.fullmatch(r"[a-f0-9]{64}", row["sha256"]):
            raise ValueError("Invalid artifact digest")


def analyze(doc):
    left, right = doc["original"], doc["restored"]
    validate(left)
    validate(right)
    changes = [name for name in FIELDS if canonical(left[name]) != canonical(right[name])]
    bad = []
    root = Path(doc["root"]).resolve(strict=True) if "root" in doc else None
    if root is not None:
        if not root.is_dir():
            raise ValueError("Root must be a directory")
        for row in right["artifacts"]:
            path = contained(root, row["path"])
            if not path.is_file() or digest(bounded_read(path)) != row["sha256"]:
                bad.append(row["path"])
    return {"status": "mismatch" if changes or bad else
            "artifacts_unverified" if right["artifacts"] and root is None else "matched",
            "changed_fields": changes, "artifact_mismatches": bad, "artifact_bytes_checked": root is not None}


if __name__ == "__main__":
    main(analyze, __doc__)
