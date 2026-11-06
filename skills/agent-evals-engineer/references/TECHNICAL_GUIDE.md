# Operating contract

Run `python scripts/check.py input.json` from this skill directory (Python 3.12+, standard library). Set `schema_version` to 1. The result is a JSON report; input errors exit 2. A valid report may indicate a failure or an incomplete check. Inspect its decision before taking action.

Pass `k` and `tasks` [{id, expected, planned_trial_ids, trials:[{id, outcome_ref?, judge?}]}]. Freeze `planned_trial_ids` before any run. Supply a separate `trusted_outcomes` object keyed by evidence reference; each value contains {task_id,trial_id,run_id,observed}. Every reference must match its planned task/trial pair; collector run IDs, outcome references and observed pairs cannot be reused. Trials without a reference remain incomplete. Candidate-authored observed state in trials is invalid. Optional model judgments are diagnostic, and human review output includes IDs and references.

Migrate old fixtures by collecting the final state outside the candidate write scope and moving it to the trusted ledger with its real collector run ID. Do not generate run IDs solely to relabel one reused observation. This checker detects protocol mismatches, not a forged collector; restrict access to trusted input and record provenance at collection.

Import a model grading record as judge {grader, pass} from the pinned provider and rubric in your adapter; the local runner makes no API call. Keep the export blind to arm identity when calibrating humans. For n observed trials with c correct, pass@k is 1 - C(n-c,k)/C(n,k), and pass^k is C(c,k)/C(n,k). These are finite observed-set estimates without replacement; do not extrapolate to deployment reliability. Incomplete tasks suppress the macro estimate.

Use a fixed baseline and retain the underlying evidence to reproduce the decision.
