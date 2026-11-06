"""Read-only assessment of declared repository entrypoints and run receipts."""
from pathlib import Path
from _contract import contained, integer, main, sequence, string


def analyze(doc):
    root = Path(doc["root"]).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("Root must be a repository directory")
    revision = string(doc["revision"], "revision")
    limit = integer(doc.get("max_entrypoint_bytes", 4096), "entrypoint limit", 1)
    findings = []
    entry = contained(root, "AGENTS.md")
    if not entry.is_file():
        findings.append("missing_agent_entrypoint")
    elif entry.stat().st_size > limit:
        findings.append("oversized_agent_entrypoint")
    if not any(contained(root, p).is_file() for p in ("README.md", "docs/architecture.md", "docs/ARCHITECTURE.md")):
        findings.append("missing_navigation_entrypoint")
    commands = {}
    for row in sequence(doc["commands"], "commands"):
        key = string(row["id"], "command ID")
        if key in commands:
            raise ValueError("Duplicate command ID")
        path = contained(root, row["path"])
        receipt = row.get("receipt")
        if not path.is_file():
            status = "missing_entrypoint"
        elif not receipt or receipt["revision"] != revision:
            status = "unverified"
        else:
            status = "passed" if integer(receipt["exit_code"], "exit code") == 0 else "failed"
        commands[key] = status
    for required in ("build", "test", "lint"):
        if required not in commands:
            findings.append(f"missing_declared_{required}")
    return {"findings": findings, "command_evidence": commands, "commands_executed": 0}


if __name__ == "__main__":
    main(analyze, __doc__)
