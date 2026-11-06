---
name: capability-security-architect
description: "Check exact capability attenuation and proposed access before issuance. Use for least-privilege grants and delegated rights; runtime-guardian owns approval consumption and reservation."
metadata:
  author: AAES
  version: "0.2.0"
---

# Capability Security Architect

Specify subject, delegator, canonical resources, effects and expiry from trusted metadata. Delegate only subsets and prohibit further delegation unless inherited. Check requested resource and tool against the actual grant at execution. Keep issued approvals and trusted clocks outside the model. Validate scope expansion, expiration and mismatched subjects.

Use the [operating contract](references/TECHNICAL_GUIDE.md) for the local helper. If the necessary observations or authority are missing, report the gap and offer the applicable design or verification procedure.

## Completion

Return the decision, evidence IDs or check results, and the limit of what was verified. Read [worked cases](references/USE_CASES.md) for boundaries and [research basis](references/RESEARCH_BASIS.md) for scientific fidelity.
