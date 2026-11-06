# Initial audit — baseline a1708ef

Scope: AAES only; 13 entrypoints, registry, references, portable scripts, host installers and evaluation assets. The independent [AIWorkbench](https://github.com/BielmFranco/AIWorkbench) was reviewed for install UX and packaging conventions. Format follows the [Agent Skills specification](https://agentskills.io/specification). AAES does not include a native host adapter; it consumes structured data and exports portable folders.

Baseline commands: `python scripts/validate.py`, `python evals/score_routing.py`, `python -m unittest discover -s tests -v`. Observed: 13 valid, 64 policy fixtures matched reference selections, 22 unit tests passed. The fixture metric does not cover natural-language activation.

| Skill | Technique | Baseline state and evidence | Limitation / risk | Audit action |
| --- | --- | --- | --- | --- |
| skill-orchestrator | Semantic capability routing | Partial: `route.py` ranks structured classifications | High: named skill may appear to cover an unrelated outcome; fixture labels do not assess host selection | Fix explicit dispatch, reject ambiguous JSON, independently review 64 labels |
| research-orchestrator | Evidence synthesis | Method only: evidence ledger in technical guide | Medium: source mapping and conflicting evidence lack executable checks | Add offline ledger verification |
| adaptive-reasoning | External budget allocation | Implemented decision helper `decide.py` | Medium: advised verification reserve is not checked | Enforce reserved budget; compare against a fixed policy on synthetic workload |
| process-verifier | Evidence gates | Implemented `verify.py` | High: duplicate JSON keys and mismatches at ingestion; provenance external | Reject ambiguous inputs and add positive/negative controls |
| trajectory-analyzer | Trace reconstruction | Implemented `summarize.py` | Medium: corrupt JSON; timing and partial trace scope | Reject ambiguous inputs and test corrupted/synthetic traces |
| long-horizon-executor | Durable checkpoints | Implemented local `checkpoint.py` | High: local transaction cannot cover external effects | Verify restart in separate processes; document reconciliation/fencing |
| multi-agent-router | Dependency and conflict scheduling | Implemented `schedule.py` | Medium: latency estimate does not imply safe or inexpensive execution | Compare serial/parallel schedules on an identical graph and surface cost cap |
| evolutionary-optimizer | Measured variant selection | Partial: `archive.py` selects a Pareto front | Medium: unbounded pairwise work; held-out promotion external | Bound archive and evaluate a controlled toy search |
| runtime-guardian | External authorization | Partial: `policy.py` plus local reservation | High: preflight alone never blocks a credentialed tool | Test denied/rebound/replayed proposals; distinguish reservation and execution |
| hypothesis-lab | Discriminating experiments | Implemented `matrix.py` | Medium: rank is descriptive; correlated evidence and null need care | Validate conflicting evidence and abstention |
| experiment-evaluator | Paired evaluation | Implemented descriptive `compare.py` | Medium: no uncertainty or clustered sampling | Add an optional paired cluster interval |
| mechanistic-interpretability | Activation patching | Partial: `patch_metrics.py` computes measurements | Medium: effect on model weights not exercised | Add a reproducible toy intervention and keep open-model status explicit |
| agentic-rl-lab | Offline returns and tool safety | Partial: `rollouts.py` validates logs and scores outcomes | High if scoring logs controlled by a policy | Exercise reward spoofing and unsafe rollouts; no training |

Distribution finding: existing lifecycle commands were complete but exposed only the generic CLI and wrappers. AAES should offer the same predictable install entrypoints as AIWorkbench and an agent-directed installation procedure, with existing collision and backup guarantees.
