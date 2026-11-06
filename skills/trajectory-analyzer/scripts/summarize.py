"""Summarize sanitized, single-trace spans on a common clock."""
import argparse
from collections import Counter
import json
from pathlib import Path


def summarize(document):
    trace_id, spans = document["trace_id"], document["spans"]
    if type(trace_id) is not str or not trace_id or not isinstance(spans, list) or not spans:
        raise ValueError("Expected trace_id and nonempty spans")
    by_id = {}
    for span in spans:
        key, start, end = span["id"], span["start_ms"], span["end_ms"]
        if type(key) is not str or not key or key in by_id:
            raise ValueError("Missing or duplicate span id")
        if any(type(v) is not int or v < 0 for v in (start, end)) or end < start:
            raise ValueError(f"Invalid timing for {key}")
        if span["status"] not in ("ok", "error", "timeout", "unknown"):
            raise ValueError(f"Invalid status for {key}")
        for optional in ("parent", "operation"):
            value = span.get(optional)
            if value is not None and (type(value) is not str or not value):
                raise ValueError(f"Invalid {optional} for {key}")
        by_id[key] = span

    done = set()
    for span_id in by_id:
        chain = set()
        current = span_id
        while current in by_id and current not in done:
            if current in chain:
                raise ValueError("Cyclic span parentage")
            chain.add(current)
            current = by_id[current].get("parent")
        done.update(chain)

    order = sorted(spans, key=lambda row: (row["start_ms"], row["id"]))
    missing, outside, failures = [], [], []
    operations = Counter()
    work, covered, finish = 0, 0, order[0]["start_ms"]
    for row in order:
        start, end = row["start_ms"], row["end_ms"]
        work += end - start
        covered += max(0, end - max(start, finish))
        finish = max(finish, end)
        parent = row.get("parent")
        if parent is not None:
            p = by_id.get(parent)
            if p is None:
                missing.append(row["id"])
            elif start < p["start_ms"] or end > p["end_ms"]:
                outside.append(row["id"])
        if row["status"] in ("error", "timeout"):
            failures.append({"id": row["id"], "status": row["status"]})
        if row.get("operation"):
            operations[row["operation"]] += 1
    return {"trace_id": trace_id, "observed_wall_ms": finish - order[0]["start_ms"],
            "span_duration_sum_ms": work, "covered_ms": covered,
            "missing_parent_spans": missing, "outside_parent_interval": outside,
            "failures": failures, "repeated_operations": {k:v for k,v in operations.items() if v > 1},
            "chronology": [row["id"] for row in order]}


def read_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError(f"Duplicate JSON key: {key}")
            result[key] = value
        return result

    def real(token):
        value = float(token)
        if not -float("inf") < value < float("inf"):
            raise ValueError("Non-finite JSON number")
        return value

    with path.open("rb") as stream:
        data = stream.read(2_000_001)
    if len(data) > 2_000_000:
        raise ValueError("JSON input exceeds 2 MB")
    return json.loads(data, object_pairs_hook=pairs, parse_float=real, parse_constant=real)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trace", type=Path)
    args = parser.parse_args()
    try:
        result = summarize(read_json(args.trace))
    except (ValueError, TypeError, KeyError, OSError, RecursionError) as exc:
        parser.exit(2, f"Invalid trace: {exc}\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
