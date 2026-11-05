"""Suggest work batches without spawning agents."""
from collections import defaultdict


def names(items):
    if not isinstance(items, list) or any(type(v) is not str or not v for v in items):
        raise ValueError("Expected a list of nonempty IDs")
    if len(set(items)) != len(items):
        raise ValueError("Repeated ID")
    return set(items)


def integer(value, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError("Invalid estimate or limit")
    return value


def analyze(doc):
    tasks = doc["tasks"]
    if not isinstance(tasks, list) or not tasks or len(tasks) > 256:
        raise ValueError("Expected 1 to 256 tasks")
    names([task["id"] for task in tasks])
    agents = integer(doc["max_agents"], 1)
    overhead = doc["overhead_ms"]
    if overhead is not None:
        integer(overhead)
    gain = integer(doc["min_gain_ms"], 1)
    if any(type(doc[k]) is not bool for k in ("host_parallel", "delegation_authorized")):
        raise ValueError("Host capability and authority must be booleans")
    rows = {t["id"]: t for t in tasks}
    deps, reads, writes, duration, children = {}, {}, {}, {}, defaultdict(list)
    for key, row in rows.items():
        deps[key] = names(row["depends_on"])
        if key in deps[key] or deps[key] - rows.keys():
            raise ValueError(f"Invalid dependency of {key}")
        reads[key], writes[key] = names(row["reads"]), names(row["writes"])
        duration[key] = integer(row["ms"], 1)
        for parent in deps[key]:
            children[parent].append(key)
    available = sorted(k for k, v in deps.items() if not v)
    count = {k: len(v) for k, v in deps.items()}
    order = []
    while available:
        item = available.pop(0)
        order.append(item)
        for child in children[item]:
            count[child] -= 1
            if not count[child]:
                available.append(child)
        available.sort()
    if len(order) != len(rows):
        raise ValueError("Cyclic dependencies")
    done, parallel = set(), []
    while len(done) < len(rows):
        batch, rs, ws = [], set(), set()
        for key in order:
            if key in done or not deps[key] <= done:
                continue
            if writes[key] & (rs | ws) or reads[key] & ws:
                continue
            batch.append(key)
            rs |= reads[key]
            ws |= writes[key]
            if len(batch) == agents:
                break
        parallel.append(batch)
        done.update(batch)
    serial = sum(duration.values())
    estimated = (sum(max(duration[k] for k in b) for b in parallel) + overhead
                 if overhead is not None else None)
    can_parallel = doc["host_parallel"] and doc["delegation_authorized"]
    use = (can_parallel and any(len(b) > 1 for b in parallel)
           and estimated is not None and serial - estimated >= gain)
    return {"topology": "parallel_batches" if use else "sequential",
            "batches": parallel if use else [[key] for key in order],
            "serial_ms": serial, "estimated_parallel_ms": estimated,
            "estimated_saving_ms": serial - estimated if estimated is not None else None,
            "reason": "estimated_gain" if use else "constraints_or_unproven_gain",
            "dispatch": "not_dispatched"}

def _pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def _nonfinite(value):
    raise ValueError(f"Invalid JSON constant: {value}")


def main():
    import argparse
    import json
    from pathlib import Path

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    try:
        with args.input.open("rb") as stream:
            raw = stream.read(2_000_001)
        if len(raw) > 2_000_000:
            raise ValueError("Input exceeds 2 MB")
        document = json.loads(raw, object_pairs_hook=_pairs, parse_constant=_nonfinite)
        print(json.dumps(analyze(document), allow_nan=False, indent=2))
    except (ValueError, TypeError, KeyError, OSError, ArithmeticError, RecursionError) as exc:
        parser.exit(2, f"Invalid input: {exc}\n")


if __name__ == "__main__":
    main()
