# Operating contract

Run `python scripts/check.py input.json` from this skill directory (Python 3.12+, standard library). Set `schema_version` to 1. The result is a JSON report; input errors exit 2. A valid report may indicate a failure or an incomplete check. Inspect its decision before taking action.

Pass tools [{name, description, schema, errors}], with errors [{code, action}]. The linter checks object schemas with primitive properties, enum and required fields; nested or advanced schemas need a host validator.

Optional calls [{id, tool, arguments}] test representative calls against this narrow profile. Compare actual tool selection, valid-argument rate, recovery and token counts using the same tasks and model. The report's catalog bytes are a serialization proxy.

Use a fixed baseline and retain the underlying evidence to reproduce the decision.
