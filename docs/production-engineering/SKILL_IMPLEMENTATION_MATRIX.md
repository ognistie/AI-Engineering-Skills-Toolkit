# Implementation matrix

| Skill | Primary capability | Analysis input | Status |
| --- | --- | --- | --- |
| [agent-first-harness](../../skills/agent-first-harness/SKILL.md) | audit_agent_harness | repository_manifest | Tool-assisted |
| [agent-computer-interface](../../skills/agent-computer-interface/SKILL.md) | lint_tool_contract | tool_contract | Tool-assisted |
| [repository-context-architecture](../../skills/repository-context-architecture/SKILL.md) | audit_repository_context | document_map | Tool-assisted |
| [kv-cache-aware-context](../../skills/kv-cache-aware-context/SKILL.md) | analyze_context_prefix | request_pair | Tool-assisted |
| [context-compaction-recovery](../../skills/context-compaction-recovery/SKILL.md) | verify_context_restore | context_checkpoint | Tool-assisted |
| [inference-serving-architect](../../skills/inference-serving-architect/SKILL.md) | estimate_inference_capacity | serving_config | Tool-assisted |
| [agent-evals-engineer](../../skills/agent-evals-engineer/SKILL.md) | score_agent_trials | trial_records | Tool-assisted |
| [trajectory-review-engine](../../skills/trajectory-review-engine/SKILL.md) | review_trajectory_patterns | structured_trace | Tool-assisted |
| [evaluator-optimizer-loop](../../skills/evaluator-optimizer-loop/SKILL.md) | decide_refinement_loop | iteration_history | Tool-assisted |
| [durable-execution-engine](../../skills/durable-execution-engine/SKILL.md) | plan_durable_recovery | journal_snapshot | Tool-assisted |
| [brain-tool-runtime-separation](../../skills/brain-tool-runtime-separation/SKILL.md) | validate_execution_plan | action_plan | Tool-assisted |
| [agent-tool-interface-design](../../skills/agent-tool-interface-design/SKILL.md) | rank_tool_catalog | tool_catalog | Tool-assisted |
| [capability-security-architect](../../skills/capability-security-architect/SKILL.md) | check_capability_delegation | capability_policy | Tool-assisted |
| [prompt-injection-boundaries](../../skills/prompt-injection-boundaries/SKILL.md) | check_information_flow | flow_policy | Tool-assisted |
| [runtime-verification-engine](../../skills/runtime-verification-engine/SKILL.md) | verify_runtime_transitions | runtime_event_stream | Tool-assisted |

Every skill includes a portable local command, a versioned input fixture, positive or adversarial regression coverage, worked cases and a source-to-implementation boundary. The durable demo also integrates the existing local SQLite journal; the executor/flow/monitor compose in an inert integration test. This matrix makes no production validation claim.
