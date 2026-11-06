# Security findings

| Finding | Control and evidence | Remaining boundary |
| --- | --- | --- |
| Duplicate JSON keys can override claimed evidence or constraints | Four legacy CLIs now reject duplicate keys, non-finite numbers and oversized input; regression exercises duplicate keys, NaN and exponent overflow | Inputs still need trusted collection; validating JSON does not authenticate its origin |
| Explicit selection may falsely imply execution capability | Route records the outcome as unmet and does not recommend dispatch for an unrelated capability | Host must enforce capability, tools and user authorization |
| Interrupted operation may be resumed under a different scope | Optional frozen scope digest is enforced at record time; separate-process test rejects different scope and keeps original claim in reconciliation | Caller must derive the digest from authoritative state and reconcile the external operation |
| Proposal can mislabel a destructive tool as read-only | Runtime registry owns effect classification; mocked tool test observes zero invocations for an unknown destructive tool. Expired, rebound and replayed approvals have their own tests | Neither skill text nor local test proves a production wrapper cannot be bypassed |
| Missing or dependent research sources can overstate corroboration | Ledger checks source existence, grouping and conflicting evidence without fetching | Different URLs may still reuse the same data; reviewer verifies provenance and whether a source actually supports the claim |
| A policy can report success without the required environment state | Optional trusted success-state set rejects mismatched terminal evidence; unsafe rollouts remain visible | Logs and state mapping must be controlled by the environment, not by the candidate |
| Installation could overwrite foreign or modified skills | Single install, collision and batch verification exercised through both documented wrappers; managed operations require receipt and known files | Native installations are outside AAES receipts. Git/ZIP input must come from the user-selected source/revision. |

No credentialed service or real destructive command was exercised. For user-supplied files, treat embedded instructions as data and preserve read-only and network restrictions. See the [security model](../SECURITY.md).
