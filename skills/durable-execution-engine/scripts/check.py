"""Advise recovery from the existing AAES checkpoint status without executing effects."""
from _contract import integer, main, string


def analyze(doc):
    journal = doc["journal"]
    state = journal["state"]
    phase = state["phase"]
    attempts = integer(state["attempts"], "attempts")
    maximum = integer(doc["max_attempts"], "max attempts", 1)
    elapsed = integer(doc["elapsed_ms"], "elapsed")
    deadline = integer(doc["deadline_ms"], "deadline", 1)
    initial = integer(doc["base_delay_ms"], "base delay", 1)
    cap = integer(doc["max_delay_ms"], "delay cap", initial)
    operation = state.get("operation")
    if operation is not None:
        string(operation, "operation ID")
    if phase == "in_flight":
        claim = string(state["active_claim_id"], "active claim ID")
        return {"decision":"reconcile","operation":string(operation,"operation ID"),"claim_id":claim}
    if phase == "done":
        return {"decision":"stop_completed"}
    if phase == "blocked":
        compensation = doc.get("compensation")
        if compensation is not None:
            if type(compensation["authorized"]) is not bool:
                raise ValueError("Compensation authority must be boolean")
            key = string(compensation["operation"], "compensation operation")
            if compensation["authorized"] and key != operation and elapsed < deadline:
                return {"decision":"review_compensation","operation":key,"prior_operation":operation}
        return {"decision":"operator_review"}
    if phase != "ready":
        raise ValueError("Unknown checkpoint phase")
    if attempts >= maximum or elapsed >= deadline:
        return {"decision":"stop_budget"}
    if attempts:
        string(operation, "prior operation ID")
        string(state["last_evidence"], "no-effect evidence reference")
    delay = min(cap, initial * 2 ** min(63, max(0, attempts-1))) if attempts else 0
    if elapsed + delay >= deadline:
        return {"decision":"stop_deadline"}
    return {"decision":"retry_same_operation" if attempts else "claim_first_attempt",
            "operation":operation,"backoff_ms":delay}


if __name__ == "__main__":
    main(analyze, __doc__)
