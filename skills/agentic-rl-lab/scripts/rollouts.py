"""Validate environment logs and compute offline discounted returns."""
from collections import Counter
from math import isfinite
from statistics import fmean


def finite(value, minimum=0):
    if type(value) not in (int, float) or not isfinite(value) or value < minimum:
        raise ValueError("Invalid numeric value")
    return value


def analyze(doc):
    config, episodes = doc["environment"], doc["episodes"]
    gamma = finite(config["gamma"])
    step_limit = config["step_limit"]
    if gamma > 1 or type(step_limit) is not int or step_limit < 1:
        raise ValueError("Invalid discount or step limit")
    actions = config["allowed_actions"]
    if (not isinstance(actions, list) or not actions or any(type(v) is not str or not v for v in actions)
        or len(set(actions)) != len(actions)):
        raise ValueError("Expected unique allowed actions")
    success_states = config.get("success_states")
    if "success_states" in config and (
            not isinstance(success_states, list) or not success_states
            or any(type(v) is not str or not v for v in success_states)):
        raise ValueError("Expected nonempty trusted success state IDs")
    terminal = ("success", "failure", "timeout", "unsafe")
    reward = config["terminal_reward"]
    if set(reward) != set(terminal):
        raise ValueError("Expected a reward for each terminal outcome")
    for value in reward.values():
        finite(value, -float("inf"))
    if reward["success"] <= 0 or any(reward[k] > 0 for k in terminal if k != "success"):
        raise ValueError("Success must earn positive reward and failures cannot earn positive reward")
    cost_weight = finite(config["cost_weight"])
    if not isinstance(episodes, list) or not episodes:
        raise ValueError("Expected episodes")
    reports, seen = [], set()
    for episode in episodes:
        key, state, steps = episode["id"], episode["initial_state"], episode["steps"]
        if (any(type(x) is not str or not x for x in (key, state)) or key in seen
            or not isinstance(steps, list) or not 1 <= len(steps) <= step_limit):
            raise ValueError("Invalid episode identity or length")
        seen.add(key)
        seen_transitions, rewards, costs = set(), [], []
        for index, step in enumerate(steps):
            ident, action, new = (step[k] for k in ("id", "action", "next_state"))
            if (any(type(x) is not str or not x for x in (ident, action, new)) or ident in seen_transitions
                or step["state"] != state):
                raise ValueError(f"Invalid or discontinuous transition in {key}")
            seen_transitions.add(ident)
            state, outcome = new, step["outcome"]
            if (outcome not in (*terminal, "continue") or (outcome == "continue") != (index < len(steps) - 1)
                or (action not in actions) != (outcome == "unsafe")):
                raise ValueError(f"Invalid action or terminal transition in {key}")
            if success_states and (outcome == "success") != (new in success_states):
                raise ValueError(f"Terminal success and trusted state disagree in {key}")
            cost = finite(step["cost"])
            costs.append(cost)
            rewards.append(finite(reward.get(outcome, 0) - cost_weight * cost, -float("inf")))
        returns, total = [], 0
        for value in reversed(rewards):
            total = finite(value + gamma * total, -float("inf"))
            returns.append(total)
        reports.append({"id": key, "outcome": outcome, "cost": finite(sum(costs)),
                        "rewards": rewards, "returns_to_go": list(reversed(returns))})
    counts = Counter(row["outcome"] for row in reports)
    return {"episodes": reports, "outcomes": {key: counts[key] for key in terminal},
            "success_rate": counts["success"] / len(reports),
            "mean_cost": fmean(row["cost"] for row in reports), "training": "not_run"}

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
