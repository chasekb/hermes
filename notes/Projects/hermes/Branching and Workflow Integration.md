# Branching and Workflow Integration

This note records the repo-specific workflow for working on Hermes across two computers, plus how to integrate work that lives on separate branches.

## Default branch policy

- Use `main` as the integration branch, not as a long-lived scratchpad.
- Prefer one active working branch per machine.
- Keep the worktree clean before switching machines.
- If both machines may be used at the same time, do not share a single editable branch.

## Recommended branch topology

### Best default
- Machine A: its own feature branch off `origin/main`
- Machine B: its own feature branch off `origin/main`
- `main`: merge/rebase target only

### Shared branch only when serialized
A single shared branch is acceptable only if all of the following are true:
- only one machine edits at a time
- the worktree is clean before handoff
- you commit and push before switching machines
- the next machine fetches and reconciles before editing

If any of those conditions is false, use separate branches.

## Handoff checklist

Before leaving one machine:
1. Run `git status --short --branch`.
2. Commit the current work, or intentionally park it in a short-lived branch.
3. Push the branch if the other machine will continue it.
4. Record any branch-specific notes in this file or the companion skill.

Before starting on the other machine:
1. `git fetch origin`
2. Inspect `git status --short --branch`
3. Rebase or merge from `origin/main` as needed.
4. Confirm no local cache or generated files are being mistaken for real work.

## Integrating work from separate branches

Use this pattern when skills, tools, workflows, or docs were developed on different branches:

1. Split the work by concern.
   - content changes
   - workflow/skill changes
   - automation/tooling changes
2. Review each branch independently first.
3. Prefer a synthesis branch for the final integration if the branches touch the same files.
4. Rebase small branch-local changes when you want a linear history.
5. Merge when you need to preserve branch structure or when the branch contains a meaningful milestone.
6. Update the umbrella skill or note only after the branch-local pieces are sound.
7. Verify the integrated state by re-reading the updated skill/note and checking git status.

### For Hermes-specific workflow changes
When branch A adds a new skill and branch B adds the tool or reference it depends on:
- land the dependency first
- then land the skill or note that points to it
- then verify the full path by loading the skill and running the helper

## Automation helpers

Use automation to reduce handoff mistakes:
- a branch status helper that reports clean/dirty state and ahead/behind counts
- a handoff helper that warns when the current branch is dirty before a machine switch
- a repo workflow helper that prints the next safe step instead of forcing the user to infer it

Recommended helper path for this repo:
- `skills/software-development/hermes-repo-branch-workflow/scripts/repo_branch_workflow.py`

## Parallel work and delegation

Use subagents when there are independent branches or orthogonal workstreams to inspect.

Good fan-out pattern:
- one agent reviews branch A
- one agent reviews branch B
- one synthesis agent compares them and gives the integration rule

Use that pattern for:
- comparing branch-local skill changes
- reviewing tool changes separately from docs changes
- checking whether two branches can be merged cleanly or should be rebased first

## Main failure modes

- switching machines with uncommitted changes
- letting generated caches ride along with real work
- merging automation before the note/skill references exist
- rebasing repeatedly without a clean checkpoint commit
- forgetting which branch is the source of truth for the current machine

## Practical rule

If the work is still exploratory, keep it isolated on a machine-specific branch.
If the work is ready to integrate, reconcile it on `main` with a fresh status check and a clean verification pass.
