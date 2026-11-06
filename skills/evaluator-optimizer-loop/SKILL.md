---
name: evaluator-optimizer-loop
description: "Control iterative revision of one artifact with a frozen rubric, independent verifier, bounded cost and stopping criteria. Use for evaluator–optimizer loops; use evolutionary-optimizer for population search."
metadata:
  author: AAES
  version: "0.2.0"
---

# Evaluator Optimizer Loop

Freeze rubric revision, hard gates, target score and budget. Give the revision step specific feedback from an external grader; preserve the last verified artifact. Stop if verification rejects candidates, improvement stalls, the artifact repeats, or another attempt cannot fit. Compare with single-pass quality and attempted cost before deploying.

Use the [operating contract](references/TECHNICAL_GUIDE.md) for the local helper. If the necessary observations or authority are missing, report the gap and offer the applicable design or verification procedure.

## Completion

Return the decision, evidence IDs or check results, and the limit of what was verified. Read [worked cases](references/USE_CASES.md) for boundaries and [research basis](references/RESEARCH_BASIS.md) for scientific fidelity.
