"""Reference adapter for atomic local execution reservations.

Call only with trusted policy/approval state and canonical adapter metadata.
A reservation is a one-time signal to the caller; no tool is invoked here.
"""
from contextlib import closing
import sqlite3

from policy import analyze, binding


def initialize(db_path, units):
    if type(units) is not int or units < 0:
        raise ValueError("Invalid budget")
    with closing(sqlite3.connect(db_path, timeout=5)) as db, db:
        db.execute("CREATE TABLE IF NOT EXISTS budget (id INTEGER PRIMARY KEY CHECK (id=1), remaining INTEGER NOT NULL)")
        db.execute("CREATE TABLE IF NOT EXISTS used (approval TEXT PRIMARY KEY)")
        db.execute("CREATE TABLE IF NOT EXISTS reservations (request TEXT PRIMARY KEY, binding TEXT NOT NULL)")
        # Initialization does not grant a second budget on process restart.
        db.execute("INSERT OR IGNORE INTO budget VALUES (1, ?)", (units,))


def reserve(db_path, trusted_request, clock):
    action = trusted_request["action"]
    with closing(sqlite3.connect(db_path, timeout=5, isolation_level=None)) as db:
        db.execute("BEGIN IMMEDIATE")
        try:
            remaining = db.execute("SELECT remaining FROM budget WHERE id=1").fetchone()[0]
            prior = db.execute("SELECT binding FROM reservations WHERE request=?", (action["request_id"],)).fetchone()
            if prior:
                db.execute("COMMIT")
                return {"decision": "deny", "rule": "request_already_reserved", "reserved": False}
            approval = trusted_request.get("approval")
            if approval:
                if type(approval.get("id")) is not str or not approval["id"]:
                    raise ValueError("Trusted approval needs a stable ID")
                used = db.execute("SELECT 1 FROM used WHERE approval=?", (approval["id"],)).fetchone()
                approval = approval | {"used": True} if used else approval
            result = analyze(trusted_request | {"remaining_units": remaining, "approval": approval, "now": clock()})
            reserved = result["decision"] == "allow"
            if reserved:
                digest = binding(action, trusted_request["policy"]["revision"])
                db.execute("INSERT INTO reservations VALUES (?, ?)", (action["request_id"], digest))
                if result["rule"] == "trusted_approval_requires_atomic_consumption":
                    db.execute("INSERT INTO used VALUES (?)", (approval["id"],))
                db.execute("UPDATE budget SET remaining = remaining - ? WHERE id=1", (action["units"],))
            db.execute("COMMIT")
            return result | {"reserved": reserved, "enforcement": "local_reservation_only"}
        except Exception:
            db.execute("ROLLBACK")
            raise
