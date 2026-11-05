"""Persist and reconcile a local milestone journal; never executes work."""
import argparse
from contextlib import closing
import json
from pathlib import Path
import sqlite3


def encoded(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), allow_nan=False)


def validate_plan(plan):
    steps = plan["steps"]
    if type(plan["run_id"]) is not str or not plan["run_id"].strip():
        raise ValueError("Expected run_id")
    if not isinstance(steps, list) or not 1 <= len(steps) <= 256:
        raise ValueError("Expected 1 to 256 steps")
    ids = set()
    for step in steps:
        key, tries = step["id"], step["max_attempts"]
        if type(key) is not str or not key or key in ids or type(tries) is not int or not 1 <= tries <= 100:
            raise ValueError("Invalid step ID or attempt limit")
        ids.add(key)


def apply(plan, state, event):
    index, count = state["index"], state["attempts"]
    if index == len(plan["steps"]):
        raise ValueError("Run already complete")
    step = plan["steps"][index]
    if event["step"] != step["id"] or event["kind"] not in ("claim", "verified", "no_effect", "abort"):
        raise ValueError("Event must target the active milestone")
    kind, operation = event["kind"], event["operation"]
    if type(operation) is not str or not operation.strip():
        raise ValueError("Expected operation identifier")
    if kind == "claim":
        if state["phase"] != "ready":
            raise ValueError("A new claim needs a ready milestone; reconcile the existing claim first")
        if state["operation"] is not None and operation != state["operation"]:
            raise ValueError("Use the same idempotency key on a retry")
        if operation in state["completed_operations"]:
            raise ValueError("Operation key already completed in this run")
        return state | {"phase": "in_flight", "operation": operation, "attempts": count + 1}
    if state["phase"] != "in_flight" or state["operation"] != operation:
        raise ValueError("Observation must match an in-flight operation")
    evidence = event["evidence"]
    if type(evidence) is not str or not evidence.strip():
        raise ValueError("Independent evidence reference required")
    if kind == "verified":
        return state | {"index": index + 1, "phase": "done" if index + 1 == len(plan["steps"]) else "ready",
                        "attempts": 0, "operation": None, "last_evidence": evidence,
                        "completed_operations": state["completed_operations"] + [operation]}
    return state | {"phase": "ready" if kind == "no_effect" and count < step["max_attempts"] else "blocked",
                    "last_evidence": evidence}


def transact(path, command, data=None):
    if command != "init" and not path.is_file():
        raise ValueError("Initialize the checkpoint first")
    with closing(sqlite3.connect(path, timeout=5, isolation_level=None)) as db:
        db.execute("BEGIN IMMEDIATE")
        try:
            if command == "init":
                validate_plan(data)
                db.execute("CREATE TABLE IF NOT EXISTS run (id INTEGER PRIMARY KEY CHECK(id=1), plan TEXT, state TEXT)")
                db.execute("CREATE TABLE IF NOT EXISTS events (id TEXT PRIMARY KEY, event TEXT NOT NULL)")
                plan = db.execute("SELECT plan FROM run WHERE id=1").fetchone()
                if plan is None:
                    state = {"index": 0, "attempts": 0, "phase": "ready", "operation": None,
                             "last_evidence": None, "completed_operations": []}
                    db.execute("INSERT INTO run VALUES (1, ?, ?)", (encoded(data), encoded(state)))
                elif plan[0] != encoded(data):
                    raise ValueError("Cannot replace the initialized plan")
            row = db.execute("SELECT plan, state FROM run WHERE id=1").fetchone()
            if row is None:
                raise ValueError("Checkpoint is not initialized")
            plan, state = map(json.loads, row)
            duplicate = False
            if command == "record":
                key = data["id"]
                if type(key) is not str or not key.strip():
                    raise ValueError("Expected event ID")
                body = encoded(data)
                previous = db.execute("SELECT event FROM events WHERE id=?", (key,)).fetchone()
                if previous:
                    if previous[0] != body:
                        raise ValueError("Event ID reused with a different payload")
                    duplicate = True
                else:
                    state = apply(plan, state, data)
                    db.execute("INSERT INTO events VALUES (?, ?)", (key, body))
                    db.execute("UPDATE run SET state=? WHERE id=1", (encoded(state),))
            db.execute("COMMIT")
        except Exception:
            db.execute("ROLLBACK")
            raise
    phase = state["phase"]
    return {"run_id": plan["run_id"], "step": None if phase == "done" else plan["steps"][state["index"]]["id"],
            "next": {"ready":"claim", "in_flight":"reconcile", "done":"stop", "blocked":"operator_review"}[phase],
            "duplicate_event": duplicate, "state": state}


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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["init", "record", "status"])
    parser.add_argument("db", type=Path)
    parser.add_argument("input", type=Path, nargs="?")
    args = parser.parse_args()
    if (args.command == "status") == bool(args.input):
        parser.error("init and record need input JSON; status does not")
    try:
        data = None
        if args.input:
            with args.input.open("rb") as stream:
                raw = stream.read(2_000_001)
            if len(raw) > 2_000_000:
                raise ValueError("Input exceeds 2 MB")
            data = json.loads(raw, object_pairs_hook=_pairs, parse_constant=_nonfinite)
        print(json.dumps(transact(args.db, args.command, data), indent=2))
    except (ValueError, TypeError, KeyError, OSError, sqlite3.Error, RecursionError) as exc:
        parser.exit(2, f"Invalid checkpoint operation: {exc}\n")


if __name__ == "__main__":
    main()
