"""Choose whether a bounded revision loop should continue, preserving verified artifacts."""
import re
from _contract import integer, main, number, sequence, string


def analyze(doc):
    rubric = string(doc["rubric"], "rubric revision")
    cap = integer(doc["max_iterations"], "iteration cap", 1)
    budget = integer(doc["budget"], "budget")
    cost = integer(doc["next_cost"], "next cost", 1)
    patience = integer(doc["patience"], "patience", 1)
    target = number(doc["target_score"], "target score")
    history = sequence(doc["history"], "history")
    best, seen, duplicate, stale, spent = None, set(), False, 0, 0
    for row in history:
        key = row["artifact_sha256"]
        if row["rubric"] != rubric or not re.fullmatch(r"[a-f0-9]{64}", key) or type(row["verified"]) is not bool:
            raise ValueError("Unbound or invalid iteration")
        spent += integer(row["cost"], "iteration cost")
        score = number(row["score"], "score")
        duplicate |= key in seen
        seen.add(key)
        if row["verified"] and (best is None or score > best["score"]):
            best, stale = {"artifact_sha256":key,"score":score}, 0
        else:
            stale += 1
    reason = ("history_exceeds_limits" if spent > budget or len(history) > cap else
              "verified_target" if best and best["score"] >= target else
              "repeated_artifact" if duplicate else
              "stalled" if stale >= patience else
              "iteration_limit" if len(history) >= cap else
              "budget_limit" if spent + cost > budget else "feedback_iteration")
    return {"decision":"continue" if reason == "feedback_iteration" else "stop",
            "reason":reason,"best_verified":best,"spent":spent,"iterations":len(history)}


if __name__ == "__main__":
    main(analyze, __doc__)
