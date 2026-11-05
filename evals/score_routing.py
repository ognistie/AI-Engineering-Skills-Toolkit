"""Score fixed routing-policy fixtures or externally observed host recommendations."""
import argparse
import importlib.util
import json
from pathlib import Path
from statistics import fmean
from time import perf_counter

HERE = Path(__file__).resolve().parent


def routing_module():
    location = HERE.parent / "skills/skill-orchestrator/scripts/route.py"
    spec = importlib.util.spec_from_file_location("aaes_route", location)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def score(cases, rows, k):
    expected_ids = [case["id"] for case in cases]
    if not expected_ids or len(set(expected_ids)) != len(expected_ids) or set(rows) != set(expected_ids):
        raise ValueError("Cases and observations require matching, unique IDs")
    precision, recall, unwanted, omitted, restricted, exact = [], [], [], [], [], []
    for case in cases:
        row = rows[case["id"]]
        ids = [item["skill"] for item in row["selected"]]
        if len(ids) != len(set(ids)):
            raise ValueError(f"Duplicate selection: {case['id']}")
        actual = set(ids[:k])
        expected = set(case["expected"]["skills"])
        precision.append(len(actual & expected) / len(actual) if actual else float(not expected))
        recall.append(len(actual & expected) / len(expected) if expected else 1.0)
        unwanted.append(bool(set(ids) - expected))
        omitted.append(bool(expected - set(ids)))
        policy = case["expected"].get("policy", {})
        restricted.append(all(row.get(field) == value for field, value in policy.items()))
        exact.append(ids == case["expected"]["skills"])
    return {"cases": len(cases), "k": k, "precision_at_k": fmean(precision),
            "recall_at_k": fmean(recall), "unnecessary_selection_case_rate": fmean(unwanted),
            "omission_case_rate": fmean(omitted), "restriction_check_case_rate": fmean(restricted),
            "exact_order_case_rate": fmean(exact)}


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--observed", type=Path, help="JSON keyed by case ID; do not include reference labels in host prompts")
    cli.add_argument("--k", type=int, default=3)
    args = cli.parse_args()
    if args.k < 1:
        cli.error("--k must be positive")
    cases = json.loads((HERE / "routing/cases.json").read_text(encoding="utf-8"))
    if args.observed:
        rows = json.loads(args.observed.read_text(encoding="utf-8"))
        timing = {"source": "external observations; provenance not verified", "local_policy_mean_ms": None}
    else:
        runner = routing_module()
        catalog = json.loads(runner.CATALOG.read_text(encoding="utf-8"))["skills"]
        start = perf_counter()
        rows = {case["id"]: runner.route(case["classification"], catalog) for case in cases}
        elapsed = (perf_counter() - start) * 1000 / len(cases)
        timing = {"source": "offline policy with supplied classifications; not natural language accuracy",
                  "local_policy_mean_ms": round(elapsed, 4), "additional_model_calls": 0}
    result = score(cases, rows, args.k) | timing
    print(json.dumps(result, indent=2))
    if not args.observed and (result["exact_order_case_rate"] != 1 or result["restriction_check_case_rate"] != 1):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
