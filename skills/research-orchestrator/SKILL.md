---
name: research-orchestrator
description: "Investigate technical or scientific questions using primary evidence, competing explanations and verifiable experiments. Use for source-backed research or an offline research plan; do not use for routine lookups."
metadata:
  author: AAES
  version: "0.1.0"
---

# Research Orchestrator

Resolve a technical decision using traceable evidence.

## Procedure

Define the decision, claim boundaries, alternatives, workload, and freshness requirements. Search official docs, papers and public implementations when the host provides permitted access. Read the relevant section of each primary source; distinguish reported result, interpretation, and assumption. Track conflicting findings by population, setup, date, or metric rather than averaging unrelated evidence.

Use the [evidence ledger](references/TECHNICAL_GUIDE.md) to map each consequential claim to a source locator and limitations. Record failed searches that matter. For no-network work, use supplied artifacts and label unverified claims; prepare reproducible queries and local experiments without pretending that retrieval occurred.

Stop when new evidence is unlikely to change the decision within budget, or when a decisive claim depends on unavailable data. When warranted, propose a falsifiable experiment with baseline, input corpus, metric, and reversal threshold.

## Deliverable

Return recommendation, competing claims, supporting and contrary evidence, confidence with reasons, and the smallest experiment that would change the decision.

Example: Compare two architectures for sparse long-running jobs; separate vendor limits from measured behavior on the actual workload.

For more scenarios read [use cases](references/USE_CASES.md). For the scientific basis and limits read [research basis](references/RESEARCH_BASIS.md).
