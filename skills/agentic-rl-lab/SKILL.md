---
name: agentic-rl-lab
description: "Design a tool-use reinforcement-learning experiment with isolated transitions, explicit rewards, credit assignment and evaluation. Use for policy training protocols or offline rollouts; no training is required."
metadata:
  author: AAES
  version: "0.1.1"
---

# Agentic RL Lab

Make the environment and credit assignment testable before training.

## Procedure

Specify observations, allowed actions, termination, time limits and reset isolation. Define outcome rewards from trusted state, compare with a fixed policy and report cost and unsafe actions separately. Give success credit only once; preserve timeout, unsafe action and malformed transition outcomes. Choose discounting and credit assignment before inspecting runs; explicitly distinguish environment rewards, return-to-go and causal action effects.

Use [the rollout protocol](references/TECHNICAL_GUIDE.md) for offline validation. Test success, timeout, repeated success claims and unauthorized actions before training. Split by task family to check generalization. If infrastructure or training authorization is absent, deliver the environment interface, validated rollout scorer and an experiment plan without claiming learned behavior.

## Deliverable

Return environment contract, episode validity, outcome and cost metrics, baseline, credit rule and limits.

Example: A model repeatedly claims success while the environment remains nonterminal; no terminal reward is issued.

Read [use cases](references/USE_CASES.md) to calibrate decisions, and [research basis](references/RESEARCH_BASIS.md) for evidence and limits.
