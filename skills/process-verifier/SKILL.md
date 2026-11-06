---
name: process-verifier
description: "Verify an AI or engineering workflow against checkpoints and independent evidence. Use for acceptance gates, audit trails, unsupported completion claims, or verifier design; use experiment evaluation for baseline comparisons."
metadata:
  author: AAES
  version: "0.1.1"
---

# Process Verifier

Decide whether a workflow met fixed acceptance gates.

## Procedure

Before inspecting outputs, pin the revision, initial state, checkpoints, required final state, and unacceptable outcomes. For each hard gate name an independent observation and what would falsify the result. Check evidence provenance, coverage and freshness; same-run IDs and a reviewer-controlled observation matter more than a well-formed claim.

Compare observations to the contract in [the verification guide](references/TECHNICAL_GUIDE.md). With authorized tools, read final state or run the smallest deterministic check that could fail. Distinguish failed from unavailable or disputed evidence. When scoring a generator, keep grader and fixtures outside the generator's write scope; test a superficially plausible artifact that lacks the real outcome. Do not rerun until green or move thresholds after seeing results.

The optional `scripts/verify.py` compares a contract with pre-collected trusted observations. It never runs candidate code or establishes provenance by itself. Stop when every hard gate has a disposition or the remaining gate requires access, permission, or unavailable evidence.

## Deliverable

Return gate, status, observation ID, evidence gap, and overall disposition. A skipped gate cannot yield a pass.

Example: A refund tool timed out: verify the ledger and provider record before treating it as a failure or attempting a retry.

For more scenarios read [use cases](references/USE_CASES.md). For the scientific basis and limits read [research basis](references/RESEARCH_BASIS.md).
