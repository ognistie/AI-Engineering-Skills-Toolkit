---
name: mechanistic-interpretability
description: "Design or analyze activation-patching, sparse feature, or circuit experiments on neural models. Use when inspecting internal activations or designing interventions; agent logs alone are insufficient."
metadata:
  author: AAES
  version: "0.1.1"
---

# Mechanistic Interpretability

Test whether a defined intervention changes a model behavior.

## Procedure

Pin model and tokenizer revisions, paired clean/corrupt examples, token alignment, layer and hook names, metric orientation and planned controls. Measure clean and corrupt baselines first. If their gap is too small, the normalized result is unstable; do not search until an appealing patch appears. Measure the targeted patch and matched controls, such as an unrelated position or shuffled pairing, and repeat on held-out pairs.

When weights and hookable activations are unavailable, produce the protocol and distinguish observed behavior from mechanistic evidence. Use [the patching guide](references/TECHNICAL_GUIDE.md) for optional local tooling and the offline metric. A recovered behavior supports a scoped intervention claim; it does not by itself prove a unique mechanism, circuit or semantic feature.

## Deliverable

Return intervention, baselines, controls, paired effect with uncertainty, and the strongest claim the experiment supports.

Example: A patch restores the target logit difference only on one prompt and the unrelated-position control does too; report the result as inconclusive.

Read [use cases](references/USE_CASES.md) to calibrate decisions, and [research basis](references/RESEARCH_BASIS.md) for evidence and limits.
