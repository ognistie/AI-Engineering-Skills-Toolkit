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
