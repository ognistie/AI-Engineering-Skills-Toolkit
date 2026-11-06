# Research basis

Primary source: [Temporal Event History](https://docs.temporal.io/encyclopedia/event-history).

Temporal separates replay of durable events from new external activity. AAES applies that separation with a local transactional journal and explicit reconciliation. It is not a distributed executor, crash-proof external ledger, or exactly-once guarantee.

## Applicability and failure boundary

The [METR time-horizon study](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/) measures task completion probability versus human task duration; it does not measure SQLite durability. Validate journal recovery separately from model success or an external exactly-once claim.
