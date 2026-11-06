---
name: agent-evals-engineer
description: "Build and score structured agent trials against independent end states; export human review and import model grader observations. Use for evaluation harness design; use experiment-evaluator for paired variant statistics."
metadata:
  author: AAES
  version: "0.2.0"
---

# Agent Evals Engineer

Freeze task criteria and repeats; compare a text success claim against trusted final state. Separate capability, regression and adversarial suites. Keep graders outside the candidate write scope, audit transcript samples, and calibrate any imported model judge against human labels. Do not turn absent trials into passes.

Use the [operating contract](references/TECHNICAL_GUIDE.md) for the local helper. If the necessary observations or authority are missing, report the gap and offer the applicable design or verification procedure.

## Completion

Return the decision, evidence IDs or check results, and the limit of what was verified. Read [worked cases](references/USE_CASES.md) for boundaries and [research basis](references/RESEARCH_BASIS.md) for scientific fidelity.
