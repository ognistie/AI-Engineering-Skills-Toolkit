# Operating contract

Run `python scripts/check.py input.json` from this skill directory (Python 3.12+, standard library). Set `schema_version` to 1. The result is a JSON report; input errors exit 2. A valid report may indicate a failure or an incomplete check. Inspect its decision before taking action.

Pass root, revision and documents [{path, topic, observed_revision?}]. The checker handles inline links with optional titles (including a title on the next line) and angle-bracket destinations. Fenced examples and external links are skipped. Reference definitions, nested-parenthesis destinations and fragment existence are outside the supported subset. Stale means an explicit observed revision differs.

Use a fixed baseline and retain the underlying evidence to reproduce the decision.
