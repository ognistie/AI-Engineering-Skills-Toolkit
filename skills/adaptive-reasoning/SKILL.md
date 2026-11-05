---
name: adaptive-reasoning
description: "Choose how much external work an AI workflow needs using evidence, difficulty, and fixed budgets. Use for verifier-guided escalation, stopping rules, or allocating attempts; this does not control hidden model reasoning."
metadata:
  author: AAES
  version: "0.1.0"
---

# Adaptive Reasoning

Allocate external attempts where they can change the outcome.

## Procedure

Choose the smallest viable first attempt. Pin time, money and attempt caps, and record a success test before spending more. Classify only observed signals: a trusted gate passed, an actionable uncertainty remains, or independent checks disagree. Escalate only when you can name the next observation, its cost and a decision it could change. Stop on verified success, exhausted budgets, repetition without new evidence, or a decision requiring authority you do not have.

Use [the budget contract](references/TECHNICAL_GUIDE.md) to select a direct attempt, verification or escalation. Freeze budgets before the run and reserve verification cost if it is mandatory. Escalation means collecting an observable artifact, changing the method or requesting expertise; it does not imply access to a closed model's internal computation.

## Deliverable

Return mode, measured spend, remaining budget, next action, verification and stopping reason.

Example: After a generated migration fails an invariant twice with no new evidence, stop retrying the same prompt and report the unresolved invariant.

Read [use cases](references/USE_CASES.md) to calibrate decisions, and [research basis](references/RESEARCH_BASIS.md) for evidence and limits.
