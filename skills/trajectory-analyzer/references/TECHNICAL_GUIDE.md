# Normalized trace

`python scripts/summarize.py trace.json`

`{"trace_id":"r7","spans":[{"id":"t1","start_ms":0,"end_ms":10,"status":"timeout","operation":"op7"},{"id":"t2","start_ms":11,"end_ms":19,"status":"ok","operation":"op7"}]}`

Convert exported spans to integer milliseconds on a shared clock; record exporter, sampling, dropped spans and clock-offset caveats separately. Optional `parent` is a span ID; optional `operation` links retries of the same logical operation. Allowed statuses: ok, error, timeout, unknown. Do not send raw prompts, tokens or tool payloads to this helper.

Wall time spans first start to last finish; covered time is the union of observed intervals; duration sum can double count nested/overlapping work. An interval outside its parent is a flag for review, not proof of a clock bug. Repeated operations need state inspection and may be expected. For a replay preserve the workload, policy and tool contracts while changing one failure mechanism.

### Corruption and temporal ambiguity

The JSON reader rejects duplicate keys, oversized input and non-finite numbers before timing analysis. Treat missing parents, clock differences and incomplete samples as uncertainty about the observed envelope. An out-of-parent child may be asynchronous or reflect clock offset; do not relabel it as root cause. Replay the same initial state with one controlled failure, then compare persisted effects outside the transcript.
