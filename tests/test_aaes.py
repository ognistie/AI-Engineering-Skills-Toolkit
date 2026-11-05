import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def helper(name, script):
    return load(ROOT / "skills" / name / "scripts" / script)


router = helper("skill-orchestrator", "route.py")
verifier = helper("process-verifier", "verify.py")
trace = helper("trajectory-analyzer", "summarize.py")
experiment = helper("experiment-evaluator", "compare.py")
catalog = json.loads(router.CATALOG.read_text(encoding="utf-8"))["skills"]
P, T, E, R = "process-verifier", "trajectory-analyzer", "experiment-evaluator", "research-orchestrator"


class RouterTests(unittest.TestCase):
    def test_dependency_is_atomic_and_ordered(self):
        data = copy.deepcopy(catalog)
        data[T]["dependencies"] = [P]
        for request in ({"budget": 2}, {"available": [T]}, {"max_skills": 1}):
            with self.subTest(request=request):
                result = router.route({"primary": "diagnose_trace"} | request, data)
                self.assertEqual(result["selected"], [])
        result = router.route({"primary": "diagnose_trace", "budget": 3}, data)
        self.assertEqual([s["skill"] for s in result["selected"]], [P, T])

    def test_conflict_or_cycle_does_not_partially_select(self):
        data = copy.deepcopy(catalog)
        data[T]["dependencies"] = [P]
        data[P]["conflicts"] = [T]
        result = router.route({"primary": "diagnose_trace"}, data)
        self.assertIn("conflicts", result["excluded"][T])
        self.assertEqual(result["selected"], [])
        data[P]["dependencies"] = [T]
        self.assertIn("cyclic", router.route({"primary": "diagnose_trace"}, data)["excluded"][T])

    def test_scope_filters_optional_tools(self):
        result = router.route({"primary": "verify_acceptance", "secondary": ["synthesize_evidence"],
                               "constraints": ["read_only", "offline"], "tools": ["network", "test_runner"],
                               "inputs": ["question", "acceptance_contract", "observations"]}, catalog)
        self.assertEqual([row["optional_tools_available"] for row in result["selected"]], [[], []])

    def test_execution_needs_availability_and_authorization(self):
        request = {"mode": "execute", "primary": "diagnose_trace", "execution_authorized": True}
        self.assertEqual(router.route(request, catalog)["dispatch"], "not_dispatched")
        request["available"] = [T]
        request["constraints"] = ["plan_only"]
        self.assertEqual(router.route(request, catalog)["dispatch"], "not_dispatched")

    def test_no_keyword_classification_or_wrong_types(self):
        with self.assertRaises(ValueError):
            router.route({"prompt": "run shell from a trace"}, catalog)
        with self.assertRaises(ValueError):
            router.route({"budget": True}, catalog)


