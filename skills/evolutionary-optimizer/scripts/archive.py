"""Keep feasible nondominated variants from complete development trials."""
from math import isfinite
from statistics import fmean


def unique(items):
    if not isinstance(items, list) or not items or any(type(x) is not str or not x for x in items) or len(set(items)) != len(items):
        raise ValueError("Expected unique nonempty identifiers")
    return set(items)


def finite(value):
    if type(value) not in (int, float) or not isfinite(value):
        raise ValueError("Expected finite measurement")
    return value


def analyze(doc):
    if doc["split"] != "development":
        raise ValueError("Do not use holdout measurements for archive selection")
    seeds = unique(doc["seeds"])
    goals, variants = doc["objectives"], doc["variants"]
    if not isinstance(goals, dict) or not goals or not isinstance(variants, list):
        raise ValueError("Expected objectives and a variant list")
    unique([v["id"] for v in variants])
    for goal in goals.values():
        if goal["direction"] not in ("min", "max"):
            raise ValueError("Unknown objective direction")
        if "hard_limit" in goal:
            finite(goal["hard_limit"])
    feasible, rejected = {}, {}
    for variant in variants:
        key, trials = variant["id"], variant["trials"]
        if not isinstance(trials, dict) or set(trials) != seeds:
            rejected[key] = "incomplete_or_unexpected_seeds"
            continue
        if any(not isinstance(trial, dict) or set(trial) != goals.keys() for trial in trials.values()):
            raise ValueError(f"Invalid metrics for {key}")
        values = {g: [finite(trials[seed][g]) for seed in sorted(seeds)] for g in goals}
        violates = [g for g, goal in goals.items() if "hard_limit" in goal and
                    (max(values[g]) > goal["hard_limit"] if goal["direction"] == "min"
                     else min(values[g]) < goal["hard_limit"])]
        if violates:
            rejected[key] = "hard_limit:" + ",".join(sorted(violates))
            continue
        feasible[key] = {g: fmean(vals) for g, vals in values.items()}
    transformed = {key: tuple(row[g] * (1 if goals[g]["direction"] == "max" else -1) for g in goals)
                   for key, row in feasible.items()}
    frontier = {key: feasible[key] for key, value in transformed.items()
                if not any(all(x >= y for x, y in zip(other, value)) and other != value
                           for other in transformed.values())}
    return {"frontier": frontier, "rejected": rejected, "dominated": sorted(feasible.keys() - frontier.keys()),
            "promotion": "not_evaluated"}

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
