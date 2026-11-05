---
name: long-horizon-executor
description: "Plan and resume multi-stage engineering work using verified milestones, durable checkpoints and bounded recovery. Use for interrupted runs or replay-safe workflows, not a one-off task."
metadata:
  author: AAES
  version: "0.1.0"
---

# Long Horizon Executor

Resume from verified state without replaying an uncertain side effect.

## Procedure

Define ordered milestones, independent completion evidence, maximum attempts, idempotency keys, and scope before starting. Persist the claim before acting and the observed result after acting. If interrupted between them, reconcile external state by the recorded operation ID before retrying. Do not infer failure from a timeout, replay a completed milestone, or invent evidence for a transition.

Use [the checkpoint protocol](references/TECHNICAL_GUIDE.md) for local state. A recovery operator owns reconciliation; an uncertain result pauses the dependent action. Advance only after verified evidence, and distinguish a process crash, a retryable no-effect result and exhausted attempts. Without writable persistence, deliver the plan and checkpoint schema without claiming automatic resume.

## Deliverable

Return the verified milestone, next permitted state transition, attempts remaining, and any reconciliation required.

Example: A migration worker died after calling an external service; verify the operation before requesting another claim.

Read [use cases](references/USE_CASES.md) to calibrate decisions, and [research basis](references/RESEARCH_BASIS.md) for evidence and limits.
