"""Estimate conventional transformer KV capacity; never contacts a serving engine."""
from _contract import integer, main, number


def analyze(doc):
    vals = {key: integer(doc[key], key, 1) for key in ("layers","kv_heads","head_dim","kv_dtype_bytes",
            "tokens","concurrent_sequences","block_tokens","kv_shards","gpu_bytes")}
    n, shards = vals["kv_heads"], vals["kv_shards"]
    if n % shards:
        raise ValueError("KV heads must divide across modeled shards; specify actual replicated layout")
    per_token = 2 * vals["layers"] * (n // shards) * vals["head_dim"] * vals["kv_dtype_bytes"]
    block = vals["block_tokens"]
    rounded = ((vals["tokens"] + block - 1) // block) * block
    required = rounded * per_token * vals["concurrent_sequences"]
    available = (vals["gpu_bytes"] - integer(doc["weights_bytes_per_gpu"], "weights")
                 - integer(doc["reserve_bytes_per_gpu"], "reserve"))
    transfer = None
    if "transfer_bytes_per_second" in doc:
        rate = number(doc["transfer_bytes_per_second"], "bandwidth", 1)
        transfer = (per_token * shards * vals["tokens"]) * 1000 / rate
    return {"estimate": "conventional_transformer_kv_only", "kv_bytes_per_token_per_gpu": per_token,
            "allocated_tokens_per_sequence": rounded, "kv_required_bytes_per_gpu": required,
            "kv_available_bytes_per_gpu": available, "fits_modeled_memory": required <= available,
            "max_sequences_by_kv": max(0, available // (rounded * per_token)),
            "ideal_full_request_transfer_ms": transfer, "measured": False}


if __name__ == "__main__":
    main(analyze, __doc__)
