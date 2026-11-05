# Technical guide

`python scripts/matrix.py input.json`

```json
{
  "null_hypothesis": "null",
  "hypotheses": [
    {
      "id": "null",
      "prediction": "No difference by cache state",
      "falsifier": "Repeatable difference under a controlled cache intervention"
    },
    {
      "id": "cache",
      "prediction": "Cold cache adds requests",
      "falsifier": "Same request count after changing cache state alone"
    }
  ],
  "evidence": [
    {
      "id": "e1",
      "group": "run7",
      "hypothesis": "cache",
      "kind": "observation",
      "direction": "supports"
    },
    {
      "id": "e2",
      "group": "run7",
      "hypothesis": "cache",
      "kind": "observation",
      "direction": "supports"
    }
  ]
}
```

Group correlated observations. A group can count at most once per direction and hypothesis; conflicting entries remain visible. The descriptive ordering prioritizes fewer intervention contradictions, then more intervention support, fewer overall contradictions and more overall support. It is not a posterior or a substitute for assessing intervention design. Choose the next experiment by its ability to distinguish the leading mechanisms.
