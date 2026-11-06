"""Check an immutable artifact binding against a trusted flow policy."""
import re

from _contract import main, string, strings

HASH = re.compile(r"[a-f0-9]{64}")


def deny(reason, **details):
    return {"decision":"deny","reason":reason} | details


def analyze(doc):
    controls = {string(key,"control"):set(strings(val,"control sink")) for key,val in doc["trusted_controls"].items()}
    sinks = {string(key,"sink"):set(strings(val,"allowed label")) for key,val in doc["sinks"].items()}
    labels = {string(key,"source"):set(strings(val,"source label")) for key,val in doc["trusted_labels"].items()}
    action = doc["action"]
    if not isinstance(action, dict) or set(action) != {"control","sink","inputs","artifact_sha256"}:
        return deny("unknown_proposal_fields")
    control, sink = string(action["control"],"control"), string(action["sink"],"sink")
    active = string(doc["active_control"],"executor-bound control")
    if control != active or sink not in controls.get(active, set()) or sink not in sinks:
        return deny("untrusted_control_or_sink")

    # The caller must derive this binding from trusted runtime state, never the model.
    binding = doc.get("trusted_binding")
    if not isinstance(binding, dict) or set(binding) != {"control","sink","source_ids","artifact_sha256"}:
        return deny("missing_trusted_binding")
    expected_hash = binding["artifact_sha256"]
    if (binding["control"] != control or binding["sink"] != sink
            or type(expected_hash) is not str or not HASH.fullmatch(expected_hash)
            or action["artifact_sha256"] != expected_hash):
        return deny("artifact_or_route_binding_mismatch")
    trusted_ids = set(strings(binding["source_ids"],"trusted source ID"))
    declared = set(strings(action["inputs"],"proposed source ID"))
    if not trusted_ids or trusted_ids != declared:
        return deny("source_binding_mismatch")
    if any(not labels.get(key) for key in trusted_ids):
        return deny("unknown_provenance")
    joined = set().union(*(labels[key] for key in trusted_ids))
    if not joined <= sinks[sink]:
        return deny("labels_not_allowed_at_sink",blocked_labels=sorted(joined-sinks[sink]))
    return {"decision":"allow","artifact_sha256":expected_hash,"propagated_labels":sorted(joined),"executed":False}


if __name__ == "__main__":
    main(analyze, __doc__)
