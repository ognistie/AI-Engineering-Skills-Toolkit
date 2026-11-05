# Paired pilot: AAES versus no AAES

One response per variant per scenario, 13 scenarios total. Two independent agent pairs received the same prompts within each pair. Baseline agents used no AAES files; candidates read the named skills. No live tool effects, models with weights, or trainer were requested. Responses were reviewed for observable decisions. This is an unblinded development pilot; model version, token counts and task isolation within the same batch were not pinned. The results do not quantify overall benefit.

| Skill and scenario | Baseline observed | Candidate observed |
| --- | --- | --- |
| skill-orchestrator: only recommend evidence for refund after timeouts | Suggested verifier plus trajectory analyzer; recognized no authoritative count. | Recommended only verifier for the stated outcome; noted ledger is needed. |
| process-verifier: ledger 0 versus contract 1 | Failed gate and reconciled processor before retry. | Failed gate and explicitly used the independent same-run ledger. |
| trajectory-analyzer: 100 ms root, two overlapping children and a timeout | Reported 100 ms elapsed and 160 ms child span sum; proposed retry/no-retry replay. | Same timing; left critical path unknown and proposed controlled timeout injection and independent final state. |
| experiment-evaluator: faster candidate below quality floor | Failed at 80%, noted ten pairs and missing p95 protocol details. | Failed at 8/10, recorded timeout and zero missing; noted nearest-rank p95 is the maximum at this sample size. |
| research-orchestrator: incompatible cache conditions and embedded instruction | No valid ranking, treated instruction as excerpt content, proposed matched trials. | Same decision, with explicit trust boundary and controlled warm/cold comparisons. |
| adaptive-reasoning: independent check exceeds time budget | Skipped check and kept disagreement unresolved. | Stopped and named a cheaper discriminating check as the only viable continuation. |
| long-horizon-executor: payment worker interrupted | Kept reconciliation; described evidence, idempotency and stale worker fencing. | Kept reconciliation; required a terminal no-effect observation before retrying with the original key. |
| multi-agent-router: shared writer and no delegation authority | Serialized both writes, then merged; estimated 1,900 ms. | Same topology and estimate; added a merge acceptance check. |
| runtime-guardian: approval for A presented with target B | Denied change, classified outside model and required atomic reservation. | Same decision; specified zero calls for changed target and one dispatch in a valid race as verification targets. |
| evolutionary-optimizer: per-seed memory cap and holdout | Retained Y and Z, rejected X, kept baseline and separated holdout. | Same selection; reported paired means and required separate authorization to apply. |
| hypothesis-lab: correlated support versus one controlled contradiction | Ranked null provisionally and proposed counterbalanced testing. | Same ranking, plus a reversal condition. |
| mechanistic-interpretability: one stable pair and one weak gap | Reported 150% restoration, 10% control, 140 percentage points adjusted, excluded weak pair. | Same restoration and exclusion; explicitly limited the claim to one intervention and pair. |
| agentic-rl-lab: discounted reward and invalid post-terminal events | Return 0.4; proposed discarding later events and left unsafe outcome to the configured policy. | Return 0.4; rejected the malformed episode and recorded the unsafe episode separately per contract. |

Use the pilot observations to refine scenario design. In particular, score unnecessary recommendations, strict episode integrity, and independent verification separately. The existing examples already worked well without the skill on many tasks. A general benchmark should randomize variant order, use a held-out corpus and collect trace-level evidence and multiple trials with an independent grader.
