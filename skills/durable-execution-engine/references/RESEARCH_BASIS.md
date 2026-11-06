# Research basis

Primary reference: [Temporal Event History and Retry Policies](https://docs.temporal.io/encyclopedia/event-history).

Temporal distinguishes deterministic replay from re-executing effects. This skill consumes the existing AAES checkpoint format to derive recovery decisions; SQLite persistence stays in long-horizon-executor. No exactly-once claim or Temporal integration is implied.
