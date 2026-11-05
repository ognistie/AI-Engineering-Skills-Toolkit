# Behavioral checks for the eight advanced skills

Use the sanitized inputs in `../fixtures/` for deterministic checks. For agent trials give each variant the same raw artifacts and user request, withhold graders, use a clean session per attempt, and randomize or balance order. A content assertion does not prove an external effect.

| Skill | Distinguishing observable result |
| --- | --- |
| adaptive-reasoning | Given conflicting evidence, proposes one discriminating check within the frozen budget; refuses another attempt once it cannot fit. |
| long-horizon-executor | Persists a claim, resumes in reconciliation, and advances only after verified state. Replaying the event does not dispatch again. |
| multi-agent-router | Keeps conflicting writes in separate batches; uses serial mode without permission or measured coordination input. |
| runtime-guardian | A changed resource or policy revision invalidates approval; two concurrent requests cannot reserve one execution twice. |
| evolutionary-optimizer | Excludes a candidate that violates one seed's memory cap, retains nondominated variants, and rejects holdout inputs for selection. |
| hypothesis-lab | Counts correlated evidence once, retains intervention contradictions, and names a discriminating experiment. |
| mechanistic-interpretability | Excludes a pair with a negligible baseline gap and compares the valid patch to a control without clipping. |
| agentic-rl-lab | Computes discounted returns, rejects repeated terminal claims, and keeps unsafe episodes visible. |

[Paired pilot](paired-pilot.md) contains actual observations for the three highest-risk workflows. These checks are not a model-quality benchmark.
