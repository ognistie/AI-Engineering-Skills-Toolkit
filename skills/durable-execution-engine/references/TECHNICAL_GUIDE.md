# Operating contract

Run `python scripts/check.py input.json` from this skill directory (Python 3.12+, standard library). Set `schema_version` to 1. The result is a JSON report; input errors exit 2. A valid report may indicate a failure or an incomplete check. Inspect its decision before taking action.

Pass a checkpoint status response as journal, plus max_attempts, elapsed_ms, deadline_ms, base_delay_ms and max_delay_ms. Optional compensation requires authorized=true and a distinct operation ID; output is a recommendation.

For a local-only demonstration run `python scripts/demo.py scratch --journal-helper PATH --interrupt after-effect`, then repeat without the interrupt flag. PATH must be the reviewed `long-horizon-executor/scripts/checkpoint.py`; the demo loads its Python code. Use a fresh scratch directory on a local filesystem. A SQLite lock is held across claim, effect and reconciliation, and a competing demo invocation is refused before it touches the journal. Process exit releases the lock. This protects cooperating local invocations and does not provide distributed fencing or control over another writer bypassing the demo.

The second run observes a separate SQLite ledger and reconciles without replaying the effect. To test interruption before the effect, use a different scratch directory with `before-effect`; the next run reconciles absence, and a subsequent run can claim the next attempt.

Use a fixed baseline and retain the underlying evidence to reproduce the decision.
