# Paired comparison

`python scripts/compare.py protocol.json observations.json`

Protocol: `{"id":"p1","trial_ids":["task1-s1"],"gates":{"min_candidate_success":1,"min_success_delta":0,"max_candidate_p95_ms":400,"max_candidate_mean_cost":0.02}}`

Observations: `{"protocol_id":"p1","attempts":[{"variant":"baseline","trial_id":"task1-s1","outcome":"success","latency_ms":390,"cost":0.02},{"variant":"candidate","trial_id":"task1-s1","outcome":"success","latency_ms":310,"cost":0.019}]}`

Record cost in one declared unit per protocol. Latency includes the measured attempt through failure/timeout. Outcomes: success, failure, timeout. Complete pairing is required. p95 uses nearest rank; for small samples, state that it is effectively the maximum. The helper does not compute confidence intervals, run trials or verify source provenance. Use a cluster-aware analysis when tasks have repeated runs. Exit 0 passed, 1 failed/incomplete, 2 invalid input.

### Paired task uncertainty

Optionally add `trial_groups` to the protocol: an exact mapping from every planned trial ID to a task cluster. Each cluster contributes its mean paired success difference, then clusters get equal weight. This differs from the trial-weighted point estimate already reported. With at least eight clusters, the helper adds a 2,000-draw percentile interval resampling entire task effects, with `bootstrap_seed` (default 0). The lower count limit is a reporting guard, not an assurance of valid coverage. Report the estimand and assumptions: independent, representative task clusters and a fixed evaluation protocol. With fewer clusters report the point estimate and no interval. Gates remain tied to the predeclared descriptive fields.
