# Hermes repo branch workflow reference

This reference captures the reusable branch-and-integration pattern for the Hermes repo.

## Branch choice
- Default: one active branch per machine.
- `main` is the integration branch.
- Shared branches are only safe when the worktree is clean and the machines are strictly serialized.

## Integration pattern
1. Split branch-local changes by concern.
   - skill/doc changes
   - helper/tooling changes
   - note or backlog changes
2. Inspect each branch separately.
3. Use a synthesis branch if several branches touch the same file family.
4. Prefer rebase for short-lived machine branches.
5. Prefer merge when the branch represents a meaningful milestone or must preserve history.
6. Verify the integrated state by re-reading the updated skill/note and checking `git status`.

## Automation
- Use a small helper to report clean/dirty state, ahead/behind counts, and the next safe step.
- Keep the helper read-only so it can be run on any machine without side effects.
- Suggested path: `skills/software-development/hermes-repo-branch-workflow/scripts/repo_branch_workflow.py`

## Parallel inspection
When comparing branch-local work:
- one subagent reviews branch A
- one subagent reviews branch B
- one synthesis subagent decides merge vs rebase and the next action

## Failure modes
- switching machines with uncommitted changes
- landing helper/tool changes before the note or skill they depend on
- treating generated caches as real branch work
- letting shared-branch history drift until the next handoff becomes ambiguous
