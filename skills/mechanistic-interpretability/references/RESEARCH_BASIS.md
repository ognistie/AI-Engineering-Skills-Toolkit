# Research basis

Primary source: [Zhang and Nanda, Activation patching methods](https://arxiv.org/abs/2309.16042).

The study shows that metric and corruption choices can change patching results. AAES implements normalized restoration with paired controls and a baseline-gap guard. Access to model weights and valid interventions remains an external prerequisite.

## Applicability and failure boundary

The study finds that choices such as corruption and metric can change which components look important. A causal intervention on one controlled example is weaker than a stable circuit claim over held-out prompts.
