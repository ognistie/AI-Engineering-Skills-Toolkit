# Research basis

Primary reference: [Agent evaluation of observable outcomes](https://www.anthropic.com/research/demystifying-evals-for-ai-agents).

Anthropic distinguishes the recorded interaction from the actual state outcome in its engineering practice. Apply that distinction by checking fixed gates against independent observations. AAES implements an offline equality checker and evidence status; it does not train a process reward model or authenticate observations.

## Applicability and failure boundary

OpenAI's [Let's Verify Step by Step](https://cdn.openai.com/improving-mathematical-reasoning-with-process-supervision/Lets_Verify_Step_by_Step.pdf) studies step-level supervision for mathematical reasoning. A run-scoped gate borrows intermediate checking but does not implement a process reward model. The source key cannot establish authenticity.
