# Operating contract

Run `python scripts/check.py input.json` from this skill directory (Python 3.12+, standard library). Set `schema_version` to 1. The result is a JSON report; input errors exit 2. A valid report may indicate a failure or an incomplete check. Inspect its decision before taking action.

Pass initial_state, budget, transitions {state:{action:next_state}} and events [{id, seq, action, units}]. Only the accepted prefix contributes to state and spend.

Use a fixed baseline and retain the underlying evidence to reproduce the decision.
