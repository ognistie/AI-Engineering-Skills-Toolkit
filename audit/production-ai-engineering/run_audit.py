"""Reproduce the independent audit without changing the checkout under review."""
import argparse
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import platform
import sys
from tempfile import TemporaryDirectory

from functional import run

HERE = Path(__file__).resolve().parent


def load(path):
    spec = importlib.util.spec_from_file_location("aaes_audit_" + path.parent.parent.name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fingerprint(root):
    files = list((root/"skills").rglob("*")) + list((root/"tools").rglob("*"))
    files += list((root/"scripts").glob("*.py")) + list((root/"dist").glob("*.zip"))
    return {path.relative_to(root).as_posix():sha256(path.read_bytes()).hexdigest()
            for path in sorted(files) if path.is_file() and "__pycache__" not in path.parts}


def route_cases(root):
    fixtures = sorted((HERE/"fixtures").glob("routing-*.json"))
    # Load and fingerprint labels before calling route(). They were authored independently of predictions.
    raw = [file.read_bytes() for file in fixtures]
    cases = [case for data in raw for case in json.loads(data)]
    if len(cases) < 75 or len({row["id"] for row in cases}) != len(cases):
        raise ValueError("Incomplete or duplicate route audit cases")
    label_digest = sha256(b"".join(raw)).hexdigest()
    route=load(root/"skills/skill-orchestrator/scripts/route.py")
    scorer=load(root/"evals/score_routing.py")
    catalog = json.loads(route.CATALOG.read_text(encoding="utf-8"))["skills"]
    outputs = {row["id"]:route.route(row["classification"],catalog) for row in cases}
    mismatches = []
    for case in cases:
        row=outputs[case["id"]]
        actual=[item["skill"] for item in row["selected"]]
        expected=case["expected"]
        policy={key:{"expected":value,"actual":row.get(key)}
                for key,value in expected["policy"].items() if row.get(key)!=value}
        if actual != expected["skills"] or policy:
            mismatches.append({"id":case["id"],"selected":actual,"expected":expected["skills"],"policy":policy,
                               "selection_modes":[item["mode"] for item in row["selected"]]})
    return {"fixture_digest":label_digest,"metrics":scorer.score(cases,outputs,3),
            "mismatches":mismatches,"outputs":outputs}


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--repo",type=Path,required=True)
    cli.add_argument("--out",type=Path,required=True)
    cli.add_argument("--require-clean",action="store_true",help="Fail if an audit control differs from its expectation")
    args = cli.parse_args()
    root = args.repo.resolve(strict=True)
    out = args.out.resolve()
    if out.is_relative_to(root) and not out.is_relative_to(root/"audit"):
        cli.error("Write results outside the checkout or inside its audit/ directory")
    expected_skills = json.loads((root/"skills/skill-orchestrator/references/catalog.json").read_text(encoding="utf-8"))["skills"]
    before = fingerprint(root)
    contract_dir = root/"tools/production"
    sys.path.insert(0,str(contract_dir))

    def module(skill, filename="check.py"):
        if skill not in expected_skills:
            raise ValueError(skill)
        return load(root/"skills"/skill/"scripts"/filename)

    modules={}
    def checker(skill):
        if skill not in modules:
            modules[skill]=module(skill).analyze
        return modules[skill]

    with TemporaryDirectory() as tmp:
        rows,perf,race=run(root,Path(tmp),checker,module)
    routes=route_cases(root)
    if fingerprint(root) != before:
        raise RuntimeError("Audit changed skill, tool, installer or ZIP files")
    result={"environment":{"platform":platform.system(),"python":platform.python_version()},
            "inventory":{"skills":len(expected_skills),"tested_expansion_skills":len({row["skill"] for row in rows})},
            "input_hashes":before,"functional":rows,"catalog_exposure":perf,
            "durable_concurrency_probe":race,"routing":routes,
            "live_model_trials":"not_run","live_gpu_trials":"not_run"}
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"functional":len(rows),"observed_mismatches":[r["id"] for r in rows if not r["met"]],
                      "routing":routes["metrics"],"routing_mismatches":routes["mismatches"],
                      "catalog_exposure":perf,"race":race},indent=2))
    if args.require_clean and (any(not row["met"] for row in rows) or routes["mismatches"]
                              or routes["metrics"]["restriction_check_case_rate"] != 1):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
