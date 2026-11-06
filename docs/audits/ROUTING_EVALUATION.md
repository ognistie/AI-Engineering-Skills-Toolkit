# Routing evaluation

Command:

```sh
python evals/score_routing.py --annotations evals/routing/independent-annotations.json
```

The 64 PT/EN development prompts cover explicit and implicit requests, ambiguity, simple negatives, adjacent skills, compositions and constraints. A separate forward reviewer received raw prompts, the catalogue and contextual host/scope facts, with the expected labels, supplied intent classifications and router predictions withheld. The [raw annotations](../../evals/routing/independent-annotations.json) are preserved. Dependency conflict and cycle cases exercise synthetic registries in unit tests.

| Measure | Observed |
| --- | --- |
| Macro Precision@3 / Recall@3 vs. development labels | 1.00 / 1.00 |
| Unnecessary / omitted selections against those labels | 0 / 64, 0 / 64 |
| Exact order | 64 / 64 |
| Expected policy fields and forbidden tools | 22 / 22 applicable cases |
| Structured justification coverage | 64 / 64; every output contains a decision reason, and each selection contains reason and outcome fields |
| Independent exact order agreement | 62 / 64 |

The disagreements are `route-34` and `route-59`. The reviewer preferred no **executable** selection without authorization or a checkpoint. The policy output retains the recommendation but blocks dispatch. Both interpretations preserve scope; the difference is material to UI wording and should be retained in a future host test. The new explicit capability test rejects a requested dispatch even if the user named the installed skill, when the skill does not cover the outcome.

These checks measure the policy conditional on classification. Explanation coverage is structural; the independent review plus the paired scenario exposed the semantic difference above. Natural-language routing accuracy, tool effects and ranking in the Codex/Claude interfaces remain NOT VERIFIED. Next: pin hosts and model revisions, capture selected resources and attempted tool effects in fresh sessions, and score separately from written recommendations.
