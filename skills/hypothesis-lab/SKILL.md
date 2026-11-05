---
name: hypothesis-lab
description: "Develop competing technical hypotheses with falsifiable predictions and independent evidence. Use for discriminating experiments or uncertainty after an incident; use source synthesis for literature-only requests."
metadata:
  author: AAES
  version: "0.1.0"
---

# Hypothesis Lab

Rank explanations by discriminating evidence without mistaking consensus for proof.

## Procedure

Write mutually distinguishable mechanisms, including a null hypothesis. For each, name the predicted observations and what would falsify it. Design the smallest intervention whose outcomes separate mechanisms while holding alternatives constant. Record whether evidence is observational or intervention-based and assign correlated rows to one source group.

Use [the evidence matrix](references/TECHNICAL_GUIDE.md) to surface conflicts and avoid counting repeated claims from the same trace or source as independent. Search for contrary evidence and document confounders. Stop when the next experiment cannot change the decision within budget or when the available evidence does not distinguish competing mechanisms.

## Deliverable

Return ranked hypotheses with rationale, contradictions, discriminating test and what would reverse the ranking.

Example: Separate warm-cache behavior from model latency using paired warm/cold runs and the same workload.

Read [use cases](references/USE_CASES.md) to calibrate decisions, and [research basis](references/RESEARCH_BASIS.md) for evidence and limits.
