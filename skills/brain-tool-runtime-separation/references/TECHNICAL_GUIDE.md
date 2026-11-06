# Operating contract

Run `python scripts/check.py input.json` from this skill directory (Python 3.12+, standard library). Set `schema_version` to 1. The result is a JSON report; input errors exit 2. A valid report may indicate a failure or an incomplete check. Inspect its decision before taking action.

Pass plan [{id, tool, resource}] and trusted_permissions {tool:[resources]}. The CLI executes inert fake callbacks only; the Python boundary accepts trusted authorization and handler callbacks.

The authorization callback is a side-effect-free preflight. It must check executor-owned metadata, not parameters supplied as authority by the planner. A real handler separately binds the exact effect and atomically consumes authorization or reserves budget immediately before execution. Whole-plan preflight is not transactional execution or a rollback of previous effects.

Use a fixed baseline and retain the underlying evidence to reproduce the decision.
