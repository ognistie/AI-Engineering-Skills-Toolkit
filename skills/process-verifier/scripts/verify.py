"""Compare fixed JSON gates with independently collected observations."""
import argparse
import json
from pathlib import Path


def verify(contract, evidence):
    run = contract["run_id"]
    if type(run) is not str or not run or evidence["run_id"] != run:
        raise ValueError("Evidence must match the contract run_id")
    gates, records = contract["gates"], evidence["observations"]
    if not isinstance(gates, list) or not gates or not isinstance(records, list):
        raise ValueError("Expected nonempty gates and a list of observations")
    observations = {}
    identifiers = set()
    for row in records:
        key, identifier = row["key"], row["id"]
        if any(type(value) is not str or not value for value in (key, identifier, row["source"])):
            raise ValueError("Observation identity and source are required")
        if identifier in identifiers:
            raise ValueError("Duplicate observation ID")
        identifiers.add(identifier)
        observations.setdefault(key, []).append(row)
    results, seen = [], set()
    for gate in gates:
        key, source = gate["key"], gate["source"]
        if any(type(value) is not str or not value for value in (key, source)) or key in seen:
            raise ValueError("Gate must have a unique key and a source")
        seen.add(key)
        expected = gate["equals"]
        matches = [row for row in observations.get(key, []) if row["source"] == source]
        status = "missing"
        if len(matches) > 1:
            status = "disputed"
        elif matches:
            observed = matches[0]["value"]
            # Strict JSON equality recursively (true != 1, ordering of keys irrelevant).
            status = "passed" if canonical(observed) == canonical(expected) else "failed"
        results.append({"key": key, "status": status, "observations": [r["id"] for r in matches]})
    states = {row["status"] for row in results}
    overall = "failed" if "failed" in states else "inconclusive" if states != {"passed"} else "passed"
    return {"run_id": run, "status": overall, "gates": results}


def canonical(value):
    return json.dumps(value, sort_keys=True, allow_nan=False, separators=(",", ":"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("contract", type=Path)
    parser.add_argument("evidence", type=Path)
    args = parser.parse_args()
    try:
        result = verify(*(json.loads(path.read_text(encoding="utf-8")) for path in (args.contract, args.evidence)))
    except (ValueError, TypeError, KeyError, OSError) as exc:
        parser.exit(2, f"Invalid verification input: {exc}\n")
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["status"] == "passed" else 1)


if __name__ == "__main__":
    main()
