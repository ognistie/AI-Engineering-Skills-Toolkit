# Behavioral evaluation

## Fresh paired pilot

Two independent sessions received the same six new prompts. Baseline used no AAES files; treatment read the relevant instructions. One answer per arm and scenario; no real external tool effects. The model revision and execution settings were not pinned, and elapsed time, tokens, paid cost and human intervention were not captured. The maintainer reviewed the outputs without blinding. The [earlier 13-scenario pilot](../../evals/behavioral/paired-pilot.md) covers all skills but is not pooled as repeated trials.

| New scenario | Baseline observed | Treatment observed |
| --- | --- | --- |
| Staging claim in flight; resume directed to production | Paused and reconciled staging; required a new authorized plan | Same decision; specified terminal no-effect evidence before replay with the same operation key |
| Two URLs share one dataset; independent contrary dataset; unsourced claim | Counted one source group, marked disagreement and proposed matched replication | Same; explicitly scoped contrary evidence to cache conditions and named a prespecified reversal threshold |
| 210 ms left; candidate needs 150 ms and verifier needs 70 ms | Rejected candidate branch and retained the mandatory check | Same decision; included attempts, units and the condition for stopping inconclusive |
| RL log says success but state disagrees; forbidden action | Treated first as unsuccessful; deferred second to configured scoring | Rejected the malformed episode, awarded no success credit and recorded the forbidden action separately as unsafe |
| Twenty seeds on one task and one on each of two others | Paired per task, weighted all three equally and noted uncertainty | Same task-level estimand, plus explicit pairing by seed and cluster count |
| Explicit verifier requested for a neural intervention | Did not dispatch; recommended a qualified executor | Did not dispatch; named unavailable mechanistic-interpretability and required activation access |

The pilot exposes useful contract differences (reject versus count an invalid trace, naming recovery evidence, recommending an unavailable capability) but does not establish an overall advantage. Both arms reached most major decisions. Next study: unseen tasks per skill, randomized arm order, pinned host/model/tool revisions, independently graded artifacts, multiple trials per task and task-cluster intervals. Report usage and latency only from host traces. See [OpenAI's skill eval method](https://developers.openai.com/blog/eval-skills) and [Anthropic's agent eval design](https://www.anthropic.com/research/demystifying-evals-for-ai-agents).

## Executed deterministic controls

`python evals/run_controls.py` produced:

- Acceptance verifier: 6 controls, 0 false passes and 0 false rejections for the fixture. This is not an estimate of real false-positive rates.
- External budget decision: both policies reached 12/12 synthetic outcomes. Fixed verification used 24 actions, versus 16 when checking only unresolved outcomes; modeled times were 360 ms and 280 ms. These are simulated times and operation units, not model latency or cost.
- Scheduling: identical graph yielded three serial batches (modeled 1,850 ms) versus two compatible batches (1,150 ms). No agents were spawned by this control.
- Variant search: a binary search was frozen after three development seeds. Held-out seed 991 returned 32/32 correct for both algorithms; item reads were 236 vs 5,928. This verifies bounded measured selection, not general evolutionary-search performance.
- Activation intervention: a fixed two-activation network restored 1.0 of the clean/corrupt gap with a targeted patch and 0.0 with the matched control. No external model weights were accessed.
