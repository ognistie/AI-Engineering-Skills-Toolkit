---
name: brain-tool-runtime-separation
description: "Validate typed model proposals against a trusted executor and run a fake-tool demonstration. Use for planner/executor integration; use runtime-guardian for the existing approval ledger."
metadata:
  author: AAES
  version: "0.2.0"
---

# Brain Tool Runtime Separation

Keep credentials and effect classification outside model output. Parse an exact proposal schema, bind approved actions to canonical resources, then authorize through runtime-guardian or the host. Fail closed before effects if any action is unknown; use a monitor for phase and resource checks. Journal receipts and reconcile external failures.

Use the [operating contract](references/TECHNICAL_GUIDE.md) for the local helper. If the necessary observations or authority are missing, report the gap and offer the applicable design or verification procedure.

## Completion

Return the decision, evidence IDs or check results, and the limit of what was verified. Read [worked cases](references/USE_CASES.md) for boundaries and [research basis](references/RESEARCH_BASIS.md) for scientific fidelity.
