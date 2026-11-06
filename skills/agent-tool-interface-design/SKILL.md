---
name: agent-tool-interface-design
description: "Design discovery, exposure budgets and composition for large agent tool catalogs. Use when selection or schema overhead dominates; use agent-computer-interface to lint a single tool."
metadata:
  author: AAES
  version: "0.2.0"
---

# Agent Tool Interface Design

Split discovery from argument validation. Restrict candidate tools to the caller's authorized namespace before ranking. Reveal minimal schemas on demand; cap exposure bytes and keep compound tools narrow with explicit transaction and failure semantics. Compare exact selection and real tokens before and after.

Use the [operating contract](references/TECHNICAL_GUIDE.md) for the local helper. If the necessary observations or authority are missing, report the gap and offer the applicable design or verification procedure.

## Completion

Return the decision, evidence IDs or check results, and the limit of what was verified. Read [worked cases](references/USE_CASES.md) for boundaries and [research basis](references/RESEARCH_BASIS.md) for scientific fidelity.
