# Operating contract

Run `python scripts/check.py input.json` from this skill directory (Python 3.12+, standard library). Set `schema_version` to 1. The result is a JSON report; input errors exit 2. A valid report may indicate a failure or an incomplete check. Inspect its decision before taking action.

Pass `trusted_controls` {control:[sinks]}, `active_control`, `trusted_labels` {data_id:[labels]}, and `sinks` {sink:[labels]} from the executor. Build `trusted_binding` {control,sink,source_ids,artifact_sha256} from the complete lineage of the immutable output and its SHA-256. The untrusted `action` supplies {control,sink,inputs,artifact_sha256}. The proposed sources must match the trusted set exactly and must be nonempty. Missing binding, changed bytes (a different digest), an omitted source or a different route fails closed.

Never construct the trusted binding from the model proposal. Resolve the complete transitive source set and calculate the digest from the exact bytes to be emitted. The host must verify those immutable bytes again at dispatch; the helper compares records and cannot attest actual payload bytes or provide credentialed enforcement.

Use a fixed baseline and retain the underlying evidence to reproduce the decision.
