---
name: evolutionary-optimizer
description: "Search isolated variants using scored trials, hard constraints, and a Pareto archive. Use for iterative algorithm or prompt optimization with a fixed objective; do not apply winners automatically."
metadata:
  author: AAES
  version: "0.1.1"
---

# Evolutionary Optimizer

Explore variants while protecting baselines and the holdout.

## Procedure

Freeze objectives, units, feasible limits, seeds, per-generation budget and held-out protocol. Keep the baseline and experiment workspaces separate. Generate one bounded batch of variants, including a control; record parent, mutation and immutable revision. Run only authorized isolated checks. Reject incomplete or infeasible measurements before ranking.

Use [the archive contract](references/TECHNICAL_GUIDE.md) to retain nondominated development variants. Choose a deployable candidate using an agreed tradeoff, freeze its revision, then use untouched holdout data once for promotion. Compare against the baseline with controlled repeats, not best-of-many anecdotes. Stop on budget, stagnation across batches or inability to reproduce. Applying a variant to the main project is a separate authorized decision.

## Deliverable

Return archive, lineage, rejected variants, frozen candidate, holdout evidence and tradeoffs.

Example: A faster candidate that violates the memory cap is excluded even if it beats every other latency measurement.

Read [use cases](references/USE_CASES.md) to calibrate decisions, and [research basis](references/RESEARCH_BASIS.md) for evidence and limits.
