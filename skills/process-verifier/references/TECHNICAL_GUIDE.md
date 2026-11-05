# Evidence contract

`python scripts/verify.py contract.json observations.json`

- Contract: `{"run_id":"r7","gates":[{"key":"refund_count","source":"ledger","equals":1}]}`
- Observations: `{"run_id":"r7","observations":[{"id":"e7","key":"refund_count","source":"ledger","value":1}]}`
- Read the contract from trusted reviewer-owned storage. The source label is a join key, not identity authentication. Keep the evidence collector outside the candidate's mutation scope and inspect it before using the helper.
- Strict JSON equality distinguishes numbers from booleans and decimal from integer representations. Normalize domain units and formats upstream. Missing and disputed gates are inconclusive; an observed mismatch fails. Exit 0 passed, 1 failed/inconclusive, 2 invalid input.
