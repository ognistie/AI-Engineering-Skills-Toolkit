# Research basis

Primary reference: [Trial-based evaluation of agent outcomes](https://www.anthropic.com/research/demystifying-evals-for-ai-agents).

Anthropic documents tasks, repeated trials, graders and outcomes for variable agents. The AAES helper consumes paired attempts, counts timeouts in the denominator and applies prespecified gates. It computes descriptive statistics; uncertainty, bias, task clustering and sample design still require analysis.

## Applicability and failure boundary

Repeated seeds on one task are not additional independent tasks. The optional bootstrap quantifies sample variation over supplied task clusters only; it cannot repair selection bias, grader error, leakage or correlated task families.
