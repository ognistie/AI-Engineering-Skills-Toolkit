# Technical guide

`python scripts/schedule.py input.json`

```json
{
  "max_agents": 2,
  "overhead_ms": 50,
  "min_gain_ms": 100,
  "host_parallel": true,
  "delegation_authorized": true,
  "tasks": [
    {
      "id": "server",
      "depends_on": [],
      "reads": [
        "baseline"
      ],
      "writes": [
        "server-report"
      ],
      "ms": 900
    },
    {
      "id": "client",
      "depends_on": [],
      "reads": [
        "baseline"
      ],
      "writes": [
        "client-report"
      ],
      "ms": 750
    },
    {
      "id": "merge",
      "depends_on": [
        "server",
        "client"
      ],
      "reads": [
        "server-report",
        "client-report"
      ],
      "writes": [
        "report"
      ],
      "ms": 200
    }
  ]
}
```

Use canonical logical ownership labels. If a parent and child path overlap, assign both the same resource label or model their conflict explicitly. Estimate total coordination overhead including merge, transport and isolation; use null when unknown. The helper greedily batches only ready tasks, with read/write exclusions and a concurrency cap. Independently estimate aggregate cost if the provider charges per worker; speed does not justify exceeding the spend budget.

### Cost and ownership gates

To enforce a modeled cost cap, set every task's `cost_units`, plus `max_cost_units` and `parallel_overhead_cost_units`. The helper excludes parallelism when coordination would exceed the cap; if even sequential work exceeds it, it returns no schedule. With no cost fields, cost remains unverified. The serial estimate sums task durations; the batched estimate sums batch maxima plus coordination. Compare dispatch, merge latency and contradictions against the same tasks before scaling.
