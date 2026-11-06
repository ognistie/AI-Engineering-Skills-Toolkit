---
name: kv-cache-aware-context
description: "Compare serialized context prefixes and provider cache telemetry. Use for KV cache reuse, tool ordering and prefix stability; use compaction recovery for resuming after context loss."
metadata:
  author: AAES
  version: "0.2.0"
---

# KV Cache Aware Context

Pin model, tokenizer, prompt template, region and request shape. Move timestamps and changing identifiers after stable content if instruction precedence permits. Preserve ordering of arrays, including tool lists; measure the cost of tool masking only where the host supports it. Compare paired cold and warm requests at the same lengths and concurrency, recording cached tokens, TTFT and actual billed units.

Use the [operating contract](references/TECHNICAL_GUIDE.md) for the local helper. If the necessary observations or authority are missing, report the gap and offer the applicable design or verification procedure.

## Completion

Return the decision, evidence IDs or check results, and the limit of what was verified. Read [worked cases](references/USE_CASES.md) for boundaries and [research basis](references/RESEARCH_BASIS.md) for scientific fidelity.
