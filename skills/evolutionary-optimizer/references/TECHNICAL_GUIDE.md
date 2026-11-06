# Technical guide

`python scripts/archive.py input.json`

```json
{
  "split": "development",
  "seeds": [
    "a",
    "b"
  ],
  "objectives": {
    "latency": {
      "direction": "min"
    },
    "quality": {
      "direction": "max"
    },
    "memory": {
      "direction": "min",
      "hard_limit": 100
    }
  },
  "variants": [
    {
      "id": "fast",
      "trials": {
        "a": {
          "latency": 4,
          "quality": 0.9,
          "memory": 90
        },
        "b": {
          "latency": 4,
          "quality": 0.9,
          "memory": 110
        }
      }
    },
    {
      "id": "baseline",
      "trials": {
        "a": {
          "latency": 10,
          "quality": 0.8,
          "memory": 90
        },
        "b": {
          "latency": 10,
          "quality": 0.8,
          "memory": 90
        }
      }
    }
  ]
}
```

Hard limits apply to every repetition. All named metrics participate in Pareto ranking, so use only comparable objective dimensions; a constrained metric also enters the frontier. Mean scores require the identical frozen seed set. A measurement split other than development is rejected. Track mutation, parent revision, environment and candidate hash in the experimental ledger, and freeze the candidate before any holdout check. Do not execute experimental code unless the host provides appropriate isolation.

### Search controls

Pin candidate identity, objective directions, units and repeats. Dominance requires at least as good on every objective and strictly better on at least one; keep ties for later diversity analysis. An individual hard-limit breach rejects the candidate even if its average is acceptable. The archive accepts at most 512 variants and 16 objectives to bound pairwise comparisons. If the search is bigger, predefine bounded generations and a retention policy rather than discarding weak seeds after measurement. Retest the frozen finalist on held-out inputs without updating the development archive.
