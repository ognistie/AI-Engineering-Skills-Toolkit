"""Run transparent, synthetic controls; never calls a model or external tool."""
import importlib.util
import json
from pathlib import Path
from random import Random

ROOT = Path(__file__).resolve().parents[1]


def load(skill, script):
    path = ROOT / "skills" / skill / "scripts" / (script + ".py")
    spec = importlib.util.spec_from_file_location(script, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verifier_control():
    verify = load("process-verifier", "verify").verify
    contract = {"run_id":"r1","gates":[{"key":"count","source":"ledger","equals":1}]}
    rows = [([("ledger",1)], "passed"), ([("ledger",0)], "failed"),
            ([("ledger",True)], "failed"), ([("model",1)], "inconclusive"),
            ([("ledger",1),("ledger",0)], "inconclusive"), ([], "inconclusive")]
    results = []
    for observations, expected in rows:
        doc = {"run_id":"r1","observations":[{"id":str(i),"key":"count","source":s,"value":v}
               for i,(s,v) in enumerate(observations)]}
        results.append((verify(contract, doc)["status"], expected))
    assert all(actual == expected for actual, expected in results)
    return {"controls":len(results), "false_passes":sum(a=="passed" and e!="passed" for a,e in results),
            "false_rejections":sum(a!="passed" and e=="passed" for a,e in results)}


def adaptive_control():
    decide = load("adaptive-reasoning", "decide").analyze
    variants = {k: {"success":0,"attempts":0,"modeled_ms":0,"cost_units":0} for k in ("fixed","adaptive")}
    # Every initial attempt costs 20ms and one unit. Some have an independent receipt.
    # The fixed policy runs a second 10ms verifier for every case. The adaptive policy
    # skips it only when independent evidence already exists.
    for already_verified in [True]*8 + [False]*4:
        doc = {"evidence":"verified" if already_verified else "disagreement",
               "limit":{"attempts":2,"ms":30,"cost_units":2},
               "spent":{"attempts":1,"ms":20,"cost_units":1},
               "next_cost":{"attempts":1,"ms":10,"cost_units":1},
               "authorized":True,"next_observation":"independent verifier"}
        decision = decide(doc)["decision"]
        for name, second in (("fixed",True), ("adaptive",decision == "verify")):
            row = variants[name]
            row["success"] += int(already_verified or second)
            row["attempts"] += 1 + int(second)
            row["modeled_ms"] += 20 + 10*int(second)
            row["cost_units"] += 1 + int(second)
    assert variants["adaptive"]["success"] == variants["fixed"]["success"] == 12
    assert variants["adaptive"]["attempts"] < variants["fixed"]["attempts"]
    return variants


def topology_control():
    schedule = load("multi-agent-router", "schedule").analyze
    fixture = json.loads((ROOT/"evals/fixtures/multi-agent-router.json").read_text(encoding="utf-8"))
    serial = schedule(fixture | {"delegation_authorized":False})
    parallel = schedule(fixture)
    assert len(serial["batches"]) == 3 and len(parallel["batches"]) == 2
    assert parallel["batches"][-1] == ["merge"]
    return {"serial_batches":serial["batches"],"parallel_batches":parallel["batches"],
            "modeled_serial_ms":serial["serial_ms"],"modeled_parallel_ms":parallel["estimated_parallel_ms"]}


def search_control():
    archive = load("evolutionary-optimizer", "archive").analyze

    def linear(items, target):
        for i, value in enumerate(items, 1):
            if value == target:
                return True, i
        return False, len(items)

    def binary(items, target):
        low, high, operations = 0, len(items), 0
        while low < high:
            mid = (low + high) // 2
            operations += 1
            value = items[mid]
            if value == target:
                return True, operations
            if value < target:
                low = mid + 1
            else:
                high = mid
        return False, operations

    def trial(search, seed):
        rng = Random(seed)
        data = list(range(0, 512, 2))
        targets = [rng.randrange(512) for _ in range(32)]
        values = set(data)
        outcomes = [(search(data, t), t in values) for t in targets]
        return {"correct":sum(result == expected for (result,_),expected in outcomes),
                "item_reads":sum(reads for (_,reads),_ in outcomes)}
    seeds = ["1","2","3"]
    functions = {"linear":linear,"binary":binary}
    variants = [{"id":name,"trials":{seed:trial(fn, int(seed)) for seed in seeds}} for name, fn in functions.items()]
    report = archive({"split":"development","seeds":seeds,"variants":variants,"objectives":{
        "correct":{"direction":"max","hard_limit":32},"item_reads":{"direction":"min"}}})
    assert set(report["frontier"]) == {"binary"}
    holdout = {name:trial(fn, 991) for name, fn in functions.items()}
    assert holdout["binary"]["correct"] == holdout["linear"]["correct"] == 32
    return {"development_frontier":report["frontier"],"frozen_candidate":"binary","holdout_seed":991,"holdout":holdout}


def patch_control():
    analyze = load("mechanistic-interpretability", "patch_metrics").analyze
    # Open toy network: two hidden activations; one uses the signal and one a nuisance.
    def hidden(signal, nuisance):
        return max(0, signal), max(0, nuisance)

    def readout(activation):
        signal, nuisance = activation
        return 2*signal - nuisance
    clean, corrupt = hidden(1,.25), hidden(0,.25)
    patched = (clean[0], corrupt[1])
    control = (corrupt[0], clean[1])
    result = analyze({"min_baseline_gap":.2,"pairs":[{"id":"toy","clean":readout(clean),"corrupt":readout(corrupt),
                                                    "patched":readout(patched),"control":readout(control)}]})
    assert result["means"]["patch_restoration"] == 1
    assert result["means"]["control_restoration"] == 0
    return result["means"]


if __name__ == "__main__":
    print(json.dumps({"type":"synthetic_controls", "verifier":verifier_control(),
                      "adaptive":adaptive_control(),"topology":topology_control(),
                      "variant_search":search_control(),"activation_patch":patch_control()}, indent=2))
