# Security validation

| Controlled scenario | Result |
| --- | --- |
| Model embeds an extra authorization field or selects an unlisted resource | Plan preflight refuses it before fake tool effects. |
| Delegated grant adds write or crosses expiry | Capability descriptor check denies it. |
| Untrusted record attempts to switch local summary to export | Executor-bound control prevents switching; separate export test denies the private provenance label. |
| Replay or cumulative cost violation | Monitor blocks the event and returns the last valid state and spend. |
| Flow/monitor composition | Denied synthetic proposal produces zero mock export calls. |

These are executable local checks, not enforcement guarantees for an actual host. Integrate a credentialed executor with immutable request binding, trusted grant provenance, independent clock and receipt, atomic quota/approval consumption, and explicit isolation. Validate bypass resistance and failure recovery in the target environment before claiming production readiness.
