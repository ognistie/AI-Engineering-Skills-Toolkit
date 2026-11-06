import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from test_aaes import ROOT, catalog, helper, router
from test_advanced import fixture


class AuditRegression(unittest.TestCase):
    def test_explicit_routing_requires_analysis_inputs_for_dispatch(self):
        name = "inference-serving-architect"
        request = {"mode":"explicit","primary":"estimate_inference_capacity","explicit":name,
                   "available":[name],"execution_authorized":True}
        result = router.route(request,catalog)
        self.assertEqual(result["selected"][0]["mode"],"plan")
        self.assertEqual(result["dispatch"],"not_dispatched")
        self.assertEqual(router.route(request | {"inputs":["serving_config"]},catalog)["dispatch"],
                         "host_may_dispatch_within_scope")

    def test_explicit_skill_does_not_claim_unrelated_capability_or_dispatch(self):
        result = router.route({"mode":"execute", "explicit":"process-verifier",
                               "primary":"analyze_activation_patch", "execution_authorized":True,
                               "available":["process-verifier"], "inputs":["acceptance_contract","observations"]}, catalog)
        self.assertEqual(result["unmet"], ["analyze_activation_patch"])
        self.assertIsNone(result["selected"][0]["capability"])
        self.assertEqual(result["dispatch"], "not_dispatched")

    def test_malformed_inputs_cannot_silently_override_evidence(self):
        targets = {
            "skill-orchestrator": "route.py", "process-verifier": "verify.py",
            "trajectory-analyzer": "summarize.py", "experiment-evaluator": "compare.py",
        }
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "malformed.json"
            for name, script in targets.items():
                load = helper(name, script).read_json
                for content in ('{"state":"deny","state":"allow"}', '{"time":1e309}', '{"time":NaN}'):
                    with self.subTest(skill=name, content=content):
                        path.write_text(content, encoding="utf-8")
                        with self.assertRaises(ValueError):
                            load(path)

    def test_research_ledger_groups_and_missing_evidence(self):
        validate = helper("research-orchestrator", "ledger.py").validate
        doc = fixture("research-ledger")
        result = validate(doc)
        self.assertEqual(result["source_authenticity"], "not_verified")
        self.assertEqual(result["claims"]["c1"], {"status":"mixed","support_groups":["dataset-warm"],
                                                "contrary_groups":["dataset-cold"]})
        self.assertEqual(result["claims"]["c2"]["status"], "unsubstantiated")
        doc["sources"][1]["locator"] = doc["sources"][0]["locator"]
        doc["sources"][1]["group"] = "fake-replication"
        with self.assertRaises(ValueError):
            validate(doc)

    def test_adaptive_does_not_spend_reserved_verification(self):
        decide = helper("adaptive-reasoning", "decide.py").analyze
        doc = fixture("adaptive-reasoning")
        doc["spent"]["ms"] = 590
        doc["next_cost"]["ms"] = 150
        doc["verification_reserve"] = {"attempts":1,"ms":70,"cost_units":2}
        result = decide(doc | {"evidence":"uncertain"})
        self.assertEqual(result["reason"], "verification_reserve_would_be_spent")
        doc["next_cost"]["ms"] = 70
        self.assertEqual(decide(doc)["decision"], "verify")

    def test_cluster_estimate_weights_tasks_and_suppresses_small_interval(self):
        compare = helper("experiment-evaluator", "compare.py").compare
        ids = ["a1","a2","a3","b1","c1"]
        protocol = {"id":"p","trial_ids":ids,"trial_groups":dict(zip(ids, "aaabc")),
                    "gates":{"min_candidate_success":0,"min_success_delta":-1,
                             "max_candidate_p95_ms":5,"max_candidate_mean_cost":5}}
        rows = [{"trial_id":key,"variant":v,"outcome":"success" if v == "candidate" and key.startswith("a") else "failure",
                 "latency_ms":1,"cost":1} for v in ("baseline","candidate") for key in ids]
        result = compare(protocol, {"protocol_id":"p","attempts":rows})
        self.assertEqual(result["delta"]["success_rate"], .6)
        self.assertAlmostEqual(result["task_cluster_success"]["equal_task_delta"], 1/3)
        self.assertIsNone(result["task_cluster_success"]["interval_95"])
        ci = helper("experiment-evaluator", "compare.py").cluster_interval([.5] * 8, 17)
        self.assertEqual(ci["interval_95"], [.5, .5])

    def test_restart_refuses_scope_change_in_separate_processes(self):
        script = ROOT / "skills/long-horizon-executor/scripts/checkpoint.py"
        with tempfile.TemporaryDirectory() as temp:
            db = Path(temp) / "state.db"
            data = Path(temp) / "input.json"
            def run(*args, code=0):
                result = subprocess.run([sys.executable,str(script),*map(str,args)], text=True,
                                        capture_output=True, timeout=10)
                self.assertEqual(result.returncode, code, result.stderr)
                return result
            scope = "a" * 64
            plan = fixture("long-horizon-executor") | {"scope_sha256":scope}
            data.write_text(json.dumps(plan), encoding="utf-8")
            run("init", db, data)
            event = {"id":"c1","step":"payment","kind":"claim","operation":"p1","scope_sha256":scope}
            data.write_text(json.dumps(event), encoding="utf-8")
            run("record", db, data)
            self.assertEqual(json.loads(run("status", db).stdout)["next"], "reconcile")
            data.write_text(json.dumps(event | {"id":"c2","scope_sha256":"b"*64}), encoding="utf-8")
            self.assertIn("scope differs", run("record", db, data, code=2).stderr)

    def test_parallel_fallback_enforces_cost_even_when_faster(self):
        doc = fixture("multi-agent-router")
        for task in doc["tasks"]:
            task["cost_units"] = 2
        analyze = helper("multi-agent-router", "schedule.py").analyze
        doc.update(max_cost_units=6, parallel_overhead_cost_units=1)
        self.assertEqual(analyze(doc)["topology"], "sequential")
        self.assertEqual(analyze(doc | {"max_cost_units":5})["topology"], "infeasible")
        self.assertEqual(analyze(doc | {"max_cost_units":7})["topology"], "parallel_batches")

    def test_environment_gate_rejects_spoofed_success(self):
        doc = fixture("agentic-rl-lab")
        doc["environment"]["success_states"] = ["verified"]
        analyze = helper("agentic-rl-lab", "rollouts.py").analyze
        with self.assertRaises(ValueError):
            analyze(doc)
        doc["episodes"][0]["steps"][-1]["next_state"] = "verified"
        self.assertEqual(analyze(doc)["outcomes"]["success"], 1)

    def test_guardian_denies_before_mock_tool_boundary(self):
        policy = helper("runtime-guardian", "policy.py")
        doc = fixture("runtime-guardian")
        doc["action"]["tool"] = "shell-delete"
        doc["action"]["effect"] = "read"
        doc["read_only"] = True
        calls = []
        if policy.analyze(doc)["decision"] == "allow":
            calls.append(doc["action"]["tool"])
        self.assertEqual(calls, [])
