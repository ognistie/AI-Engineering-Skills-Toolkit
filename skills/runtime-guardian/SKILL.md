---
name: runtime-guardian
description: "Design and test an external policy gate for AI tool actions. Use for action authorization, scope checks, approvals, replay resistance, or audit records; skill text is not a security barrier."
metadata:
  author: AAES
  version: "0.1.0"
---

# Runtime Guardian

Make execution authority an external, testable boundary.

## Procedure

Enumerate supported actions and exact resource identifiers. Derive effect class from a trusted tool registry, never from model text or tool payloads. Bind each approval to the specific proposal, budget and expiration, and make it single use. Deny unknown actions, unknown scopes and unsafe effects even if the model labels them read-only. Recheck authorization and reserve budget atomically at the executor boundary; a preflight result is not a reusable capability.

Use [the policy contract](references/TECHNICAL_GUIDE.md) to simulate allow/deny/approval decisions. In production, enforce in a wrapper with exclusive tool credentials and independent audit. Bound calls with host timeouts and quotas. Log request IDs and reasons without raw arguments or secrets. Stop on ambiguous classification, unavailable enforcement, stale approval or a denied decision.

## Deliverable

Return policy decision, rule, required approval and a test demonstrating the executor cannot bypass the gate.

Example: An approval to publish artifact A cannot be reused to publish artifact B.

Read [use cases](references/USE_CASES.md) to calibrate decisions, and [research basis](references/RESEARCH_BASIS.md) for evidence and limits.
