---
name: hermes-repo-branch-workflow
description: Hermes repo-specific workflow for using one branch across two computers, integrating changes from separate branches, and using helper tooling to reduce handoff mistakes.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, git, branches, worktrees, workflow, automation, delegation]
    related_skills: [software-development-workflows, github-workflows, workflow-skill-curation]
---

# Hermes Repo Branch Workflow

Use this skill when working in the Hermes repo on more than one computer, when deciding whether to share a branch or split work by machine, or when integrating skills/tools/workflows that were built on separate branches.

This skill is repo-specific. The companion project note lives at:
`notes/Projects/hermes/Branching and Workflow Integration.md`

## Core rule

Prefer one active branch per machine and keep `main` as the integration branch.
Use a shared branch only when the work is strictly serialized and the worktree is clean before every handoff.

## Branch choice

### Default
- Machine A: its own feature branch off `origin/main`
- Machine B: its own feature branch off `origin/main`
- `main`: integration only

### Shared branch exception
A single shared branch is only acceptable when:
- only one machine edits at a time
- the branch is committed and pushed before switching
- the next machine fetches and reconciles before editing

If any of those conditions is false, switch to per-machine branches.

## Handoff procedure

Before switching machines:
1. Run `git status --short --branch`.
2. Commit the current work or move it onto a dedicated branch.
3. Push the branch if the other machine needs it.
4. Confirm any generated caches or local state are not part of the intended change.

Before continuing on the other machine:
1. `git fetch origin`
2. Inspect `git status --short --branch`
3. Rebase or merge from `origin/main` as needed.
4. Re-run the relevant verification step for the branch.

## Integrating work from separate branches

When skills, tools, notes, or workflows were developed on different branches, integrate them in this order:
1. Land the dependency first.
2. Land the note or reference that explains the workflow.
3. Land the skill or helper that consumes it.
4. Verify the full path from the repo root.

Prefer a synthesis branch when several branch-local changes touch the same files.
Use rebase for short-lived machine branches when you want a linear history.
Use merge when you need to preserve a milestone or a branch structure.

## Parallel work

Use subagents when branch-local workstreams are independent.
Good split:
- one agent inspects branch A
- one agent inspects branch B
- one synthesis agent decides how to integrate them

This is especially useful when:
- one branch changes a skill and another branch changes a tool
- one branch changes docs and another branch changes automation
- you need a compare/contrast recommendation before choosing merge vs rebase

## Automation helper

Use the repo helper script to reduce handoff mistakes:
`skills/software-development/hermes-repo-branch-workflow/scripts/repo_branch_workflow.py`

The helper should report:
- current branch
- clean/dirty status
- ahead/behind state
- a next-safe-step recommendation

## Pitfalls

- Switching machines with uncommitted work
- Letting generated caches ride along with real branch changes
- Rewriting history before capturing a clean checkpoint commit
- Merging automation before the note/skill reference exists
- Forgetting which branch is the source of truth for the current machine

## Verification

A good run of this skill ends with:
- a clear branch choice
- a clean handoff checklist
- a verified integration path
- a helper script or note that makes the next handoff easier
