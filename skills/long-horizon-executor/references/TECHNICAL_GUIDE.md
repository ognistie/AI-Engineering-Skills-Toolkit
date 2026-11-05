# Technical guide

Example plan:

```json
{
  "run_id": "run-9",
  "steps": [
    {
      "id": "payment",
      "max_attempts": 2
    },
    {
      "id": "receipt",
      "max_attempts": 1
    }
  ]
}
```

Use `python scripts/checkpoint.py init state.db plan.json`, `python scripts/checkpoint.py record state.db event.json` and `python scripts/checkpoint.py status state.db`.

Claim: `{"id":"claim-1","step":"payment","kind":"claim","operation":"p42"}`. Observation: `{"id":"observation-1","step":"payment","kind":"verified","operation":"p42","evidence":"provider:receipt/10"}`. A no-effect observation needs proof that the prior attempt cannot settle later. `abort` blocks progress. Keep the same operation key for a retry. Treat a duplicate event response as an observation, never as permission to dispatch.

Keep SQLite on a trusted local filesystem with one operator protocol. Fence stale workers before resuming or use provider-enforced idempotency. A database transaction does not encompass the remote call; verify the outcome independently. Keep secrets out of event references.
