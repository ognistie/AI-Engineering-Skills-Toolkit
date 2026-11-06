# Research basis

Primary reference: [OpenTelemetry, traces and Anthropic agent evals](https://opentelemetry.io/docs/concepts/signals/traces/).

Span data and transcript events capture distinct observations. Existing trajectory-analyzer handles span normalization and overlap. This helper identifies repeated failed operations with unchanged observed state and flags outcome disagreement; it does not infer causality.
