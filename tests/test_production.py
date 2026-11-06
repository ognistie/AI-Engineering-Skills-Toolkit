"""Outcome controls for all 15 engineering skills and their shared boundaries."""
from hashlib import sha256
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest

from test_aaes import ROOT, helper, load

FIXTURES = ROOT / "evals/production-fixtures"
SHARED = ROOT / "tools/production"
sys.path.insert(0, str(SHARED))
try:
    MODULES = {p.stem: helper(p.stem, "check.py") for p in FIXTURES.glob("*.json")}
finally:
    sys.path.pop(0)


def fixture(name):
    return json.loads((FIXTURES / (name + ".json")).read_text(encoding="utf-8"))


def check(name, doc):
    return MODULES[name].analyze(doc)


class ProductionContracts(unittest.TestCase):
    def test_portable_contract_copies_and_command(self):
        self.assertEqual(len(MODULES), 15)
        contract = (SHARED / "_contract.py").read_bytes()
        for name, module in MODULES.items():
            with self.subTest(skill=name):
                self.assertEqual(Path(module.__file__).with_name("_contract.py").read_bytes(), contract)
                result = subprocess.run([sys.executable, "-B", module.__file__, str(FIXTURES / (name + ".json"))],
                                        cwd=ROOT, capture_output=True, timeout=10)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIsInstance(json.loads(result.stdout), dict)

    def test_harness_distinguishes_missing_stale_and_failed_evidence(self):
        name = "agent-first-harness"
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for path in ("README.md", "lint.py", "test.py"):
                (root / path).write_text("# fixture", encoding="utf-8")
            report = check(name, fixture(name) | {"root":temp})
            self.assertEqual(report["command_evidence"], {"build":"missing_entrypoint","lint":"unverified","test":"failed"})
            self.assertIn("missing_agent_entrypoint", report["findings"])
            (root / "AGENTS.md").write_text("x"*20, encoding="utf-8")
            self.assertIn("oversized_agent_entrypoint", check(name, fixture(name) | {
                "root":temp,"max_entrypoint_bytes":5})["findings"])

    def test_aci_validates_arguments_and_reports_bad_schema(self):
        name = "agent-computer-interface"
        doc = fixture(name)
        calls = check(name, doc)["calls"]
        self.assertTrue(calls[0]["valid"])
        self.assertEqual(calls[1]["errors"], ["wrong_type:limit"])
        doc["calls"][0]["arguments"]["limit"] = 5.0
        self.assertTrue(check(name, doc)["calls"][0]["valid"])
        doc["tools"][0]["schema"]["required"].append("scope")
        self.assertIn("required_field_missing_definition", [row["code"] for row in check(name, doc)["findings"]])

    def test_repo_map_conflicts_links_and_revision(self):
        name = "repository-context-architecture"
        with tempfile.TemporaryDirectory() as temp:
            docs = Path(temp) / "docs"
            docs.mkdir()
            for filename in ("overview.md", "copy.md"):
                (docs / filename).write_text("[bad](missing.md)\n[escape](../../private.md)\n", encoding="utf-8")
            report = check(name, fixture(name) | {"root":temp})
            self.assertEqual({row[0] for row in report["findings"]},
                             {"canonical_conflict","duplicate_content","revision_mismatch","broken_link","link_outside_repository"})

    def test_repo_map_reads_titles_and_ignores_nested_fence_example(self):
        name = "repository-context-architecture"
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root/"exists.md").write_text("# Present",encoding="utf-8")
            (root/"map.md").write_text(
                "[present](exists.md \"title\")\n"
                "[missing](<not here.md>\n 'title')\n"
                "~~~markdown\n~~\n[ignored](fake.md)\n~~~\n",
                encoding="utf-8")
            report = check(name,{"root":temp,"revision":"r","documents":[{"path":"map.md","topic":"docs"}]})
            self.assertEqual(report["findings"],[["broken_link","map.md","not here.md"]])

    def test_cache_telemetry_is_not_inferred_from_prefix(self):
        name = "kv-cache-aware-context"
        doc = fixture(name)
        result = check(name, doc)
        self.assertEqual(result["stable_segments"], 1)
        self.assertEqual(result["observed_provider_usage"]["candidate"]["cached_token_fraction"], .6)
        doc["candidate"].reverse()
        self.assertEqual(check(name, doc | {"observations":[]})["stable_segments"], 0)
        self.assertIsNone(check(name, doc | {"observations":[]})["observed_provider_usage"])

    def test_compaction_preserves_scope_errors_and_artifact_content(self):
        name = "context-compaction-recovery"
        doc = fixture(name)
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "evidence.json"
            original = b"expected"
            path.write_bytes(original)
            for key in ("original","restored"):
                doc[key]["artifacts"] = [{"path":path.name,"sha256":sha256(original).hexdigest()}]
            self.assertEqual(check(name, doc)["status"], "artifacts_unverified")
            self.assertEqual(check(name, doc | {"root":temp})["status"], "matched")
            doc["restored"]["constraints"] = []
            doc["restored"]["errors"] = []
            path.write_bytes(b"changed")
            bad = check(name, doc | {"root":temp})
            self.assertEqual(bad["changed_fields"], ["constraints","errors"])
            self.assertEqual(bad["artifact_mismatches"], [path.name])

    def test_serving_estimate_accounts_for_pages_shards_and_headroom(self):
        name = "inference-serving-architect"
        doc = fixture(name)
        result = check(name, doc)
        self.assertEqual(result["kv_bytes_per_token_per_gpu"], 65536)
        self.assertEqual(result["allocated_tokens_per_sequence"], 32)
        self.assertEqual(result["max_sequences_by_kv"], 3)
        self.assertFalse(result["fits_modeled_memory"])
        self.assertFalse(result["measured"])
        with self.assertRaises(ValueError):
            check(name, doc | {"kv_shards":3})

    def test_agent_trials_reject_text_only_success_and_incomplete_metrics(self):
        name = "agent-evals-engineer"
        doc = fixture(name)
        result = check(name, doc)
        self.assertEqual(result["macro"], {"pass@1":.75,"pass@k":1.0,"pass^k":.5})
        self.assertTrue(result["human_review"][-1]["judge_disagrees"])
        del doc["tasks"][0]["trials"][-1]["outcome_ref"]
        self.assertIsNone(check(name, doc)["macro"])

    def test_agent_trials_reject_replay_wrong_trial_and_candidate_state(self):
        name = "agent-evals-engineer"
        doc = fixture(name)
        doc["tasks"][0]["trials"][1]["outcome_ref"] = "ledger-0"
        with self.assertRaisesRegex(ValueError,"reused or mismatched"):
            check(name,doc)
        doc = fixture(name)
        doc["tasks"][0]["trials"][1]["id"] = "not-planned"
        with self.assertRaisesRegex(ValueError,"outside the frozen"):
            check(name,doc)
        doc = fixture(name)
        doc["trusted_outcomes"]["ledger-1"]["run_id"] = doc["trusted_outcomes"]["ledger-0"]["run_id"]
        with self.assertRaisesRegex(ValueError,"Replayed evidence"):
            check(name,doc)
        doc = fixture(name)
        doc["tasks"][0]["trials"][3]["observed"] = {"count":1}
        with self.assertRaisesRegex(ValueError,"only in the trusted"):
            check(name,doc)

    def test_trajectory_review_uses_existing_span_order_and_flags_stall(self):
        name = "trajectory-review-engine"
        doc = fixture(name)
        summarize = helper("trajectory-analyzer", "summarize.py").summarize
        spans = [{"id":f"t{i}","start_ms":i,"end_ms":i+1,"status":"timeout"} for i in (2,3,1)]
        doc["events"].reverse()
        doc["span_summary"] = summarize({"trace_id":"trace","spans":spans})
        report = check(name, doc)
        self.assertEqual(report["loop_candidates"][0]["events"], ["t1","t2","t3"])
        self.assertTrue(report["outcome_disagreement"])
        doc["events"][0]["state"] = "progress"
        self.assertEqual(check(name, doc)["loop_candidates"], [])

    def test_trajectory_interleaved_reads_do_not_reset_unrelated_stall(self):
        name = "trajectory-review-engine"
        doc = fixture(name)
        a,b,c = doc["events"]
        reads = [{"id":f"l{i}","operation":"read-log","status":"ok","state":"unchanged"} for i in (1,2)]
        doc["events"] = [a,reads[0],b,reads[1],c]
        self.assertEqual(check(name,doc)["loop_candidates"][0]["events"],["t1","t2","t3"])
        b["status"] = "ok"
        self.assertEqual(check(name,doc)["loop_candidates"],[])

    def test_refinement_preserves_verified_candidate_and_budget(self):
        name = "evaluator-optimizer-loop"
        doc = fixture(name)
        result = check(name, doc)
        self.assertEqual(result["reason"], "budget_limit")
        self.assertEqual(result["best_verified"]["score"], .76)
        self.assertEqual(check(name, doc | {"budget":10})["decision"], "continue")
        doc["history"][1]["verified"] = True
        self.assertEqual(check(name, doc)["reason"], "verified_target")

    def test_durable_advisor_uses_existing_persisted_claim(self):
        name = "durable-execution-engine"
        journal = helper("long-horizon-executor", "checkpoint.py").transact
        with tempfile.TemporaryDirectory() as temp:
            db = Path(temp) / "journal.db"
            plan = {"run_id":"refund","steps":[{"id":"refund","max_attempts":2}]}
            journal(db, "init", plan)
            claim = {"id":"c1","step":"refund","kind":"claim","operation":"p7"}
            journal(db, "record", claim)
            doc = fixture(name) | {"journal":journal(db, "status")}
            self.assertEqual(check(name, doc), {"decision":"reconcile","operation":"p7","claim_id":"c1"})
            observed = claim | {"id":"obs","kind":"no_effect","claim_id":"c1","evidence":"provider:terminal"}
            doc["journal"] = journal(db, "record", observed)
            self.assertEqual(check(name, doc)["decision"], "stop_budget")
            self.assertEqual(check(name, doc | {"elapsed_ms":0})["operation"], "p7")

    def test_durable_demo_reconciles_before_and_after_effect_across_processes(self):
        script = ROOT / "skills/durable-execution-engine/scripts/demo.py"
        journal = ROOT / "skills/long-horizon-executor/scripts/checkpoint.py"
        with tempfile.TemporaryDirectory() as temp:
            def run(folder, *args):
                result = subprocess.run([sys.executable, "-B", str(script), str(Path(temp) / folder),
                                         "--journal-helper", str(journal), *args],
                                        capture_output=True, timeout=10)
                self.assertEqual(result.returncode, 0, result.stderr)
                return json.loads(result.stdout)
            self.assertEqual(run("after", "--interrupt", "after-effect")["effects"], 1)
            self.assertEqual(run("after"), {"phase":"done","effects":1,"next":"stop"})
            self.assertEqual(run("after")["effects"], 1)
            self.assertEqual(run("before", "--interrupt", "before-effect")["effects"], 0)
            self.assertEqual(run("before"), {"phase":"ready","effects":0,"next":"claim"})
            self.assertEqual(run("before")["phase"], "done")

    def test_durable_demo_refuses_concurrent_operator_before_journal(self):
        script = ROOT / "skills/durable-execution-engine/scripts/demo.py"
        journal = ROOT / "skills/long-horizon-executor/scripts/checkpoint.py"
        with tempfile.TemporaryDirectory() as temp:
            db = sqlite3.connect(Path(temp)/"operator.db")
            args = [sys.executable,"-B",str(script),temp,"--journal-helper",str(journal)]
            try:
                db.execute("BEGIN IMMEDIATE")
                result = subprocess.run(args,capture_output=True,timeout=10)
                self.assertEqual(result.returncode,2)
                self.assertIn(b"Another operator",result.stderr)
                self.assertFalse((Path(temp)/"journal.db").exists())
            finally:
                db.close()
            result = subprocess.run(args,capture_output=True,timeout=10)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(json.loads(result.stdout)["effects"],1)

    def test_executor_preflights_all_before_any_handler(self):
        mod = MODULES["brain-tool-runtime-separation"]
        doc = fixture("brain-tool-runtime-separation")
        calls = []
        handlers = {"read":lambda target: calls.append(target)}
        bad = doc["plan"] + [{"id":"a2","tool":"read","resource":"case/2","allow":True}]
        self.assertEqual(mod.dispatch(bad, doc["trusted_permissions"], handlers)["decision"], "deny")
        self.assertEqual(calls, [])
        self.assertEqual(mod.dispatch(doc["plan"], doc["trusted_permissions"], handlers)["decision"], "dispatched")
        self.assertEqual(calls, ["case/1"])

    def test_tool_shortlist_does_not_expose_denied_tool_or_exceed_budget(self):
        name = "agent-tool-interface-design"
        doc = fixture(name)
        result = check(name, doc)
        self.assertEqual([tool["id"] for tool in result["selected"]], ["case.read"])
        self.assertEqual(check(name, doc | {"max_bytes":2})["decision"], "abstain")

    def test_capability_rejects_expansion_and_expiry(self):
        name = "capability-security-architect"
        doc = fixture(name)
        self.assertEqual(check(name, doc)["decision"], "allow")
        self.assertEqual(check(name, doc | {"now":15})["reason"], "expiry")
        doc["child"]["effects"].append("write")
        self.assertEqual(check(name, doc)["reason"], "scope_expansion")

    def test_flow_keeps_privacy_across_transformation_and_blocks_control_switch(self):
        name = "prompt-injection-boundaries"
        doc = fixture(name)
        self.assertEqual(check(name, doc)["propagated_labels"], ["private","public"])
        doc["action"].update(control="authorized_export", sink="external")
        self.assertEqual(check(name, doc)["reason"], "untrusted_control_or_sink")
        doc["active_control"] = "authorized_export"
        doc["trusted_binding"].update(control="authorized_export",sink="external")
        self.assertEqual(check(name,doc)["blocked_labels"],["private"])

    def test_flow_rejects_omitted_origins_missing_binding_and_substituted_artifact(self):
        name = "prompt-injection-boundaries"
        doc = fixture(name)
        doc["active_control"] = "authorized_export"
        doc["trusted_binding"].update(control="authorized_export",sink="external")
        doc["action"].update(control="authorized_export",sink="external",inputs=["ticket"])
        self.assertEqual(check(name,doc)["reason"],"source_binding_mismatch")
        self.assertEqual(check(name,doc|{"trusted_binding":None})["reason"],"missing_trusted_binding")
        doc["trusted_binding"]["source_ids"] = ["ticket"]
        self.assertEqual(check(name,doc)["decision"],"allow")
        doc["action"]["artifact_sha256"] = "b"*64
        self.assertEqual(check(name,doc)["reason"],"artifact_or_route_binding_mismatch")

    def test_monitor_blocks_before_effect_and_retains_last_valid_state(self):
        name = "runtime-verification-engine"
        doc = fixture(name)
        self.assertEqual(check(name, doc)["state"], "published")
        doc["events"][-1]["units"] = 2
        result = check(name, doc)
        self.assertEqual((result["violation"],result["state"],result["spent"]), ("budget_exhausted","approved",1))
        doc["events"][-1]["id"] = doc["events"][0]["id"]
        self.assertEqual(check(name, doc)["violation"], "replay")

    def test_flow_and_monitor_gate_demo_dispatch(self):
        executor = MODULES["brain-tool-runtime-separation"]
        plan = [{"id":"q","tool":"export","resource":"case/1"}]
        flow = fixture("prompt-injection-boundaries")
        flow["active_control"] = "authorized_export"
        flow["action"].update(control="authorized_export",sink="external",inputs=["ticket"])
        flow["trusted_binding"].update(control="authorized_export",sink="external",source_ids=["ticket"])
        monitor = fixture("runtime-verification-engine")
        monitor["events"] = [{"id":"q","seq":1,"action":"publish","units":1}]
        calls = []
        def policy(*args):
            return (check("prompt-injection-boundaries", flow)["decision"] == "allow"
                    and check("runtime-verification-engine", monitor)["decision"] == "allow")
        self.assertEqual(executor.dispatch(plan, {"export":["case/1"]},
                         {"export":lambda resource: calls.append(resource)}, policy)["decision"], "deny")
        self.assertEqual(calls, [])
