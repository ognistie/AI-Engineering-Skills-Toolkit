"""Score frozen trials using evidence from a trusted, separately collected ledger."""
from math import comb
from statistics import fmean

from _contract import canonical, integer, main, sequence, string, strings


def summarize(n, correct, k):
    combinations = comb(n, k)
    return {"pass@1": correct / n, "pass@k": 1 - comb(n-correct, k) / combinations,
            "pass^k": comb(correct, k) / combinations}


def analyze(doc):
    k = integer(doc["k"],"k",1)
    tasks = sequence(doc["tasks"],"tasks",512)
    strings([row["id"] for row in tasks],"task ID")
    protocol = {task["id"]:set(strings(task["planned_trial_ids"],"frozen trial ID")) for task in tasks}
    if any(len(ids) < k for ids in protocol.values()):
        raise ValueError("Frozen trials fewer than k")
    if not isinstance(doc["trusted_outcomes"],dict):
        raise ValueError("Expected trusted outcome ledger object")

    # One unique collector run and outcome record per frozen task/trial pair.
    ledger, covered, runs = {}, set(), set()
    for ref, item in doc["trusted_outcomes"].items():
        string(ref,"outcome reference")
        task_id = string(item["task_id"],"outcome task")
        trial_id = string(item["trial_id"],"outcome trial")
        run_id = string(item["run_id"],"collector run ID")
        pair = (task_id,trial_id)
        if trial_id not in protocol.get(task_id,set()):
            raise ValueError("Evidence is outside the frozen trial protocol")
        if pair in covered or run_id in runs:
            raise ValueError("Replayed evidence or collector run")
        covered.add(pair)
        runs.add(run_id)
        ledger[ref] = (pair,canonical(item["observed"]))

    results, review, used = {}, [], set()
    for task in tasks:
        identifier = task["id"]
        planned = len(protocol[identifier])
        trials = sequence(task["trials"],"trials")
        ids = set(strings([row["id"] for row in trials],"trial ID"))
        if not ids <= protocol[identifier]:
            raise ValueError("Trial is outside the frozen protocol")
        correct, complete = 0, 0
        expected = canonical(task["expected"])
        for row in trials:
            if "observed" in row:
                raise ValueError("Observed state belongs only in the trusted outcome ledger")
            ref = row.get("outcome_ref")
            outcome = None
            if ref is not None:
                string(ref,"outcome reference")
                if ref in used or ref not in ledger or ledger[ref][0] != (identifier,row["id"]):
                    raise ValueError("Unknown, reused or mismatched outcome reference")
                used.add(ref)
                outcome = ledger[ref][1] == expected
                complete += 1
                correct += outcome
            judge = row.get("judge")
            if judge is not None:
                string(judge["grader"],"grader revision")
                if type(judge["pass"]) is not bool:
                    raise ValueError("Judge pass must be boolean")
            review.append({"task_id":identifier,"trial_id":row["id"],"outcome_ref":ref,"objective_pass":outcome,
                           "imported_judge":judge,"judge_disagrees":judge["pass"] != outcome
                           if judge is not None and outcome is not None else None})
        result = {"planned":planned,"complete":complete,"correct":correct,"metrics":None}
        if complete == planned:
            result["metrics"] = summarize(complete,correct,k)
        results[identifier] = result
    measured = [row["metrics"] for row in results.values() if row["metrics"] is not None]
    macro = {key:fmean(m[key] for m in measured) for key in measured[0]} if measured and len(measured)==len(tasks) else None
    return {"k":k,"tasks":results,"macro":macro,"incomplete_tasks":len(tasks)-len(measured),"human_review":review}


if __name__ == "__main__":
    main(analyze, __doc__)
