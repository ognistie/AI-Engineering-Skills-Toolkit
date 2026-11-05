"""Summarize paired activation-patching measurements and negative controls."""
from math import isfinite
from statistics import fmean


def finite(value):
    if type(value) not in (int, float) or not isfinite(value):
        raise ValueError("Metric must be finite")
    return value


def analyze(doc):
    threshold = finite(doc["min_baseline_gap"])
    if threshold <= 0:
        raise ValueError("min_baseline_gap must be positive")
    pairs = doc["pairs"]
    if not isinstance(pairs, list) or not pairs:
        raise ValueError("Expected paired measurements")
    ids, included, excluded = set(), [], []
    for pair in pairs:
        key = pair["id"]
        if type(key) is not str or not key or key in ids:
            raise ValueError("Missing or duplicate pair identifier")
        ids.add(key)
        clean, corrupt, patch, control = (finite(pair[k]) for k in ("clean", "corrupt", "patched", "control"))
        gap = finite(clean - corrupt)
        if gap < threshold:
            excluded.append(key)
            continue
        restored = finite((patch - corrupt) / gap)
        negative = finite((control - corrupt) / gap)
        included.append({"id": key, "clean_corrupt_gap": gap, "patch_restoration": restored,
                         "control_restoration": negative, "patch_minus_control": finite(restored - negative)})
    summary = {k: fmean(row[k] for row in included) for k in
               ("patch_restoration", "control_restoration", "patch_minus_control")} if included else None
    return {"status": "descriptive_only" if included else "no_usable_pairs",
            "included": included, "excluded_small_or_reversed_gap": excluded, "means": summary}

def _pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def _nonfinite(value):
    raise ValueError(f"Invalid JSON constant: {value}")


def main():
    import argparse
    import json
    from pathlib import Path

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    try:
        with args.input.open("rb") as stream:
            raw = stream.read(2_000_001)
        if len(raw) > 2_000_000:
            raise ValueError("Input exceeds 2 MB")
        document = json.loads(raw, object_pairs_hook=_pairs, parse_constant=_nonfinite)
        print(json.dumps(analyze(document), allow_nan=False, indent=2))
    except (ValueError, TypeError, KeyError, OSError, ArithmeticError, RecursionError) as exc:
        parser.exit(2, f"Invalid input: {exc}\n")


if __name__ == "__main__":
    main()
