# Research basis

Primary reference: [Trace and span model](https://opentelemetry.io/docs/concepts/signals/traces/).

OpenTelemetry models distributed work as spans with parentage, timing and attributes. AAES checks a normalized single trace for temporal and structural anomalies and explicit repeated operation IDs. It does not ingest provider telemetry automatically, estimate causal effects, or recover omitted spans.
