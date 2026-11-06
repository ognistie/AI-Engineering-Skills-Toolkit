"""Compare stable request segments and summarize observed provider measurements."""
from _contract import canonical, integer, main, number, sequence


def analyze(doc):
    baseline = [canonical(x) for x in sequence(doc["baseline"], "baseline")]
    candidate = [canonical(x) for x in sequence(doc["candidate"], "candidate")]
    stable = []
    for left, right in zip(baseline, candidate):
        if left != right:
            break
        stable.append(left)
    totals = {}
    for row in sequence(doc.get("observations", []), "observations"):
        arm = row["arm"]
        if arm not in ("baseline", "candidate"):
            raise ValueError("Unknown observation arm")
        supplied = integer(row["input_tokens"], "input tokens", 1)
        cached = integer(row["cached_tokens"], "cached tokens")
        if cached > supplied:
            raise ValueError("Cached tokens exceed input")
        bucket = totals.setdefault(arm, {"input_tokens":0,"cached_tokens":0,"ttft_ms":[],
                                         "hits":0,"billed_input_tokens":[],"cost_microunits":[]})
        bucket["input_tokens"] += supplied
        bucket["cached_tokens"] += cached
        bucket["hits"] += int(cached > 0)
        bucket["ttft_ms"].append(number(row["ttft_ms"], "TTFT"))
        for key in ("billed_input_tokens","cost_microunits"):
            if key in row:
                bucket[key].append(integer(row[key], key))
    for bucket in totals.values():
        bucket["cached_token_fraction"] = bucket["cached_tokens"] / bucket["input_tokens"]
        times = sorted(bucket.pop("ttft_ms"))
        bucket["samples"] = len(times)
        bucket["request_hit_rate"] = bucket.pop("hits") / len(times)
        bucket["p95_ttft_ms"] = times[(95 * len(times) + 99)//100 - 1]
        for key in ("billed_input_tokens","cost_microunits"):
            values = bucket[key]
            bucket[key] = sum(values) if len(values) == len(times) else None
    return {"stable_segments": len(stable), "stable_segment_bytes": sum(map(len, stable)),
            "proxy": "canonical_segment_bytes", "observed_provider_usage": totals or None}


if __name__ == "__main__":
    main(analyze, __doc__)
