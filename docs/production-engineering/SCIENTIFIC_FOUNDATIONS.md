# Scientific foundations

The references support engineering decisions; the local helpers do not reproduce laboratory results.

- **agent-first-harness:** [OpenAI, Harness engineering (2026)](https://openai.com/index/harness-engineering/) — [mechanism and limits](../../skills/agent-first-harness/references/RESEARCH_BASIS.md).
- **agent-computer-interface:** [SWE-agent and Anthropic tool design (2024–2025)](https://www.anthropic.com/research/writing-tools-for-agents) — [mechanism and limits](../../skills/agent-computer-interface/references/RESEARCH_BASIS.md).
- **repository-context-architecture:** [OpenAI, Harness engineering and Agent Skills](https://openai.com/index/harness-engineering/) — [mechanism and limits](../../skills/repository-context-architecture/references/RESEARCH_BASIS.md).
- **kv-cache-aware-context:** [Manus, Context Engineering for AI Agents (2025)](https://manus.im/en/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) — [mechanism and limits](../../skills/kv-cache-aware-context/references/RESEARCH_BASIS.md).
- **context-compaction-recovery:** [Manus, Context Engineering for AI Agents (2025)](https://manus.im/en/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) — [mechanism and limits](../../skills/context-compaction-recovery/references/RESEARCH_BASIS.md).
- **inference-serving-architect:** [NVIDIA Dynamo, Disaggregated Serving and Overall Architecture](https://docs.nvidia.com/dynamo/components/router/disaggregated-serving) — [mechanism and limits](../../skills/inference-serving-architect/references/RESEARCH_BASIS.md).
- **agent-evals-engineer:** [Anthropic, Demystifying evals for AI agents (2026)](https://www.anthropic.com/research/demystifying-evals-for-ai-agents) — [mechanism and limits](../../skills/agent-evals-engineer/references/RESEARCH_BASIS.md).
- **trajectory-review-engine:** [OpenTelemetry, traces and Anthropic agent evals](https://opentelemetry.io/docs/concepts/signals/traces/) — [mechanism and limits](../../skills/trajectory-review-engine/references/RESEARCH_BASIS.md).
- **evaluator-optimizer-loop:** [Anthropic, Building effective agents](https://www.anthropic.com/research/building-effective-agents) — [mechanism and limits](../../skills/evaluator-optimizer-loop/references/RESEARCH_BASIS.md).
- **durable-execution-engine:** [Temporal Event History and Retry Policies](https://docs.temporal.io/encyclopedia/event-history) — [mechanism and limits](../../skills/durable-execution-engine/references/RESEARCH_BASIS.md).
- **brain-tool-runtime-separation:** [CaMeL, Defeating Prompt Injections by Design (2025)](https://arxiv.org/abs/2503.18813) — [mechanism and limits](../../skills/brain-tool-runtime-separation/references/RESEARCH_BASIS.md).
- **agent-tool-interface-design:** [Anthropic, Advanced tool use (2025)](https://www.anthropic.com/research/advanced-tool-use) — [mechanism and limits](../../skills/agent-tool-interface-design/references/RESEARCH_BASIS.md).
- **capability-security-architect:** [CaMeL and AI Control](https://arxiv.org/abs/2503.18813) — [mechanism and limits](../../skills/capability-security-architect/references/RESEARCH_BASIS.md).
- **prompt-injection-boundaries:** [Google DeepMind, CaMeL (2025)](https://arxiv.org/abs/2503.18813) — [mechanism and limits](../../skills/prompt-injection-boundaries/references/RESEARCH_BASIS.md).
- **runtime-verification-engine:** [OpenTelemetry trace model and Temporal Event History](https://docs.temporal.io/encyclopedia/event-history) — [mechanism and limits](../../skills/runtime-verification-engine/references/RESEARCH_BASIS.md).

## Integration sources

- [SWE-agent](https://arxiv.org/abs/2405.15793) informs interface evaluation; selection and argument validity need separate measures.
- [CaMeL implementation](https://github.com/google-research/camel-prompt-injection) describes the research prototype. AAES does not implement its interpreter.
- [NVIDIA Dynamo architecture](https://docs.nvidia.com/dynamo/latest/knowledge-base/overview) and [versioned disaggregated serving guide](https://docs.nvidia.com/dynamo/v1.6.0/kubernetes/disaggregated-serving/overview) replace stale URLs supplied in the brief. Engine-specific implementation details are not assumed.
- [Inspect AI scorers](https://inspect.aisi.org.uk/scorers.html), [Playwright test isolation](https://playwright.dev/docs/test-isolation) and [Docker seccomp](https://docs.docker.com/engine/security/seccomp/) support test adapters and isolation choices. They are not bundled as dependencies.
- [vLLM disaggregated prefilling](https://docs.vllm.ai/en/latest/features/disagg_prefill/) and [SGLang prefill/decode disaggregation](https://docs.sglang.io/advanced_features/pd_disaggregation.html) are backend references; consult the documentation matching the installed versions before running experiments.
