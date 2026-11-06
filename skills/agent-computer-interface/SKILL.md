---
name: agent-computer-interface
description: "Lint individual agent tool contracts, parameter schemas and actionable errors. Use when a model miscalls a tool or cannot recover; use tool interface design for discovery across a large catalog."
metadata:
  author: AAES
  version: "0.2.0"
---

# Agent Computer Interface

Start with transcripts of invalid arguments and ambiguities. Prefer narrow names, schema-validated required fields, errors with a concrete recovery action, and responses containing only decision-relevant state. Test valid, invalid and recovery examples with the executor; never infer support for constrained decoding from a JSON Schema.

Use the [operating contract](references/TECHNICAL_GUIDE.md) for the local helper. If the necessary observations or authority are missing, report the gap and offer the applicable design or verification procedure.

## Completion

Return the decision, evidence IDs or check results, and the limit of what was verified. Read [worked cases](references/USE_CASES.md) for boundaries and [research basis](references/RESEARCH_BASIS.md) for scientific fidelity.
