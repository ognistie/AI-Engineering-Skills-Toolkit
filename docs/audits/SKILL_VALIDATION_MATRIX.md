# Skill validation matrix

**R** = research-grounded method; **S** = structurally valid; **F** = functionally verified within the stated local scope; **E** = a paired agent pilot exists (historical 13-scenario pilot plus fresh six-scenario audit where applicable). E does not imply a statistically powered study. No skill has been classified **PRODUCTION-READY** by this audit.

| Skill | Gates | Functional evidence | NOT VERIFIED |
| --- | --- | --- | --- |
| skill-orchestrator | R / S / F / E | 64 structured fixtures, independent raw-prompt review, explicit capability regression | Native automatic activation and end-to-end dispatch |
| research-orchestrator | R / S / F / E | Offline ledger detects grouped support, contrary evidence, unsourced claims and inconsistent duplicate locators | Retrieval and fact checking against a live corpus |
| adaptive-reasoning | R / S / F / E | Rejects a branch that consumes mandatory reserve; synthetic fixed-policy comparison | Model quality, paid cost and wall time |
| process-verifier | R / S / F / E | Six fault controls plus forged success, typed mismatch and malformed input tests | Provenance under untrusted executor |
| trajectory-analyzer | R / S / F / E | Synthetic overlap, missing parent, repeated operation, cycle and corrupt JSON | Real trace sample and causal attribution |
| long-horizon-executor | R / S / F / E | Separate-process reopen, reconciliation gate, retry and changed-scope rejection | Provider exactly-once or worker fencing in production |
| multi-agent-router | R / S / F / E | Same graph under serial/batched modes; conflicts, cycles, budget and permission | Model-based parallel execution speedup |
| evolutionary-optimizer | R / S / F / E | Per-repetition caps, Pareto rejection, paired toy search and separate holdout seed | Autonomous search across production workloads |
| runtime-guardian | R / S / F / E | Changed payload, expired approval, policy revision, unknown tool and SQLite race | Real host bypass resistance, identity and credential isolation |
| hypothesis-lab | R / S / F / E | Correlated source counts and controlled contradiction | Hypothesis novelty or empirical discovery benefit |
| experiment-evaluator | R / S / F / E | Missing-pair abstention, timeout gate, task versus trial weighting and cluster reporting guard | Representative model benchmark and real-cost regression |
| mechanistic-interpretability | R / S / F / E | Unclipped normalization, invalid gap exclusion, toy activation intervention and matched control | Pinned model-weight experiment, SAE and circuit identification |
| agentic-rl-lab | R / S / F / E | Return calculation, unsafe episode preservation, malformed transition and spoofed state rejection | Training and cross-family generalization |

Reproduce with `python -m unittest discover -s tests -v` and `python evals/run_controls.py`. See [behavioral evidence](BEHAVIORAL_EVALUATION.md) for pilot limitations.
