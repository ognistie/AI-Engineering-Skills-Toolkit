# Technical guide

`python scripts/patch_metrics.py input.json`

```json
{
  "min_baseline_gap": 0.2,
  "pairs": [
    {
      "id": "p1",
      "clean": 2,
      "corrupt": 0,
      "patched": 1.2,
      "control": 0.2
    }
  ]
}
```

Normalize (patched − corrupt) / (clean − corrupt) after orienting the metric so higher means more of the clean behavior. Apply the same denominator to the matched control. Retain negative and above-one values. Record exclusions and repeat on held-out examples; fit uncertainty at the pair or cluster level. The helper computes descriptive results only.

Optional execution when a compatible local [TransformerLens](https://github.com/TransformerLensOrg/TransformerLens) model and dependencies already exist: run the clean sequence with an activation cache, run the corrupt sequence as baseline, then run the corrupt input with a temporary hook that clones the corrupt activation and replaces only the prespecified layer/position from the aligned clean cache. Use identical logits, answer tokens and metric for each condition. For SAE analysis use a compatible local [SAELens](https://github.com/decoderesearch/SAELens) checkpoint; compare reconstruction and ablation controls and do not equate a feature label with a causal mechanism. Do not download weights or run code just to install the skill.

### Intervention verification

Keep one hook coordinate fixed while recording clean, corrupt, patched and matched control conditions. A large recovery with a comparably large control is not specific. A near-zero denominator is an exclusion with a count and reason, not permission to silently switch metrics. Validate the hook by comparing actual activations before and after the intervention. The repository's two-activation toy verifies this arithmetic; repeat on a pinned open model before drawing language-model conclusions.
