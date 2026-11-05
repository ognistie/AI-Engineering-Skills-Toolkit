# Research basis

Primary source: [Microsoft Research, Agent Lightning](https://arxiv.org/abs/2508.03680).

Agent Lightning separates agent execution and training, with transitions and explicit credit assignment. AAES implements offline outcome accounting and discounted returns on environment-generated logs. It does not implement LightningRL, train a policy, or infer causal credit.
