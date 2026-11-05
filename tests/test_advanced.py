from concurrent.futures import ThreadPoolExecutor
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from threading import Barrier
import unittest

from test_aaes import ROOT, helper, router, catalog

GUARD = ROOT / "skills/runtime-guardian/scripts"
sys.path.insert(0, str(GUARD))
try:
    import reservations
    import policy
finally:
    sys.path.remove(str(GUARD))


def fixture(skill):
    return json.loads((ROOT / "evals/fixtures" / (skill + ".json")).read_text(encoding="utf-8"))


class AdvancedChecks(unittest.TestCase):
    def test_adaptive_verifies_then_stops_on_budget_or_repeated_failure(self):
        name = "adaptive-reasoning"
        analyze = helper(name, "decide.py").analyze
        doc = fixture(name)
        self.assertEqual(analyze(doc)["decision"], "verify")
        doc["spent"]["attempts"] = 3
        self.assertEqual(analyze(doc)["reason"], "next_action_exceeds_budget")
        doc["evidence"] = "stalled"
        self.assertEqual(analyze(doc)["decision"], "stop")

    def test_checkpoint_reopens_and_reconciles_before_retry(self):
        name = "long-horizon-executor"
        transact = helper(name, "checkpoint.py").transact
        with tempfile.TemporaryDirectory() as temp:
            db = Path(temp) / "local.db"
            plan = fixture(name)
            transact(db, "init", plan)
            claim = {"id":"c1","step":"payment","kind":"claim","operation":"p42"}
            transact(db, "record", claim)
            self.assertEqual(transact(db, "status")["next"], "reconcile")
            self.assertTrue(transact(db, "record", claim)["duplicate_event"])
            with self.assertRaises(ValueError):
                transact(db, "record", claim | {"id":"unsafe-retry"})
            with self.assertRaises(ValueError):
                transact(db, "record", claim | {"operation":"forged"})
            self.assertEqual(transact(db, "status")["state"]["attempts"], 1)
            proof = claim | {"id":"o1","kind":"no_effect","evidence":"provider:p42-terminal-no-effect"}
            self.assertEqual(transact(db, "record", proof)["next"], "claim")
            with self.assertRaises(ValueError):
                transact(db, "record", claim | {"id":"c2","operation":"other"})
            transact(db, "record", claim | {"id":"c2"})
            complete = proof | {"id":"o2","kind":"verified","evidence":"provider:receipt/1"}
            self.assertEqual(transact(db, "record", complete)["step"], "receipt")
            transact(db, "record", claim | {"id":"c3","step":"receipt","operation":"r1"})
            self.assertEqual(transact(db, "record", complete | {"id":"o3","step":"receipt",
                             "operation":"r1"})["next"], "stop")

    def test_topology_respects_conflicts_cost_and_permission(self):
        name = "multi-agent-router"
        analyze = helper(name, "schedule.py").analyze
        doc = fixture(name)
        self.assertEqual(analyze(doc)["batches"], [["client","server"],["merge"]])
        self.assertEqual(analyze(doc | {"delegation_authorized":False})["topology"], "sequential")
        self.assertEqual(analyze(doc | {"overhead_ms":None})["topology"], "sequential")
        doc["tasks"][0]["writes"] = doc["tasks"][1]["writes"]
        self.assertEqual(analyze(doc)["topology"], "sequential")
        doc["tasks"][0]["depends_on"] = ["merge"]
        with self.assertRaises(ValueError):
            analyze(doc)

    def test_guard_rejects_edited_payload_revision_and_expired_approval(self):
        doc = fixture("runtime-guardian")
        self.assertEqual(policy.analyze(doc)["decision"], "approval_required")
        approval = {"id":"a1","expires":100,"used":False,"binding":policy.binding(doc["action"], "p1")}
        doc["approval"] = approval
        self.assertEqual(policy.analyze(doc)["decision"], "allow")
        self.assertEqual(policy.analyze(doc | {"read_only":True})["rule"], "read_only")
        self.assertEqual(policy.analyze(doc | {"now":100})["decision"], "deny")
        edited = doc["action"] | {"payload_sha256":"b"*64}
        self.assertEqual(policy.analyze(doc | {"action":edited})["decision"], "deny")
        self.assertEqual(policy.analyze(doc | {"policy":doc["policy"] | {"revision":"p2"}})["decision"], "deny")
        doc["policy"]["tools"]["publish"]["resources"] = "artifact/A"
        with self.assertRaises(ValueError):
            policy.analyze(doc)

    def test_guard_race_and_quota_use_real_transactions(self):
        doc = fixture("runtime-guardian")
        doc["approval"] = {"id":"a1","expires":100,"used":False,"binding":policy.binding(doc["action"], "p1")}
        with tempfile.TemporaryDirectory() as temp:
            db = Path(temp) / "guard.db"
            reservations.initialize(db, 1)
            self.assertFalse(reservations.reserve(db, doc, lambda: 100)["reserved"])
            barrier = Barrier(2, timeout=5)
            def run(_):
                barrier.wait()
                return reservations.reserve(db, doc, lambda: 10)
            with ThreadPoolExecutor(max_workers=2) as pool:
                results = list(pool.map(run, range(2)))
            self.assertEqual(sum(row["reserved"] for row in results), 1)
            self.assertIn("request_already_reserved", [row["rule"] for row in results])
            other = doc["action"] | {"request_id":"q6"}
            second = doc["approval"] | {"id":"a2","binding":policy.binding(other, "p1")}
            reservations.initialize(db, 100)
            self.assertEqual(reservations.reserve(db, doc | {"action":other,"approval":second}, lambda: 10)["rule"], "budget_or_timeout")

    def test_frontier_uses_worst_seed_for_hard_limits_and_blocks_holdout(self):
        name = "evolutionary-optimizer"
        analyze = helper(name, "archive.py").analyze
        doc = fixture(name)
        doc["variants"].append({"id":"better","trials":{k:{"latency":9,"quality":0.9,"memory":90} for k in ("a","b")}})
        result = analyze(doc)
        self.assertEqual(set(result["frontier"]), {"better"})
        self.assertEqual(result["dominated"], ["baseline"])
        self.assertEqual(result["rejected"], {"fast":"hard_limit:memory"})
        with self.assertRaises(ValueError):
            analyze(doc | {"split":"holdout"})

    def test_evidence_groups_do_not_outvote_a_controlled_contradiction(self):
        name = "hypothesis-lab"
        analyze = helper(name, "matrix.py").analyze
        doc = fixture(name)
        self.assertEqual(analyze(doc)["ranking"][0]["independent_support"], ["run7"])
        doc["evidence"].append({"id":"e3","group":"experiment","hypothesis":"cache",
                                "kind":"intervention","direction":"contradicts"})
        result = analyze(doc)
        self.assertEqual(result["leading_hypothesis"], "null")
        self.assertEqual(result["ranking"][1]["intervention_contradiction"], ["experiment"])

    def test_patching_retains_unclipped_effect_and_excludes_unstable_gap(self):
        name = "mechanistic-interpretability"
        analyze = helper(name, "patch_metrics.py").analyze
        doc = fixture(name)
        doc["pairs"][0]["patched"] = 3
        doc["pairs"].append({"id":"weak","clean":0.1,"corrupt":0,"patched":5,"control":0})
        result = analyze(doc)
        self.assertEqual(result["excluded_small_or_reversed_gap"], ["weak"])
        self.assertEqual(result["included"][0]["patch_restoration"], 1.5)
        self.assertAlmostEqual(result["means"]["patch_minus_control"], 1.4)

    def test_rollouts_credit_only_trusted_terminal_outcomes_and_count_unsafe(self):
        name = "agentic-rl-lab"
        analyze = helper(name, "rollouts.py").analyze
        doc = fixture(name)
        unsafe = {"id":"ep2","initial_state":"s0","steps":[{"id":"u1","state":"s0","action":"delete",
                   "next_state":"closed","outcome":"unsafe","cost":0}]}
        doc["episodes"].append(unsafe)
        result = analyze(doc)
        self.assertEqual(result["success_rate"], .5)
        self.assertEqual(result["outcomes"]["unsafe"], 1)
        self.assertAlmostEqual(result["episodes"][0]["returns_to_go"][0], .4)
        duplicate = copy.deepcopy(doc)
        duplicate["episodes"][0]["steps"].append(duplicate["episodes"][0]["steps"][-1])
        with self.assertRaises(ValueError):
            analyze(duplicate)

    def test_advanced_router_gates_tools_and_does_not_dispatch_without_inputs(self):
        row = router.route({"primary":"schedule_agent_work","tools":["subagents"],"inputs":["task_graph"],
                            "constraints":["no_delegation"]}, catalog)["selected"][0]
        self.assertEqual(row["optional_tools_available"], [])
        row = router.route({"primary":"resume_workflow","mode":"execute","execution_authorized":True,
                            "available":["long-horizon-executor"]}, catalog)
        self.assertEqual(row["dispatch"], "not_dispatched")

    def test_helper_cli_rejects_ambiguous_json(self):
        with tempfile.TemporaryDirectory() as temp:
            data = Path(temp) / "input.json"
            data.write_text('{"evidence":"verified","evidence":"blocked"}', encoding="utf-8")
            result = subprocess.run([sys.executable,str(ROOT / "skills/adaptive-reasoning/scripts/decide.py"),str(data)],
                                    capture_output=True,text=True,timeout=10)
            self.assertEqual(result.returncode, 2)
            self.assertIn("Duplicate JSON key", result.stderr)


if __name__ == "__main__":
    unittest.main()
