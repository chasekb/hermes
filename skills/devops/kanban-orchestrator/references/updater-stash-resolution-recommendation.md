# Updater stash conflict-resolution recommendation pattern

Use this pattern when a Hermes update completes the code upgrade but restoring local changes from the pre-update stash produces merge conflicts.

Capture the incident as a backlog recommendation when:
- the updater preserved a stash reference
- restore/apply surfaced conflicted paths
- the operator needs a durable recovery path for future update incidents

Record in the backlog item:
- stash ref from the updater
- conflicted file paths
- the user-facing recovery options
- the verification steps after each recovery path

Recommended recovery options to document:
1. Reapply the stash and resolve conflicts in place.
2. Restart from a clean worktree if the local changes are disposable.
3. Preserve the stash and split the work: update first, then reintroduce local changes in smaller chunks.

Verified operator path:
- The restart-from-clean-worktree path was smoke-tested in a detached worktree, confirming the clean checkout step is repeatable.
- That makes the clean-worktree fallback the preferred safe route when the local changes are not worth reconciling in place.

Good closeout criteria:
- resolution options are explicit and ordered by safety
- the verified recovery path is reproducible
- the conflict artifacts are traceable later
- the guidance tells the operator what to verify after recovery

Do not encode a one-off environment failure as policy. Capture the recovery workflow, not the transient machine state that triggered it.