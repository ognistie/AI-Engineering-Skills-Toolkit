# Production engineering expansion

This is the initial expansion report. The [independent audit and release revalidation](../../audit/production-ai-engineering/REMEDIATION.md) record later regression checks and the fixes.

AAES now contains 28 standalone skills: 13 existing and 15 new. The expansion adds versioned local tooling for harness readiness, tool interfaces, context/inference, evaluations, recovery, and runtime controls. It preserves existing span, checkpoint and guardian interfaces.

## Reproduce

```sh
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python evals/score_routing.py --annotations evals/routing/independent-annotations.json
python evals/score_routing.py --cases evals/routing/production-cases.json
python -m unittest discover -s tests -v
python evals/run_controls.py
python scripts/test_installers.py --published
```

Validation covers 55 unit and integration tests, 100 structured routing cases, and 28 installable ZIPs checked against their sources. The current changes were checked locally, including PowerShell and Git Bash destinations. There is no new hosted CI run for the local expansion.

## Report index

- [Architecture and overlap](ARCHITECTURE_REVIEW.md)
- [Scientific foundations](SCIENTIFIC_FOUNDATIONS.md)
- [Skill implementation matrix](SKILL_IMPLEMENTATION_MATRIX.md)
- [ACI review](ACI_DESIGN_REVIEW.md)
- [Harness readiness](HARNESS_READINESS_REPORT.md)
- [Evaluation results](EVAL_RESULTS.md)
- [Context efficiency](CONTEXT_EFFICIENCY.md)
- [Runtime reliability](RUNTIME_RELIABILITY.md)
- [Security validation](SECURITY_VALIDATION.md)

**Evidence boundary:** all 15 new skills are tool-assisted. The durable demo and mock security composition are local runtime integration. GPU serving, live model grading, automatic host selection, credentialed provider effects and production deployment were not validated.
