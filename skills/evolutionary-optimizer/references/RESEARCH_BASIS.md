# Research basis

Primary source: [Google DeepMind, AlphaEvolve](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/).

AlphaEvolve combines candidate generation with automated evaluation in an evolutionary loop. AAES implements the measured-selection component: complete repeated development measurements, feasibility and a Pareto frontier. It does not generate code autonomously, run untrusted variants, or replicate published results.

## Applicability and failure boundary

The reported engineering wins in AlphaEvolve use executable evaluators and specialized search infrastructure. AAES covers the evaluator and bounded selection pattern; optimization can still overfit evaluator bugs or miss alternatives outside the candidate set.
