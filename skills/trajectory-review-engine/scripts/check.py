"""Flag invalid events, failed same-state loops and outcome disagreement."""
from _contract import integer, main, sequence, string, strings


def analyze(doc):
    threshold = integer(doc.get("loop_threshold", 3), "loop threshold", 2)
    events = sequence(doc["events"], "events")
    strings([event["id"] for event in events], "event ID")
    if "span_summary" in doc:
        order = strings(doc["span_summary"]["chronology"], "span event ID")
        by_id = {event["id"]: event for event in events}
        if set(order) != by_id.keys():
            raise ValueError("Span chronology and event IDs must match")
        events = [by_id[key] for key in order]
    loops, invalid, by_operation = [], [], {}
    for event in events:
        status = event["status"]
        if status not in ("ok","timeout","error","invalid","denied"):
            raise ValueError("Unknown event status")
        operation = string(event["operation"], "operation")
        state = string(event["state"], "state reference")
        if status in ("invalid","denied"):
            invalid.append(event["id"])
        if status == "ok":
            by_operation.pop(operation, None)
            continue
        prior_state, window = by_operation.get(operation, (None, []))
        if state != prior_state:
            window = []
            by_operation[operation] = (state, window)
        window.append(event["id"])
        if len(window) == threshold:
            loops.append({"operation":operation,"unchanged_state":state,"events":window.copy()})
    claims = [doc.get(k) for k in ("claimed_success","observed_success")]
    if any(value is not None and type(value) is not bool for value in claims):
        raise ValueError("Outcomes must be booleans or null")
    return {"invalid_or_denied":invalid,"loop_candidates":loops,"outcome_disagreement":None if None in claims
            else claims[0] != claims[1],"causal_attribution":"not_verified"}


if __name__ == "__main__":
    main(analyze, __doc__)
