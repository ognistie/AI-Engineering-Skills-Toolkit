---
name: multi-agent-router
description: "Choose whether and how to delegate independent agent work with dependency, ownership, latency and cost constraints. Use for agent topology and task decomposition; do not delegate a simple linear task."
metadata:
  author: AAES
  version: "0.1.0"
---

# Multi Agent Router

Select a topology that can beat sequential work without violating ownership.

## Procedure

Start with a single-agent baseline. Specify each work unit's inputs, output contract, dependencies, read/write ownership, expected duration, and merge owner. Use the [topology guide](references/TECHNICAL_GUIDE.md) to compare sequential work with compatible batches. Use supplied estimates and measured coordination cost where available; report the source and uncertainty. A shared state writer blocks parallel work with another reader or writer of that resource.

A topology proposal does not grant delegation. Dispatch only when the host supports it and the user authorized it. Give workers least-privilege access and acceptance criteria. The merge owner resolves contradictions using evidence instead of majority vote. Stop adding agents when predicted savings disappear, access is missing, or the dependency graph is invalid.

## Deliverable

Return topology, ordered batches, ownership, merge check, estimated savings and actual dispatch status.

Example: Two reviewers on independent read-only slices can run together; keep migrations against the same schema serialized.

Read [use cases](references/USE_CASES.md) to calibrate decisions, and [research basis](references/RESEARCH_BASIS.md) for evidence and limits.
