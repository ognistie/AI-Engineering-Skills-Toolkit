# Operating contract

Run `python scripts/check.py input.json` from this skill directory (Python 3.12+, standard library). Set `schema_version` to 1. The result is a JSON report; input errors exit 2. A valid report may indicate a failure or an incomplete check. Inspect its decision before taking action.

Pass intent, allowed tool IDs, max_tools, max_bytes and catalog [{id, intents, schema}]. Match host-classified intent; authorization is an input, not inferred from descriptions.

Use a fixed baseline and retain the underlying evidence to reproduce the decision.
