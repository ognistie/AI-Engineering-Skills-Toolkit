"""Simulate a fail-closed action policy; does not dispatch tools."""
import hashlib
import json
import re

HASH = re.compile(r"[0-9a-f]{64}\Z")
EFFECTS = {"read", "write", "external", "destructive"}


def binding(action, revision):
    canonical = json.dumps({"policy_revision": revision} | {k: action[k] for k in ("request_id", "principal", "tool", "resource", "payload_sha256",
                                                  "units", "timeout_ms")}, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def analyze(doc):
    policy, action = doc["policy"], doc["action"]
    trusted = policy["tools"]
    revision = policy["revision"]
    if type(revision) is not str or not revision.strip() or not isinstance(trusted, dict):
        raise ValueError("Invalid trusted policy")
    now, remaining = doc["now"], doc["remaining_units"]
    for v in (now, remaining, action["units"], action["timeout_ms"], policy["max_timeout_ms"]):
        if type(v) is not int or v < 0:
            raise ValueError("Expected nonnegative integers")
    if not action["units"] or not action["timeout_ms"] or not policy["max_timeout_ms"]:
        raise ValueError("Action units and timeouts must be positive")
    for key in ("request_id", "principal", "tool", "resource", "payload_sha256"):
        if type(action[key]) is not str or not action[key]:
            raise ValueError(f"Invalid action field: {key}")
    if not HASH.fullmatch(action["payload_sha256"]):
        raise ValueError("Invalid payload digest")
    read_only = doc["read_only"]
    if type(read_only) is not bool:
        raise ValueError("read_only must be boolean")

    def result(decision, rule, digest=None):
        return {"request_id": action["request_id"], "decision": decision, "rule": rule,
                "binding": digest, "enforcement": "preflight_only"}

    rule = trusted.get(action["tool"])
    if rule is None or rule["effect"] not in EFFECTS:
        return result("deny", "unclassified_tool")
    for field in ("principals", "resources"):
        if not isinstance(rule[field], list) or any(type(x) is not str or not x for x in rule[field]):
            raise ValueError("Invalid allowlist")
    if action["principal"] not in rule["principals"] or action["resource"] not in rule["resources"]:
        return result("deny", "out_of_scope")
    if read_only and rule["effect"] != "read":
        return result("deny", "read_only")
    if action["units"] > remaining or action["timeout_ms"] > policy["max_timeout_ms"]:
        return result("deny", "budget_or_timeout")
    if type(rule["approval_required"]) is not bool:
        raise ValueError("Approval rule must be boolean")
    if rule["effect"] == "read" and not rule["approval_required"]:
        return result("allow", "trusted_read")
    approval = doc.get("approval")
    digest = binding(action, revision)
    if approval is None:
        return result("approval_required", "missing_approval", digest)
    if (type(approval["expires"]) is not int or type(approval["used"]) is not bool
        or type(approval["binding"]) is not str):
        raise ValueError("Invalid approval")
    if approval["binding"] != digest or approval["expires"] <= now or approval["used"]:
        return result("deny", "approval_mismatch_expired_or_consumed", digest)
    return result("allow", "trusted_approval_requires_atomic_consumption", digest)

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
