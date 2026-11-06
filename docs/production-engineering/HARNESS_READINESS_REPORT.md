# Harness readiness

Inputs are a repository root, revision, and declared command entrypoints and receipts. The analyzer is read-only and never executes an entrypoint. It separates absent files, absent or stale evidence, and recorded failures. Two independent temporary fixture layouts exercise command readiness and documentation navigation.

In a real repository, trace AGENTS.md to canonical architecture, build and test targets; run selected targets only in an authorized environment. Bind test receipts to the checked-out revision. Use isolated worktrees for mutation, scoped CI credentials, structured tool/trace IDs and feedback that lets a worker reproduce a failed gate. A present command or an exit code claimed by the agent does not certify readiness.
