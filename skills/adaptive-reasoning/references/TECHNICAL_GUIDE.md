# Technical guide

`python scripts/decide.py input.json`

```json
{
  "evidence": "disagreement",
  "limit": {
    "attempts": 3,
    "ms": 800,
    "cost_units": 12
  },
  "spent": {
    "attempts": 1,
    "ms": 200,
    "cost_units": 4
  },
  "next_cost": {
    "attempts": 1,
    "ms": 100,
    "cost_units": 2
  },
  "authorized": true,
  "next_observation": "Query the migration ledger"
}
```

Use the same units and counter source in limit, spent and next_cost. Evidence values: not_started, uncertain, disagreement, verified, stalled, blocked. Reserve cost and time at the caller before executing the proposed action. `verified` is permitted only from a trusted acceptance gate. The helper returns a recommendation; it cannot meter time or enforce a host budget.
