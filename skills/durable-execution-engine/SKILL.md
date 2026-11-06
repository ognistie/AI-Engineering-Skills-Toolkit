---
name: durable-execution-engine
description: "Choose bounded retry, reconciliation and compensation from a persisted execution snapshot. Use for external effects and crash recovery architecture; long-horizon-executor owns the transactional journal."
metadata:
  author: AAES
  version: "0.2.0"
---

# Durable Execution Engine

Use long-horizon-executor's SQLite checkpoint for local persistence. Reconcile in-flight operations before retrying; preserve the operation key and active claim ID. Retry only known no-effect failures under attempts and elapsed limits. A compensation is a distinct authorized and idempotent operation. Temporal is optional: map effects to activities, define timeout and retry policies, and verify replay with a crash at each boundary.

Use the [operating contract](references/TECHNICAL_GUIDE.md) for the local helper. If the necessary observations or authority are missing, report the gap and offer the applicable design or verification procedure.

## Completion

Return the decision, evidence IDs or check results, and the limit of what was verified. Read [worked cases](references/USE_CASES.md) for boundaries and [research basis](references/RESEARCH_BASIS.md) for scientific fidelity.
