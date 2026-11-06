# Operating contract

Run `python scripts/check.py input.json` from this skill directory (Python 3.12+, standard library). Set `schema_version` to 1. The result is a JSON report; input errors exit 2. A valid report may indicate a failure or an incomplete check. Inspect its decision before taking action.

Pass layers, kv_heads, head_dim, kv_dtype_bytes, tokens, concurrent_sequences, block_tokens, kv_shards, gpu_bytes, weights_bytes_per_gpu, reserve_bytes_per_gpu and optionally transfer_bytes_per_second. Model per rank; validate on device before shipping.

For an authorized benchmark pin engine/model revision, hardware topology, parallelism and generation limits. Replay the same arrival timestamps, input/output lengths and repeated prefixes across colocated and split arms. Run separate warm and cold repetitions; collect offered vs completed requests, tail TTFT and intertoken latency, timeouts, peak GPU memory and utilization. Record KV handoff and cache evictions where supported. Verify that tail improvements preserve per-SLO goodput; revert if transfer or queueing dominates. The byte estimate omits fragmentation beyond page rounding, runtime workspace variability, quantized metadata and engine-specific KV layouts.

Use a fixed baseline and retain the underlying evidence to reproduce the decision.
