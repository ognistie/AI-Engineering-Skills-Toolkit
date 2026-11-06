# Operating contract

Run `python scripts/check.py input.json` from this skill directory (Python 3.12+, standard library). Set `schema_version` to 1. The result is a JSON report; input errors exit 2. A valid report may indicate a failure or an incomplete check. Inspect its decision before taking action.

Use root, revision, and commands [{id, path, receipt?}] in the audit. A receipt must contain revision and integer exit_code. Paths are repository-relative; the script checks presence and never executes a command.

Use a fixed baseline and retain the underlying evidence to reproduce the decision.