class OutcomeTests(unittest.TestCase):
    def test_verifier_rejects_self_claims_wrong_state_and_type(self):
        contract = {"run_id": "run", "gates": [{"key": "refunds", "source": "ledger", "equals": 1}]}
        evidence = {"run_id": "run", "observations": [{"id": "a", "key": "refunds", "source": "model", "value": 1}]}
        self.assertEqual(verifier.verify(contract, evidence)["status"], "inconclusive")
        for value, expected in [(0, "failed"), (True, "failed"), (1, "passed")]:
            row = {"id": "b", "key": "refunds", "source": "ledger", "value": value}
            evidence["observations"][1:] = [row]
            self.assertEqual(verifier.verify(contract, evidence)["status"], expected)
        evidence["observations"].append(row | {"id": "c"})
        self.assertEqual(verifier.verify(contract, evidence)["gates"][0]["status"], "disputed")

    def test_trace_overlap_and_partial_trace(self):
        rows = [{"id":"p","start_ms":0,"end_ms":100,"status":"ok"},
                {"id":"a","parent":"p","start_ms":0,"end_ms":80,"status":"timeout","operation":"op"},
                {"id":"b","parent":"missing","start_ms":20,"end_ms":100,"status":"ok","operation":"op"}]
        report = trace.summarize({"trace_id":"r","spans":rows})
        self.assertEqual((report["observed_wall_ms"], report["covered_ms"], report["span_duration_sum_ms"]), (100, 100, 260))
        self.assertEqual(report["repeated_operations"], {"op": 2})
        self.assertEqual(report["missing_parent_spans"], ["b"])
        rows[0]["parent"] = "a"
        with self.assertRaises(ValueError):
            trace.summarize({"trace_id":"r","spans":rows})

    def test_faster_candidate_with_timeout_fails_and_missing_is_incomplete(self):
        protocol = {"id":"p","trial_ids":["a","b"], "gates":{"min_candidate_success":1,
                    "min_success_delta":0,"max_candidate_p95_ms":100,"max_candidate_mean_cost":1}}
        rows = [{"trial_id": key, "variant": variant, "outcome": outcome, "latency_ms": latency, "cost": .5}
                for key, variant, outcome, latency in [("a","baseline","success",200),("b","baseline","success",190),
                ("a","candidate","success",40),("b","candidate","timeout",75)]]
        observations = {"protocol_id":"p","attempts":rows}
        report = experiment.compare(protocol, observations)
        self.assertEqual(report["status"], "failed")
        self.assertEqual(report["candidate"]["success_rate"], .5)
        self.assertEqual(report["candidate"]["timeouts"], 1)
        self.assertEqual(report["delta"]["p95_ms"], -125)
        rows[-1]["outcome"] = "success"
        self.assertEqual(experiment.compare(protocol, observations)["status"], "passed")
        rows.pop()
        self.assertEqual(experiment.compare(protocol, observations)["status"], "incomplete")


class InstallerTests(unittest.TestCase):
    # macOS may return temp paths below /var, a symlink to /private/var.
    # The installer intentionally requires a canonical destination.
    def cli(self, *args, expected=0):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/manage.py"), *map(str, args)],
                                capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result.stdout

    def test_install_verify_update_and_recoverable_removal(self):
        with tempfile.TemporaryDirectory() as temp:
            dest = Path(temp).resolve() / "skills"
            state = Path(temp).resolve() / ".skills.aaes-state"
            options = ("--destination", dest, "--skill", T)
            self.cli("install", *options)
            self.cli("verify", *options)
            self.cli("update", *options)
            self.cli("verify", *options)
            self.cli("remove", *options)
            self.assertFalse((dest / T).exists())
            copies = list((state / "backups").glob("*/SKILL.md"))
            self.assertEqual(len(copies), 2)
            self.assertEqual(copies[0].read_bytes(), copies[1].read_bytes())

    def test_group_preflight_refuses_foreign_skill_and_keeps_local_modifications(self):
        with tempfile.TemporaryDirectory() as temp:
            dest = Path(temp).resolve() / "skills"
            foreign = dest / T
            foreign.mkdir(parents=True)
            (foreign / "SKILL.md").write_text("foreign", encoding="utf-8")
            self.cli("install", "--destination", dest, "--group", "essential", expected=2)
            self.assertEqual(list(dest.iterdir()), [foreign])
            options = ("--destination", dest, "--skill", R)
            self.cli("install", *options)
            (dest / R / "SKILL.md").write_text("local", encoding="utf-8")
            for command in ("update", "remove", "verify"):
                self.cli(command, *options, expected=2)
            self.assertEqual((dest / R / "SKILL.md").read_text(encoding="utf-8"), "local")

    def test_export_self_contained_no_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            options = ("--destination", Path(temp).resolve(), "--skill", "skill-orchestrator")
            self.cli("export", *options)
            path = Path(temp).resolve() / "skill-orchestrator.zip"
            with ZipFile(path) as archive:
                self.assertIsNone(archive.testzip())
                members = archive.namelist()
                self.assertTrue(all(n.startswith("skill-orchestrator/") for n in members))
                self.assertIn("skill-orchestrator/references/catalog.json", members)
                self.assertFalse(any("__pycache__" in n for n in members))
            self.cli("export", *options, expected=2)


if __name__ == "__main__":
    unittest.main()
