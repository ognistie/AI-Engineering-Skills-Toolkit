# Technical guide

`python scripts/policy.py input.json`

```json
{
  "policy": {
    "revision": "p1",
    "tools": {
      "publish": {
        "effect": "external",
        "principals": [
          "operator"
        ],
        "resources": [
          "artifact/A"
        ],
        "approval_required": true
      }
    },
    "max_timeout_ms": 1000
  },
  "action": {
    "request_id": "q5",
    "principal": "operator",
    "tool": "publish",
    "resource": "artifact/A",
    "payload_sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "units": 1,
    "timeout_ms": 500
  },
  "now": 10,
  "remaining_units": 2,
  "read_only": false
}
```

Load policy, clock, principal, budgets, approval and scope from trusted executor state. Recompute the payload digest from the exact bytes or canonical tool arguments that will be dispatched; do not trust a proposed digest. Use exact resource identifiers resolved by the adapter, with no implicit prefix matches. The approval binding includes policy revision and immutable request attributes.

Executor integration: (1) derive trusted request metadata; (2) in a durable transaction load current policy, fetch approval, compare binding/expiry, atomically claim request ID and consume approval/reserve budget; (3) release the transaction, dispatch the immutable payload with a timeout through the only credentialed wrapper; (4) record evidence and reconcile uncertain results by request ID. Reject duplicates as new executions. Test expiry and a race using the real store before deploying. The bundled helper is the decision function only; it cannot establish identity, trust an approval, consume it or block bypass paths.

For a trusted single-node integration, import `scripts/reservations.py` in the credentialed wrapper. Initialize the budget once with `initialize(db, units)`; call `reserve(db, trusted_request, trusted_clock)` per request. The callback supplies the current integer clock after the write lock is acquired. Only dispatch when `reserved` is true. The approval needs a stable `id` from the approval store; the table tracks consumption by that ID. Keep policy/approval lifecycle and this reservation transaction consistent in the real executor. A process crash after reservation requires reconciliation; do not reuse a consumed approval to retry blindly.

### Validate actual enforcement

In the real credentialed wrapper, test an action that claims to be read-only while selecting a destructive tool, a trusted tool with a different resource and a duplicate reservation. Assert zero calls for denied cases, and query the execution ledger for the allowed race. Record trusted policy revision, request ID and rule, without storing raw secrets or approval tokens. Keep any classification derived from files, logs or external requests outside the authority decision.
