"""Replay a trusted state machine and report the first deterministic violation."""
from _contract import integer, main, sequence, string


def analyze(doc):
    state = string(doc["initial_state"], "initial state")
    budget = integer(doc["budget"], "budget")
    transitions = doc["transitions"]
    if not isinstance(transitions, dict):
        raise ValueError("Transitions must be an object")
    for name, edges in transitions.items():
        string(name, "transition state")
        for action, target in edges.items():
            string(action, "transition action")
            string(target, "transition target")
    seen, accepted, spent = set(), [], 0
    for event in sequence(doc["events"], "events"):
        key = string(event["id"], "event ID")
        index = integer(event["seq"], "sequence", 1)
        action = string(event["action"], "action")
        units = integer(event["units"], "units")
        target = transitions.get(state, {}).get(action)
        rule = ("replay" if key in seen else "sequence_gap" if index != len(accepted)+1
                else "invalid_transition" if target is None else "budget_exhausted" if spent+units > budget else None)
        if rule:
            return {"decision":"block","violation":rule,"event":key,"state":state,
                    "spent":spent,"accepted":accepted}
        state, spent = target, spent+units
        seen.add(key)
        accepted.append(key)
    return {"decision":"allow","state":state,"spent":spent,"accepted":accepted}


if __name__ == "__main__":
    main(analyze, __doc__)
