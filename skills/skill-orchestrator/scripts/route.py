"""Rank host-classified capabilities, without invoking tools or models."""
import argparse
import json
from pathlib import Path

CATALOG = Path(__file__).resolve().parents[1] / "references" / "catalog.json"
LEVEL = {"low": 0, "moderate": 1, "high": 2}


def strings(value, label):
    if not isinstance(value, list) or any(type(item) is not str or not item for item in value):
        raise ValueError(f"{label} must be a list of nonempty strings")
    if len(value) != len(set(value)):
        raise ValueError(f"{label} contains duplicates")
    return value


def route(request, skills):
    keys = {"mode", "primary", "secondary", "explicit", "risk_limit", "budget",
            "max_skills", "inputs", "available", "tools", "constraints",
            "host", "execution_authorized"}
    if not isinstance(request, dict) or request.keys() - keys:
        raise ValueError("Invalid request fields")
    mode = request.get("mode", "recommend")
    primary = request.get("primary")
    explicit = request.get("explicit")
    if any(v is not None and (type(v) is not str or not v) for v in (primary, explicit)):
        raise ValueError("primary and explicit must be nonempty strings or null")
    if mode not in ("recommend", "execute", "explicit") or (mode == "explicit" and not explicit):
        raise ValueError("Invalid mode or missing explicit skill")
    if mode == "recommend" and explicit:
        raise ValueError("Use explicit mode for a named skill")
    secondary = strings(request.get("secondary", []), "secondary")
    if primary in secondary:
        raise ValueError("primary must not be repeated in secondary")
    inputs = set(strings(request.get("inputs", []), "inputs"))
    constraints = set(strings(request.get("constraints", []), "constraints"))
    if constraints - {"read_only", "offline", "no_delegation", "plan_only"}:
        raise ValueError("Unknown constraint")
    available = set(strings(request.get("available", list(skills)), "available"))
    tools = set(strings(request.get("tools", []), "tools"))
    risk_limit = request.get("risk_limit", "moderate")
    budget, limit = request.get("budget", 6), request.get("max_skills", 3)
    authorized = request.get("execution_authorized", False)
    host = request.get("host", "generic")
    if risk_limit not in LEVEL or host not in ("generic", "codex", "claude"):
        raise ValueError("Invalid risk_limit or host")
    if type(budget) is not int or budget < 0 or type(limit) is not int or limit < 1:
        raise ValueError("Invalid budget or max_skills")
    if type(authorized) is not bool:
        raise ValueError("execution_authorized must be boolean")

    selected, excluded, used = {}, {}, 0

    def propose(name, why, capability=None):
        nonlocal used
        pending = {}

        def collect(current, reason, cap, visiting):
            if current in visiting:
                raise ValueError("cyclic dependency")
            if current in selected or current in pending:
                return
            if current not in available or current not in skills:
                raise ValueError(f"{current} unavailable")
            item = skills[current]
            if host not in item["compatibility"]:
                raise ValueError(f"{current} incompatible with {host}")
            if LEVEL[item["risk"]] > LEVEL[risk_limit]:
                raise ValueError(f"{current} exceeds risk limit")
            for dependency in item["dependencies"]:
                collect(dependency, f"dependency of {current}", None, visiting | {current})
            for other in set(selected) | set(pending):
                if other in item["conflicts"] or current in skills[other]["conflicts"]:
                    raise ValueError(f"{current} conflicts with {other}")
            missing = sorted(set(item["prerequisites"]) - inputs)
            planning = "plan_only" in constraints or (cap or "").startswith("design_")
            planning |= (cap or "").startswith("plan_") or cap == "route_skills"
            action = "plan" if missing or planning else "analyze"
            if action not in item["modes"]:
                raise ValueError(f"{current} cannot operate in {action} mode")
            optional = tools & set(item["optional_tools"])
            if "offline" in constraints or "plan_only" in constraints:
                optional.discard("network")
            if "read_only" in constraints or action == "plan":
                optional.difference_update({"test_runner", "checkpoint_store", "isolated_runner", "trainer"})
            if "no_delegation" in constraints or "offline" in constraints or action == "plan":
                optional.discard("subagents")
            pending[current] = {"skill": current, "reason": reason, "capability": cap,
                                "mode": action, "missing_inputs": missing,
                                "optional_tools_available": sorted(optional),
                                "outcome": item["outcome"], "cost_units": item["cost"]}

        try:
            collect(name, why, capability, set())
            added = sum(row["cost_units"] for row in pending.values())
            if len(selected) + len(pending) > limit or used + added > budget:
                raise ValueError("selection exceeds budget or skill limit")
        except ValueError as exc:
            excluded[name] = str(exc)
            return False
        selected.update(pending)
        used += added
        return True

    def match(cap, priority):
        if cap is None or any(cap in skills[name]["capabilities"] for name in selected):
            return True
        matches = [name for name, item in skills.items()
                   if cap in item["capabilities"] and item["group"] != "routing"]
        matches.sort(key=lambda name: (
            not set(skills[name]["prerequisites"]) <= inputs,
            skills[name]["cost"], LEVEL[skills[name]["risk"]], name))
        return any(propose(name, priority, cap) for name in matches)

    if explicit:
        ready = propose(explicit, "explicit user selection", primary)
    else:
        ready = match(primary, "primary requested outcome")
    unmet = []
    if not ready and (explicit or primary):
        unmet.append(primary or explicit)
    if ready:
        for cap in secondary:
            if not match(cap, "distinct secondary outcome"):
                unmet.append(cap)
    # No external effects. This is a dispatch recommendation for the host.
    dispatch = "not_requested" if mode == "recommend" else "not_dispatched"
    if mode == "execute" and not authorized:
        dispatch = "authorization_required"
    elif mode in ("execute", "explicit") and "available" in request and "plan_only" not in constraints:
        dispatchable = all(row["mode"] == "analyze" for row in selected.values())
        dispatch = ("host_may_dispatch_within_scope"
                    if authorized and selected and not unmet and (mode == "explicit" or dispatchable)
                    else "not_dispatched")
    return {"mode": mode, "decision": "select" if selected else "abstain",
            "selected": list(selected.values()), "excluded": excluded, "unmet": unmet,
            "constraints": sorted(constraints), "cost_units": used, "dispatch": dispatch}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("request", type=Path)
    args = parser.parse_args()
    try:
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        result = route(json.loads(args.request.read_text(encoding="utf-8")), catalog["skills"])
    except (ValueError, TypeError, KeyError, OSError) as exc:
        parser.exit(2, f"Invalid routing input: {exc}\n")
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
