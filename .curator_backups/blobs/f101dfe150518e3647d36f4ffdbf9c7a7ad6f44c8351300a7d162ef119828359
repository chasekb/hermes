# Backlog-to-Kanban Migration Checklist

## Read-only inventory

- Confirm the target machine and Hermes home before reading state.
- For remote inspection, use SSH/Tailscale read-only unless remote mutation is separately authorized.
- Export through the supported backlog CLI/API; do not open the source database directly.
- Accept `project_id` and `project` as read-only schema aliases, but preserve the original source record.

## Board mapping

For each non-empty project identifier:

1. Discover the Hermes project primary path.
2. Verify `git -C <path> rev-parse --show-toplevel`.
3. Create/reuse a same-named board.
4. Bind the project to that board.
5. Set the board default workdir to the exact Git root.

For unscoped records, use a named catch-all board only if its workdir is a verified Git root. If a project root is unknown or not a repository, hold the records and report the blocker.

## Idempotent import

Index all boards, including archived cards, by stable source ID. Create cards with a deterministic key such as `shared-backlog:<board>:<source-id>`. Preserve the complete source record, provenance, criteria, tenant, project identifier, and original status in the body. Archive closed/historical cards after creation and preserve unrelated pre-existing tasks.

## Verification report

Record:

- source total and project/status distribution
- created, already-present, held, and failed counts
- canonical source ID → board/task ID mapping
- missing, duplicate, and wrong-board IDs
- every board workdir and `git rev-parse` result
- backup and manifest paths/checksums

Migration is not complete until missing, duplicate, and wrong-board sets are empty and every board root check passes.

## Cleanup gate

Create and verify a backup and manifest first. Print a dry-run with the exact deletion target. Obtain point-of-action confirmation before deleting the source backlog. Delete only the intended source file/directory; never delete a database data directory. Re-run source absence and Kanban reconciliation after cleanup.
