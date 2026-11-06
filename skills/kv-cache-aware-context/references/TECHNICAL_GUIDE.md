# Operating contract

Run `python scripts/check.py input.json` from this skill directory (Python 3.12+, standard library). Set `schema_version` to 1. The result is a JSON report; input errors exit 2. A valid report may indicate a failure or an incomplete check. Inspect its decision before taking action.

Pass baseline and candidate as ordered JSON segment lists. Optional observations rows contain input_tokens, cached_tokens and ttft_ms. Serialized bytes are a local proxy; observations are caller supplied, not inferred.

Add billed_input_tokens and cost_microunits only when known from the provider. Use the same currency and attribution in both arms; missing measurements suppress the arm total. Request hit rate counts requests with at least one cached token; the cached-token fraction measures the volume reused. For actual cache experiments retain request IDs, model and tokenizer revision, region, cold/warm ordering and the offered load.

Use a fixed baseline and retain the underlying evidence to reproduce the decision.
