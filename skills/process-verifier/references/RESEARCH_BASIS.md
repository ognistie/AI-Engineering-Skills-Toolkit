# Research basis

Primary reference: [Agent evaluation of observable outcomes](https://www.anthropic.com/research/demystifying-evals-for-ai-agents).

Anthropic distinguishes the recorded interaction from the actual state outcome in its engineering practice. Apply that distinction by checking fixed gates against independent observations. AAES implements an offline equality checker and evidence status; it does not train a process reward model or authenticate observations.
