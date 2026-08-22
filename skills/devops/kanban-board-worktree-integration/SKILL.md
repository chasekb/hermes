---
name: kanban-board-worktree-integration
description: "Use when matching Kanban boards to Git worktrees."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [kanban, boards, worktrees, projects, backlog, isolation]
    related_skills: [kanban-orchestrator, project-backlog-workflows, hermes-orchestrator-layout]
    created_by: agent
---

# Kanban Board and Worktree Integration

Use this class-level workflow when a backlog has project-scoped work and each project should execute through an isolated Kanban board and Git worktree. The backlog remains the durable intake/specification layer; the board is the execution queue; the Hermes project record supplies the repository anchor and deterministic worktree convention.

## Bootstrap sequence

1. Enumerate project ids from the live backlog sources. Prefer the canonical shared backlog CLI; inspect the Hermes legacy snapshot when the request explicitly refers to `project_id`, and reconcile the union without silently dropping projects.
2. Discover the real repository path for every project. Verify the path exists and `git -C <path> rev-parse --show-toplevel` succeeds. Never invent a path or use a non-Git directory as a worktree anchor.
3. Create or reuse a Kanban board whose slug and display name equal the project id.
4. Create or reuse a Hermes project with the same slug and the verified repository as its primary path.
5. Bind the project to the same-named board with `hermes project bind-board <project> <board>`.
6. Set the board default workdir with `hermes kanban boards set-default-workdir <board> <repo>`; this makes the board worktree-capable and gives the dashboard a concrete workspace anchor.
7. Create future execution cards with `--project <project-id>` (or explicit `--workspace worktree`). Project-linked cards auto-select worktree workspaces and branch from the project repository.

## Backlog bridge

When materializing backlog items, preserve the source and stable backlog id in the Kanban card body and use a deterministic idempotency key such as `backlog:<source>:<board>:<backlog-id>`. Apply only active items by default; closed, archived, and completed items remain historical backlog evidence rather than new active cards. Re-run the bridge to verify no duplicates are created.

## Verification checklist

- `hermes kanban boards list` shows every expected board.
- `hermes project show <project>` reports the same board and a valid primary Git path.
- `hermes kanban boards list --json` reports a non-null `default_workdir` for every board in scope.
- `hermes kanban --board <board> stats` confirms the expected queue.
- A project-linked task creation path is used for new work so its `workspace_kind` resolves to `worktree`.
- Existing running or queued scratch tasks are not rewritten in place; changing their workspace can disrupt workers and lose state.
- Every task defaults to `remote_ci_required=true`: workers must not run local package/container builds, and repository changes require commit, push, and exact-SHA GitHub Actions build verification before completion.
- A local build is an explicit exception only when the task is created with `remote_ci_required=false` or the CLI `--allow-local-build` override.

## Remote-only build policy

The Kanban task schema and worker context carry the remote-CI requirement. New cards inherit it automatically, child cards inherit it unless explicitly overridden, and legacy cards are migrated to the required default. See `references/remote-ci-build-verification.md` for the push → exact-SHA run → build-proof sequence.

## Scope and safety

The default board is also a board and should receive an explicit valid Git workdir if the user literally requests all boards. Do not delete databases, archive active work, or recreate live tasks solely to change workspace mode. If a project path is missing, create the board only if requested, report that worktree enablement is blocked for that project, and wait for a real repository path.

See `references/kanban-board-worktree-bootstrap.md` for the verified command sequence and the legacy/shared backlog reconciliation notes.
