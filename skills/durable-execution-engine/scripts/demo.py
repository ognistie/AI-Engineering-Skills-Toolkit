"""Simulate a durable local effect with the existing, explicitly trusted checkpoint helper."""
import argparse
from contextlib import closing
import importlib.util
import json
from pathlib import Path
import sqlite3

PLAN = {"run_id":"demo","steps":[{"id":"record","max_attempts":2}]}
OPERATION = "demo-local-receipt"


def load_journal(path):
    spec = importlib.util.spec_from_file_location("aaes_trusted_journal", path)
    if spec is None or spec.loader is None:
        raise ValueError("Expected the trusted AAES checkpoint.py path")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.transact


def demo(directory, journal, interrupt="none"):
    directory.mkdir(parents=True, exist_ok=True)
    # This local lock covers claim, effect and reconciliation across all cooperating
    # demo invocations. SQLite releases it when the process exits or crashes.
    with closing(sqlite3.connect(directory / "operator.db", timeout=0, isolation_level=None)) as operator:
        try:
            operator.execute("BEGIN IMMEDIATE")
        except sqlite3.OperationalError as exc:
            if (getattr(exc,"sqlite_errorcode",0) & 0xff) in (sqlite3.SQLITE_BUSY,sqlite3.SQLITE_LOCKED):
                raise ValueError("Another operator owns this demo; no reconciliation attempted") from exc
            raise
        return run_locked(directory,journal,interrupt)


def run_locked(directory, journal, interrupt):
    state_file = directory / "journal.db"
    ledger_file = directory / "local-effects.db"
    status = journal(state_file, "init", PLAN)
    with closing(sqlite3.connect(ledger_file)) as ledger:
        with ledger:
            ledger.execute("CREATE TABLE IF NOT EXISTS effects (operation TEXT PRIMARY KEY)")
        if status["state"]["phase"] == "ready":
            key = f"claim-{status['state']['attempts'] + 1}"
            status = journal(state_file, "record", {"id":key,"step":"record","kind":"claim","operation":OPERATION})
            if interrupt == "before-effect":
                return {"phase":"in_flight","simulated_interruption":interrupt,"effects":0}
            with ledger:
                ledger.execute("INSERT OR IGNORE INTO effects VALUES (?)", (OPERATION,))
            if interrupt == "after-effect":
                return {"phase":"in_flight","simulated_interruption":interrupt,"effects":1}
        count = ledger.execute("SELECT COUNT(*) FROM effects WHERE operation=?", (OPERATION,)).fetchone()[0]
        if status["state"]["phase"] == "in_flight":
            claim = status["state"]["active_claim_id"]
            status = journal(state_file, "record", {"id":f"observed-{claim}","claim_id":claim,
                             "step":"record","operation":OPERATION,"kind":"verified" if count else "no_effect",
                             "evidence":"local-effects.db:present" if count else "local-effects.db:absent"})
    return {"phase":status["state"]["phase"],"effects":count,"next":status["next"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--journal-helper", required=True, type=Path,
                        help="Path to the reviewed long-horizon-executor/scripts/checkpoint.py")
    parser.add_argument("--interrupt", choices=["none","before-effect","after-effect"], default="none")
    args = parser.parse_args()
    try:
        print(json.dumps(demo(args.directory, load_journal(args.journal_helper), args.interrupt)))
    except (OSError, ValueError, KeyError, sqlite3.Error) as exc:
        parser.exit(2, f"Demo error: {exc}\n")


if __name__ == "__main__":
    main()
