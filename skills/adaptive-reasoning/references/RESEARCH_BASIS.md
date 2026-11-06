# Research basis

Primary source: [Snell et al., Optimizing test-time compute](https://arxiv.org/abs/2408.03314).

The paper reports gains from allocating computation by problem difficulty in its experimental setup. This skill adapts the allocation idea to external actions using fixed budgets and observable checks. The helper does not schedule model internals, reproduce the paper, or predict a gain on arbitrary tasks.

## Applicability and failure boundary

Difficulty estimates can be wrong, and a weak verifier can reward polished failures. Allocate from observable uncertainty and validate independently before claiming success.
