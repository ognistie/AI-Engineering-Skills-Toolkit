"""Evaluate paired attempts against a frozen descriptive protocol."""
import argparse
import json
import math
from pathlib import Path
import random


def number(value, label, minimum=0, maximum=None):
    if type(value) not in (int, float) or not math.isfinite(value):
        raise ValueError(f"{label} must be finite")
    if value < minimum or maximum is not None and value > maximum:
        raise ValueError(f"{label} out of range")
    return value


def compare(protocol, observations):
    identifier = protocol["id"]
    if type(identifier) is not str or not identifier or observations["protocol_id"] != identifier:
        raise ValueError("Observations must match the frozen protocol")
    keys = protocol["trial_ids"]
    if not isinstance(keys, list) or not keys or any(type(v) is not str or not v for v in keys):
        raise ValueError("Expected nonempty trial_ids")
    known = set(keys)
    if len(known) != len(keys):
        raise ValueError("Duplicate protocol trial IDs")
    groups = protocol.get("trial_groups")
    if "trial_groups" in protocol and (
            not isinstance(groups, dict) or set(groups) != known
            or any(type(group) is not str or not group.strip() for group in groups.values())):
        raise ValueError("trial_groups must map every planned trial to a task cluster")
    if groups and len(set(groups.values())) > 512:
        raise ValueError("At most 512 task clusters for the optional interval")
    bootstrap_seed = protocol.get("bootstrap_seed", 0)
    if type(bootstrap_seed) is not int:
        raise ValueError("bootstrap_seed must be an integer")
    limits = protocol["gates"]
    floor = number(limits["min_candidate_success"], "success floor", 0, 1)
    delta = number(limits["min_success_delta"], "success delta", -1, 1)
    p95_max = number(limits["max_candidate_p95_ms"], "latency cap")
    cost_max = number(limits["max_candidate_mean_cost"], "cost cap")
    variants = {"baseline": {}, "candidate": {}}
    for row in observations["attempts"]:
        variant, key, outcome = row["variant"], row["trial_id"], row["outcome"]
        if variant not in variants or key not in known or key in variants[variant]:
            raise ValueError("Unknown or duplicate variant/trial")
        if outcome not in ("success", "failure", "timeout"):
            raise ValueError("Unknown outcome")
        latency = number(row["latency_ms"], "latency_ms")
        cost = number(row["cost"], "cost")
        variants[variant][key] = (outcome, latency, cost)
    missing = {v: sorted(known - attempts.keys()) for v, attempts in variants.items()}
    paired = len(variants["baseline"].keys() & variants["candidate"].keys())
    report = {"protocol_id": identifier, "paired": paired, "planned": len(keys), "missing": missing}
    if any(missing.values()):
        return report | {"status": "incomplete"}

    def metrics(attempts):
        rows = list(attempts.values())
        n = len(rows)
        successes = sum(row[0] == "success" for row in rows)
        return {"successes": successes, "attempts": n, "success_rate": successes / n,
                "timeouts": sum(row[0] == "timeout" for row in rows),
                "p95_ms": sorted(row[1] for row in rows)[math.ceil(.95 * n) - 1],
                "mean_cost": math.fsum(row[2] / n for row in rows)}

    baseline, candidate = (metrics(variants[v]) for v in ("baseline", "candidate"))
    effects = {k: candidate[k] - baseline[k] for k in ("success_rate", "p95_ms", "mean_cost")}
    gates = {"success_floor": candidate["success_rate"] >= floor,
             "success_delta": effects["success_rate"] + 1e-12 >= delta,
             "latency_cap": candidate["p95_ms"] <= p95_max,
             "cost_cap": candidate["mean_cost"] <= cost_max}
    result = report | {"status": "passed" if all(gates.values()) else "failed",
                       "baseline": baseline, "candidate": candidate, "delta": effects, "gates": gates}
    if groups:
        paired_effects = {}
        for key in keys:
            change = (int(variants["candidate"][key][0] == "success")
                      - int(variants["baseline"][key][0] == "success"))
            paired_effects.setdefault(groups[key], []).append(change)
        values = [math.fsum(paired_effects[g]) / len(paired_effects[g]) for g in sorted(paired_effects)]
        result["task_cluster_success"] = cluster_interval(values, bootstrap_seed)
    return result


def cluster_interval(values, seed):
    n = len(values)
    result = {"clusters": n, "equal_task_delta": math.fsum(values) / n, "interval_95": None,
              "status": "insufficient_clusters"}
    if n < 8:
        return result
    rng = random.Random(seed)
    draws = 2_000
    samples = sorted(math.fsum(rng.choices(values, k=n)) / n for _ in range(draws))
    return result | {"interval_95": [samples[49], samples[1949]], "seed": seed, "draws": draws,
                     "status": "percentile_cluster_bootstrap"}


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
    parser.add_argument("protocol", type=Path)
    parser.add_argument("observations", type=Path)
    args = parser.parse_args()
    try:
        report = compare(*(read_json(path) for path in (args.protocol, args.observations)))
    except (ValueError, TypeError, KeyError, OSError, OverflowError, RecursionError) as exc:
        parser.exit(2, f"Invalid experiment: {exc}\n")
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["status"] == "passed" else 1)


if __name__ == "__main__":
    main()
