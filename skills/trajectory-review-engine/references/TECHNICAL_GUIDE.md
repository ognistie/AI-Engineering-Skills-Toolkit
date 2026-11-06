# Operating contract

Run `python scripts/check.py input.json` from this skill directory (Python 3.12+, standard library). Set `schema_version` to 1. The result is a JSON report; input errors exit 2. A valid report may indicate a failure or an incomplete check. Inspect its decision before taking action.

Pass events [{id, operation, status, state}] in observed order and optional claimed_success and observed_success booleans. loop_threshold defaults to 3. Optionally pass the trusted trajectory-analyzer output as span_summary; its chronology must match all event IDs, and determines their review order. Do not derive observed state from a tool's text.

The loop window is per operation and observed state. A success for that operation or its changed state clears the prior window; unrelated log reads do not. These patterns identify stall candidates, not causality.

Use a fixed baseline and retain the underlying evidence to reproduce the decision.
