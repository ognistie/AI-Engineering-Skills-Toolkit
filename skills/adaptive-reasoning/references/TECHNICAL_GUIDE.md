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

### Allocation boundary

For each resource r, enforce spent[r] + proposed[r] + reserve[r] <= cap[r] for non-verification actions. Set optional `verification_reserve` to the required cost of the next mandatory verification. Explicitly mark the independent check `next_kind: "verify"` and name its observable result in `next_observation`; then it may spend the reserved units. A rejected alternative is not a rejected verification. If the evidence is still ambiguous after the affordable check, return the unresolved claim and do not retry an identical operation.

Compare with a frozen always-verify or fixed-attempt baseline over the same tasks. Measure actual quality separately from budget accounting; any synthetic operation prices or latencies are illustrative.
