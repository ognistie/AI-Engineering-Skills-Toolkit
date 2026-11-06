"""Score fixed routing-policy fixtures or externally observed host recommendations."""
import argparse
import importlib.util
import json
from pathlib import Path
from statistics import fmean
from time import perf_counter

HERE = Path(__file__).resolve().parent
WRITE_TOOLS = {"test_runner", "checkpoint_store", "isolated_runner", "trainer"}
FORBIDDEN_TOOLS = {
    "offline": {"network", "subagents"},
    "no_delegation": {"subagents"},
    "read_only": WRITE_TOOLS,
    "plan_only": WRITE_TOOLS | {"network", "subagents"},
}


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
    explanation_checks = []
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
        constraints = case.get("classification", {}).get("constraints", [])
        forbidden = set().union(*(FORBIDDEN_TOOLS[constraint] for constraint in constraints))
        if policy or forbidden:
            policy_ok = all(row.get(field) == value for field, value in policy.items())
            tools_ok = True
            if forbidden:
                for item in row["selected"]:
                    tools = item.get("optional_tools_available")
                    if not isinstance(tools, list) or any(
                        type(tool) is not str or tool in forbidden for tool in tools
                    ):
                        tools_ok = False
                        break
            restricted.append(policy_ok and tools_ok)
        exact.append(ids == case["expected"]["skills"])
        explanation_checks.append(bool(row.get("decision_reason")) and all(
            item.get("reason") and item.get("outcome") for item in row["selected"]))
    return {"cases": len(cases), "k": k, "precision_at_k": fmean(precision),
            "recall_at_k": fmean(recall), "unnecessary_selection_case_rate": fmean(unwanted),
            "omission_case_rate": fmean(omitted), "restriction_check_cases": len(restricted),
            "restriction_check_case_rate": fmean(restricted) if restricted else None,
            "exact_order_case_rate": fmean(exact), "structured_explanation_coverage": fmean(explanation_checks)}


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--observed", type=Path, help="JSON keyed by case ID; do not include reference labels in host prompts")
    cli.add_argument("--k", type=int, default=3)
    cli.add_argument("--annotations", type=Path, help="Compare recommendations with independent raw-prompt labels")
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
    if args.annotations:
        labels = json.loads(args.annotations.read_text(encoding="utf-8"))
        if set(labels) != rows.keys():
            cli.error("Annotation IDs must match the evaluation cases")
        disagreements = [key for key, row in rows.items()
                         if [item["skill"] for item in row["selected"]] != labels[key]["skills"]]
        result["independent_annotation"] = {"exact_order_agreement": 1 - len(disagreements) / len(rows),
                                            "disagreement_ids": disagreements}
    print(json.dumps(result, indent=2))
    restriction_failed = result["restriction_check_case_rate"] not in (1, None)
    if not args.observed and (result["exact_order_case_rate"] != 1 or restriction_failed):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
