---
name: skill-orchestrator
description: "Recommend and compose advanced AI engineering skills for a task. Use when asked to choose skills, route an AI engineering workflow, or explain why no specialized skill is needed."
metadata:
  author: AAES
  version: "0.1.0"
---

# Skill Orchestrator

Route by requested outcome and authorized mode.

## Procedure

Extract the deliverable, primary outcome, independent secondary outcomes, complexity, risk, and explicit restrictions. Classify by what must be produced, not by words in the prompt. Use the capability identifiers in [the registry](references/catalog.json); leave uncertain matches out and state the missing distinction.

For recommendation, classify into the [routing contract](references/TECHNICAL_GUIDE.md) and run `python scripts/route.py request.json` when available. Without Python, apply the same ordering and hard gates manually. For execution, use the same decision and open only selected skills available through the host; dispatch only authorized actions. Explicit skill requests take precedence within scope; an unknown skill remains the host's responsibility.

Prefer a single skill if it delivers the outcome. Compose only for distinct deliverables or a declared hard dependency. Preserve read-only, offline, budget, and approval constraints through every handoff. Parallelize only independent, authorized operations on disjoint state; merge against a shared definition of done. If there is no material match, abstain. Explain missing tools and permissions without inventing dispatch.

## Deliverable

Return task classification, mode, ordered recommendations with evidence, material exclusions, verification needs, and dispatch or approval status. Do not treat inferred risk as a grant of authority.

Example: Recommend skills for read-only investigation of an agent trace: choose trajectory analysis; include research only if the user also needs external evidence.

For more scenarios read [use cases](references/USE_CASES.md). For the scientific basis and limits read [research basis](references/RESEARCH_BASIS.md).
