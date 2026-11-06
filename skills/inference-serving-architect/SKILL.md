---
name: inference-serving-architect
description: "Estimate self-hosted LLM serving memory and design comparable prefill/decode experiments. Use for batching, KV routing, offload and worker sizing; do not use for hosted prompt-only tuning."
metadata:
  author: AAES
  version: "0.2.0"
---

# Inference Serving Architect

Compare colocated first, then remote prefill when prefill interferes with decode tails or independently sized pools could help. Account for weights, runtime reserve, per-device sharding, allocator pages and transfer bandwidth; monitor queues, GPU utilization, TTFT, intertoken latency and request goodput under equal offered load.

Use the [operating contract](references/TECHNICAL_GUIDE.md) for the local helper. If the necessary observations or authority are missing, report the gap and offer the applicable design or verification procedure.

## Completion

Return the decision, evidence IDs or check results, and the limit of what was verified. Read [worked cases](references/USE_CASES.md) for boundaries and [research basis](references/RESEARCH_BASIS.md) for scientific fidelity.
