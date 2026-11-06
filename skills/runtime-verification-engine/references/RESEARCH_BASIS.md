# Research basis

Primary reference: [OpenTelemetry trace model and Temporal Event History](https://docs.temporal.io/encyclopedia/event-history).

Event histories support deterministic replay of observed state. AAES checks sequence, transition table and cumulative budget with a deterministic monitor and returns the first violation. A pure monitor must be integrated with the live executor to block effects.
