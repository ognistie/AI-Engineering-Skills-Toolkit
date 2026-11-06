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

Claim: `{"id":"claim-1","step":"payment","kind":"claim","operation":"p42"}`. Observation: `{"id":"observation-1","step":"payment","kind":"verified","operation":"p42","claim_id":"claim-1","evidence":"provider:receipt/10"}`. Each observation (`verified`, `no_effect`, or `abort`) must carry the current attempt’s claim event ID, available as `state.active_claim_id` in status. Use a new claim event ID for each retry and keep the same operation key. A no-effect observation needs proof specific to that claim that the attempt cannot settle later. `abort` blocks progress. Treat a duplicate event response as an observation, never as permission to dispatch.

Keep SQLite on a trusted local filesystem with one operator protocol. Fence stale workers before resuming or use provider-enforced idempotency. A database transaction does not encompass the remote call; verify the outcome independently. Keep secrets out of event references.

### Freeze execution scope

Optionally set `scope_sha256` in the initialized plan to the digest of canonical environment, revision, permitted actions and relevant approval scope. Every record must carry the same digest. Compute it from trusted caller state; a matching string from a proposal does not authorize an action. Never switch targets when resuming. An authorized change uses a new plan after reconciling the old in-flight effect. Checkpoint status is a recovery cue, not a lease; fence stale workers externally or use provider idempotency.
