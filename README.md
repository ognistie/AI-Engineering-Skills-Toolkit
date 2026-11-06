# Advanced AI Engineering Skills

**AAES** is a portable catalog of 28 [Agent Skills](https://agentskills.io/specification) for agent design, evaluation, research, and operational safety. It pairs task procedures with reproducible local checks. The helpers use the Python standard library and require no model API, GPU, or service account.

## Install

Clone the repository or [download the ZIP](https://github.com/ognistie/AI-Engineering-Skills-Toolkit/archive/refs/heads/main.zip). Open the extracted repository with Python 3.12+ installed.

```sh
git clone https://github.com/ognistie/AI-Engineering-Skills-Toolkit.git
cd AI-Engineering-Skills-Toolkit
```

| Host | Windows PowerShell | macOS / Linux |
| --- | --- | --- |
| Codex | `.\scripts\install.ps1 -Target codex` | `sh scripts/install.sh codex` |
| Claude Code | `.\scripts\install.ps1 -Target claude` | `sh scripts/install.sh claude` |

Add `-Skill process-verifier` in PowerShell or append `process-verifier` in shell to install only that skill. Start a new session and invoke `$process-verifier` in Codex or `/process-verifier` in Claude Code.

**Ask your agent:**

> Install the `process-verifier` skill from https://github.com/ognistie/AI-Engineering-Skills-Toolkit for this host. Follow INSTALL.md, preserve existing skills, and report the destination and how to invoke it.

Use “all 28 skills” to install the full catalog. See [installation and update procedures](INSTALL.md).

For hosts that import skill archives, download an individual package from [dist/](dist/).

## Research areas

| Area | Skills |
| --- | --- |
| Routing | [Skill orchestrator](skills/skill-orchestrator/) |
| Evidence and evaluation | [Research](skills/research-orchestrator/), [verification](skills/process-verifier/), [traces](skills/trajectory-analyzer/), [experiments](skills/experiment-evaluator/) |
| Agent execution | [Adaptive reasoning](skills/adaptive-reasoning/), [checkpoints](skills/long-horizon-executor/), [delegation](skills/multi-agent-router/), [runtime policy](skills/runtime-guardian/) |
| Experimental methods | [Evolutionary search](skills/evolutionary-optimizer/), [hypotheses](skills/hypothesis-lab/), [interpretability](skills/mechanistic-interpretability/), [agentic RL](skills/agentic-rl-lab/) |
| Production engineering | [15 skills for harnesses, tools, context, evals, runtime and security](docs/production-engineering/SKILL_IMPLEMENTATION_MATRIX.md) |

[Architecture](docs/ARCHITECTURE.md) · [Independent audit and remediation](audit/production-ai-engineering/REMEDIATION.md) · [Production engineering evidence](docs/production-engineering/FINAL_ENGINEERING_REPORT.md) · [Security model](docs/SECURITY.md)

Local validation covers format, deterministic behavior and installation. Host activation, model efficacy, and production enforcement require separate evidence.
