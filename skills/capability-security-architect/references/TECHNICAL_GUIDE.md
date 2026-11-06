# Operating contract

Run `python scripts/check.py input.json` from this skill directory (Python 3.12+, standard library). Set `schema_version` to 1. The result is a JSON report; input errors exit 2. A valid report may indicate a failure or an incomplete check. Inspect its decision before taking action.

Pass parent and child grants with subject, tools, resources, effects, expires, delegable; child requires issuer. Supply now from a trusted clock. Optional request validates exact use of the child grant.

A grant describes a Cartesian product of listed tools, resources, and effects. Use separate grants if only particular combinations are allowed and still enforce the registered tool effect at dispatch.

Use a fixed baseline and retain the underlying evidence to reproduce the decision.
