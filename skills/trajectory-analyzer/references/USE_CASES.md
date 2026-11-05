# Use cases

- **Retry after timeout:** operation op7 appears twice; compare idempotency key and persisted state. Replay with timeout injected once and assert the final count independently.
- **Parallel fan-out:** 100 ms parent with two overlapping 80 ms child spans. Summed span duration is 260 ms while observed wall time is 100 ms; neither indicates which dependency is on the critical path.
