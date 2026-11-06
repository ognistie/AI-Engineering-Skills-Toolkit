# Research basis

Primary source: [Anthropic, Building effective agents](https://www.anthropic.com/research/building-effective-agents).

Anthropic documents parallelization and orchestrator-workers as useful patterns under different task structures. AAES implements an offline scheduling heuristic with conflict checks and overhead estimates. The result is not an optimal schedule or a measured speedup.

## Applicability and failure boundary

Parallelization only helps when compatible work can overlap and overhead is sufficiently small. The greedy batch order does not optimize globally and gives no empirical claim about model quality.
