---
name: trajectory-review-engine
description: "Review chronological agent events for invalid calls, stalled loops and disagreement with authoritative outcomes. Use for trajectory failure triage; use trajectory-analyzer for span timing and parentage."
metadata:
  author: AAES
  version: "0.2.0"
---

# Trajectory Review Engine

Start from an independently observed result and ordered event IDs. Use the existing trajectory-analyzer for span timing. Distinguish intentional retries that make progress from repeated failures on the same operation and unchanged state. Record the earliest discriminating observation and plan a controlled replay before assigning cause.

Use the [operating contract](references/TECHNICAL_GUIDE.md) for the local helper. If the necessary observations or authority are missing, report the gap and offer the applicable design or verification procedure.

## Completion

Return the decision, evidence IDs or check results, and the limit of what was verified. Read [worked cases](references/USE_CASES.md) for boundaries and [research basis](references/RESEARCH_BASIS.md) for scientific fidelity.
