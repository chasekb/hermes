---
name: kanban-migration-governance
description: "Use when migrating Hermes backlogs into Kanban boards."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [kanban, migration, backlog, project-routing, worktrees, safety]
    related_skills: [kanban-board-worktree-integration, project-backlog-workflows, shared-backlog]
    created_by: agent
---

# Kanban Migration Governance

Use this class-level workflow when converting a Hermes backlog or project-scoped task source into durable Kanban boards, especially when remote inspection, multiple Hermes homes, historical records, or source cleanup are involved.

## Scope boundary first

1. Identify the machine and Hermes home being migrated.
2. Treat remote access (SSH, Tailscale, gateway, or another host) as read-only unless the user separately authorizes remote mutation.
3. Never infer that a remote source is the target merely because it contains a similar board or session history.
4. Keep local and remote manifests, backups, and verification results separate.

## Source and project discovery

1. Read the canonical live source for the target machine through its supported CLI/API; never edit the source database directly.
2. Normalize read-only schema aliases such as `project_id` and `project`, while preserving the original record and source identifier.
3. Enumerate every project scope, including unscoped records and projects with only historical records.
4. For every project that requires a board, discover its actual repository root and verify it with `git -C <path> rev-parse --show-toplevel`. Do not invent a path or use a non-Git directory when the requirement is a repository-root workdir.
5. If a project root cannot be verified, hold that project's records and report the blocker. Do not silently route them to another project.

## Board and card materialization

1. Create or reuse exactly one board per routable project; use the project identifier as the board slug and display name.
2. Create or reuse the Hermes project, set its verified primary path, bind it to the same-named board, and set the board default workdir to the exact Git root.
3. Index all existing Kanban cards by stable source ID before creating anything.
4. Use deterministic idempotency keys and preserve the full source record, criteria, provenance, tenant, project identifier, and original status in the card body.
5. Preserve unrelated pre-existing Kanban tasks. Never rewrite running or queued tasks merely to change workspace mode.
6. Materialize closed/historical records as archived, non-executable cards; materialize active records as runnable cards with source status retained as metadata.
7. Route unscoped records only to an explicitly named catch-all board whose default workdir is a verified Git root. Report this policy rather than presenting the records as project-owned.

## Verification gates

Before declaring migration complete, independently verify:

- Every routable source ID appears exactly once across the target boards, including archived cards.
- No source ID is missing, duplicated, or on the wrong board.
- Every board in scope has a non-null default workdir.
- Every default workdir exactly equals `git rev-parse --show-toplevel`.
- Every Hermes project is bound to its same-named board and has the same verified primary root.
- Existing unrelated Kanban tasks remain present.
- The migration manifest records source counts, project/status distribution, created/skipped items, held blockers, board roots, and verification results.

## Cleanup safety

1. Write a source backup and migration manifest before cleanup.
2. Perform a dry-run that prints the exact source path(s) and record scope to be deleted.
3. Require explicit point-of-action user/safety confirmation before deleting the source backlog.
4. Delete only the intended source files; never delete a database data directory as part of backlog cleanup.
5. Re-run source-absence, manifest, backup, and Kanban reconciliation checks after cleanup.

See `references/backlog-kanban-migration.md` for the command-independent checklist, schema-alias notes, and verification report shape.
