---
name: runtime-verification-engine
description: "Evaluate deterministic runtime state transitions, sequence IDs and budget invariants before an action advances. Use for live monitor design or audit replay; use process-verifier for final evidence."
metadata:
  author: AAES
  version: "0.2.0"
---

# Runtime Verification Engine

Define permitted transitions and invariant limits before running. Reject replayed IDs, sequence gaps, unknown transitions and exhausted budget. A preflight must not mutate persistent state; atomically persist approved transition and effect receipt at the proper executor boundary. Use reconciliation after ambiguous effects.

Use the [operating contract](references/TECHNICAL_GUIDE.md) for the local helper. If the necessary observations or authority are missing, report the gap and offer the applicable design or verification procedure.

## Completion

Return the decision, evidence IDs or check results, and the limit of what was verified. Read [worked cases](references/USE_CASES.md) for boundaries and [research basis](references/RESEARCH_BASIS.md) for scientific fidelity.
