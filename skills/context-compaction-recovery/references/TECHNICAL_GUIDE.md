# Operating contract

Run `python scripts/check.py input.json` from this skill directory (Python 3.12+, standard library). Set `schema_version` to 1. The result is a JSON report; input errors exit 2. A valid report may indicate a failure or an incomplete check. Inspect its decision before taking action.

Pass original and restored checkpoints (schema_version, objective, constraints, state, decisions, artifacts, evidence, next_actions, errors); optional root verifies artifact paths and SHA-256 values.

Use a fixed baseline and retain the underlying evidence to reproduce the decision.
