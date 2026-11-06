# AAES engineering audit

**Scope:** 13 portable Agent Skills, installation for Codex and Claude Code, the routing registry, local helpers, and scientific fidelity. Baseline: `a1708ef`. This is an engineering audit with observed local results.

| Gate | Evidence |
| --- | --- |
| Research-grounded | Source-to-mechanism review for all 13. Research claims are bounded to the implementation. |
| Structurally valid | 13 skill entrypoints, metadata, registry and relative resources validated. |
| Functionally verified | 37 unit/regression tests; 64 deterministic routing fixtures (22 with policy checks); 5 groups of synthetic controls; 13 installations and 13 published ZIP comparisons. |
| Empirically evaluated | Six fresh paired scenarios in the audit, plus a historical paired pilot spanning the 13 skills. No aggregate model efficacy claim. |
| Production-ready | NOT VERIFIED. Actual app activation, credentialed host enforcement, real provider recovery, model-weight interventions and agent training were not verified. |

## Reproduce

```sh
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python evals/score_routing.py --annotations evals/routing/independent-annotations.json
python -m unittest discover -s tests -v
python evals/run_controls.py
python scripts/test_installers.py --published
```

The installer smoke test exercised PowerShell and Git Bash on Windows in isolated destinations. It checks install bytes and packaging, not host UI discovery. The revised workflow is configured for Windows, Linux and macOS. This audit does not assert a new remote CI run.

## Audit record

[Initial audit](INITIAL_AUDIT.md) · [Research fidelity](RESEARCH_GAP_ANALYSIS.md) · [Skill matrix](SKILL_VALIDATION_MATRIX.md) · [Routing](ROUTING_EVALUATION.md) · [Behavioral evaluation](BEHAVIORAL_EVALUATION.md) · [Security](SECURITY_FINDINGS.md) · [Changes](IMPLEMENTATION_CHANGES.md)

Prioritize a pinned, held-out host study with genuine selection traces and repeated paired trials. For production use, verify the credentialed tool boundary and reconciliation against a real test environment before claiming external safety.
