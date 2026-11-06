---
name: trajectory-analyzer
description: "Analyze AI agent traces or logs to reconstruct tool calls, failures, retries, and latency. Use for debugging a recorded execution or designing a counterfactual; do not use for internal neural activations."
metadata:
  author: AAES
  version: "0.1.1"
---

# Trajectory Analyzer

Find where a recorded workflow diverged and what evidence would isolate the cause.

## Procedure

Start from a trace ID and an observable expected outcome. Reconstruct parentage, chronological spans and operation IDs; reconcile timeouts and tool responses with independently observed state. Flag missing parents, partial sampling and clock offsets before making timing claims.

Separate symptom, first observed divergence, plausible mechanism, and falsification experiment. Count repeated operations and interval overlap before inferring a serial bottleneck; wall time and cumulative work differ. Group retries using explicit operation identity, never just repeated tool names. Keep secrets and raw prompts out of handoffs; share stable event IDs instead.

Use [the normalized trace contract](references/TECHNICAL_GUIDE.md) and optional `scripts/summarize.py` on sanitized data. Tool failures may be expected fallbacks; a successful status need not imply state changed. Stop when the evidence supports a bounded conclusion or specify the missing span, state check, or controlled replay.

## Deliverable

Return chronology, observed failures/retries, latency with measurement scope, alternative explanations, and a counterfactual replay plan. Never present correlation as causation.

Example: Two timeouts share an operation ID: check persisted effect before replay; overlapping spans are not two serial delays.

For more scenarios read [use cases](references/USE_CASES.md). For the scientific basis and limits read [research basis](references/RESEARCH_BASIS.md).
