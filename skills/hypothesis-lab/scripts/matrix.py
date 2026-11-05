"""Summarize independent support and conflicts for falsifiable hypotheses."""


def analyze(doc):
    hypotheses, evidence = doc["hypotheses"], doc["evidence"]
    if not isinstance(hypotheses, list) or len(hypotheses) < 2 or not isinstance(evidence, list):
        raise ValueError("Compare at least two hypotheses")
    ids = set()
    for item in hypotheses:
        name = item["id"]
        if type(name) is not str or not name or name in ids:
            raise ValueError("Invalid or duplicate hypothesis ID")
        for field in ("prediction", "falsifier"):
            if type(item[field]) is not str or not item[field].strip():
                raise ValueError(f"Missing {field} for {name}")
        ids.add(name)
    if doc["null_hypothesis"] not in ids:
        raise ValueError("Expected a declared null hypothesis")
    groups, observations = {}, set()
    for item in evidence:
        identifier, group = item["id"], item["group"]
        if any(type(v) is not str or not v for v in (identifier, group)) or identifier in observations:
            raise ValueError("Missing group or duplicate observation ID")
        observations.add(identifier)
        kind, direction, name = item["kind"], item["direction"], item["hypothesis"]
        if kind not in ("observation", "intervention") or direction not in ("supports", "contradicts", "neutral") or name not in ids:
            raise ValueError("Invalid evidence kind, direction or hypothesis")
        groups.setdefault((name, group), []).append((kind, direction))
    rows = []
    for name in sorted(ids):
        row = {"hypothesis": name, "independent_support": [], "independent_contradiction": [],
               "mixed": [], "intervention_support": [], "intervention_contradiction": []}
        for (hypothesis, group), entries in sorted(groups.items()):
            if hypothesis != name:
                continue
            directions = {direction for _, direction in entries} - {"neutral"}
            if len(directions) > 1:
                row["mixed"].append(group)
            elif directions == {"supports"}:
                row["independent_support"].append(group)
            elif directions == {"contradicts"}:
                row["independent_contradiction"].append(group)
            if ("intervention", "supports") in entries:
                row["intervention_support"].append(group)
            if ("intervention", "contradicts") in entries:
                row["intervention_contradiction"].append(group)
        rows.append(row)
    def rank(row):
        return (len(row["intervention_contradiction"]), -len(row["intervention_support"]),
                len(row["independent_contradiction"]), -len(row["independent_support"]))
    rows.sort(key=rank)
    tied = rank(rows[0]) == rank(rows[1])
    return {"ranking": rows, "leading_hypothesis": None if tied else rows[0]["hypothesis"],
            "status": "not_distinguished" if tied else "descriptive_only"}

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
