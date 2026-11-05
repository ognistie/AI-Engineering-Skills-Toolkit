# Use cases

| Task | Decision |
| --- | --- |
| “Só indique skills para investigar timeouts deste trace.” | Recommend trajectory analysis; do not execute or select experiment evaluation until asked to compare variants. |
| “Translate this string.” | Abstain. |
| “Run our replay against a remote environment.” | Report missing authorization or tool access; do not dispatch. |
| “Use the verifier and don't run anything.” | Explicit selection; work from supplied evidence and leave unavailable gates inconclusive. |
