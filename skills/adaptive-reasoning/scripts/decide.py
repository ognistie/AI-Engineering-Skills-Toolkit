"""Choose an external next step under a frozen budget."""


def analyze(doc):
    evidence = doc["evidence"]
    if evidence not in ("not_started", "uncertain", "disagreement", "verified", "stalled", "blocked"):
        raise ValueError("Unknown evidence state")
    remaining = {}
    for key in ("attempts", "ms", "cost_units"):
        cap, used, price = (doc[section][key] for section in ("limit", "spent", "next_cost"))
        if any(type(v) is not int or v < 0 for v in (cap, used, price)):
            raise ValueError(f"{key}: expected nonnegative integers")
        remaining[key] = cap - used
    if doc["next_cost"]["attempts"] < 1:
        raise ValueError("A new action consumes at least one attempt")
    authorized = doc["authorized"]
    if type(authorized) is not bool:
        raise ValueError("authorized must be boolean")
    action = doc.get("next_observation")
    if action is not None and (type(action) is not str or not action.strip()):
        raise ValueError("next_observation must be nonempty")
    if any(v < 0 for v in remaining.values()):
        decision, reason = "stop", "budget_already_exceeded"
    elif evidence == "verified":
        decision, reason = "stop", "verified_success"
    elif evidence in ("stalled", "blocked") or not authorized:
        decision, reason = "stop", "no_progress_or_authority"
    elif any(remaining[k] < doc["next_cost"][k] for k in remaining):
        decision, reason = "stop", "next_action_exceeds_budget"
    elif evidence == "not_started":
        decision, reason = "direct", "smallest_viable_attempt"
    elif not action:
        decision, reason = "stop", "no_discriminating_observation"
    elif evidence == "disagreement":
        decision, reason = "verify", "independent_check_needed"
    else:
        decision, reason = "escalate", "resolve_actionable_uncertainty"
    return {"decision": decision, "reason": reason, "remaining": remaining,
            "next_observation": action if decision != "stop" else None}

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
