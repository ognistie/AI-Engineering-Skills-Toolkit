# Implementation changes

| Issue and evidence | Change | Validation / residual risk |
| --- | --- | --- |
| Existing installation exposed management syntax as the only entry point | Added PowerShell and POSIX install commands plus an agent-readable INSTALL.md. Kept existing receipt and backup semantics | Smoke verifies both documented entry points, path with spaces, a single skill, collisions, all skills and ZIP parity; no app activation claim |
| Router assigned the primary capability to any explicitly named skill | Records the mismatch, returns it as unmet and blocks dispatch; reason for abstention/partial result is explicit | Regression and 64 policy cases; independent raw-prompt review still not host activation |
| Legacy JSON readers accepted ambiguous or non-finite values | Bounded, strict loaders in route, verifier, trace and experiment helpers | Duplicate and non-finite controls; no guarantee of observation truth |
| Evidence grouping was descriptive only | New offline research ledger validator and conflicting-source fixture | Groups duplicate citations, identifies unsubstantiated claims; source authenticity unverified |
| Verification could be crowded out; delegation estimates omitted budget | Added verification reserve and optional cost ceiling for schedules | Regression plus fixed-policy and topology controls; model cost unverified |
| Resumed operations could change environment outside journal semantics | Optional frozen scope binding and process restart test | Reconciliation retained; real provider verification remains external |
| Pareto work unbounded and no measured search example | Bounded archive cardinality and executable development/holdout comparison | Toy result only; no arbitrary code execution |
| Trial-weighted estimate can overrepresent repeated tasks | Optional equal-task effect and clustered percentile interval with small-sample guard | Weighting and constant-effect controls; assumptions in technical guide |
| State-dependent reward could trust a success label | Optional environment success-state check | Spoofed state and unsafe action controls; no training |
| Research bases did not consistently explain applicability | Expanded all 13 local research bases and technical guides; kept entrypoints concise | Resource and structure validation; see [research fidelity](RESEARCH_GAP_ANALYSIS.md) |
