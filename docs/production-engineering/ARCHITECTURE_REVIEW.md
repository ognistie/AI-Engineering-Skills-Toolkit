# Architecture and compatibility

Baseline: AAES commit `3b4b938`; its 37 tests passed before expansion. The [Agent Skills specification](https://agentskills.io/specification) and [AIWorkbench](https://github.com/BielmFranco/AIWorkbench) inform standalone packaging, concise entrypoints, scoped references and local verification.

| Overlap | Boundary |
| --- | --- |
| Harness / repo context | Harness checks operational commands and run evidence. Repo context checks canonical documentation and navigability. |
| ACI / tool discovery | ACI validates one schema and its example arguments. Discovery selects from many authorized contracts under a budget. |
| Existing trajectory analyzer / review engine | Analyzer owns spans, clocks and overlap. Review consumes its chronology and finds failure patterns and state disagreement. |
| Experiment evaluator / agent evals | Experiment evaluator compares variants and clusters; agent evals scores an individual trial suite with an end-state contract. |
| Long-horizon executor / durable engine / context recovery | Original journal owns persistence and claims. Durable engine consumes that status and demonstrates local restart; compaction guards information continuity rather than remote effects. |
| Runtime guardian / capability policy / information flow / monitor | Guardian retains approval and reservation. New tools cover narrowing grants, data provenance, and temporal invariants respectively. The demo executor accepts trusted callbacks at its boundary. |
| Process verifier / runtime monitor | Final evidence gates versus transitions during execution. |
| Evolutionary optimizer / evaluator–optimizer loop | Population search versus bounded refinement of one artifact. |

Existing helpers and output shapes remain intact. The 15 tools use a common JSON contract with version 1 and strict bounded intake. The canonical helper is [tools/production/_contract.py](../../tools/production/_contract.py); packaged copies are byte-identical and tested because each skill must work when installed alone. Trace and journal components reuse existing output contracts.
