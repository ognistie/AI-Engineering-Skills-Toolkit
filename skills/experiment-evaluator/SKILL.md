---
name: experiment-evaluator
description: "Plan or analyze paired baseline versus candidate experiments for AI models, agents, or engineering workflows. Use for repeated trials, regression gates, held-out datasets, and quality, latency or cost comparisons."
metadata:
  author: AAES
  version: "0.1.1"
---

# Experiment Evaluator

Compare alternatives under a frozen protocol and report uncertainty.

## Procedure

Lock the task sample, assignment or pairing unit, seeds, budgets, graders, slices, and decision thresholds before running. Pair on workload and trial key; balance run order or use independent equivalent environments. Record failures, timeouts and missing observations separately. Compare total cost per attempted task alongside success and tail latency.

Keep held-out data and grader keys outside tuning. Calibrate graders with invalid, valid, and alternative-correct artifacts. If a judge sees model outputs, blind variant labels and inspect disagreements; keep human criteria separate from executable checks. Report numerator and denominator, effects per meaningful slice, and uncertainty at the task or cluster level rather than assuming repeated seeds are independent.

The offline helper in [the comparison guide](references/TECHNICAL_GUIDE.md) computes paired descriptive metrics, fixed gates and an optional task-cluster interval. Do not claim superiority from a small or unrepresentative sample. Stop at the frozen trial budget; declare incomplete data instead of silently dropping unpaired or timed-out trials.

## Deliverable

Return protocol ID, trial coverage, quality/latency/cost deltas, gate status, uncertainty or limitations, and release recommendation.

Example: Compare two RAG configurations on identical tasks and seeds; a faster candidate that fails the quality floor does not pass.

For more scenarios read [use cases](references/USE_CASES.md). For the scientific basis and limits read [research basis](references/RESEARCH_BASIS.md).
