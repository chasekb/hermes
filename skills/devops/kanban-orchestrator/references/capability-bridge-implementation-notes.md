# Capability bridge implementation notes

This note captures the operational pattern that emerged while building the Hermes backlog↔Kanban bridge.

## Canonical backlog store

- Keep the project backlog durable in `~/.hermes/backlog/backlog.json`.
- Treat backlog items as the source of truth for intake/spec state.
- Use Kanban as the execution surface and preserve the stable backlog id in Kanban metadata or a backlink comment.

## Bridge helpers

- `scripts/backlog_to_kanban.py` — materialize backlog items into runnable Kanban tasks.
- `scripts/review_backlog.py` — produce weekly/stale review output from the backlog store.
- `scripts/kanban_closeout_sync.py` — copy completion evidence back into the backlog record.

## Live bridge

- `scripts/backlog_to_kanban.py` can render the backlog as a bridge payload or apply it directly to a Kanban board with `--apply --board <slug>`.
- The created Kanban task title should preserve the stable backlog id, and the body should restate the execution and closeout criteria.
- Use the Kanban task as the runnable slice; keep the backlog item as the durable spec.
- Prefer `--triage`/specification handoff for newly promoted items so the backlog review remains the source of truth for acceptance.

## Closeout rule

When syncing a task to `done`/`closed`, require completion evidence by default. If the workflow needs an exception, make that explicit in the call rather than silently accepting an empty closeout.

## Verification pattern

Prefer lightweight CLI smoke tests before committing bridge changes:

1. Compile the scripts.
2. Run the bridge helpers directly with a minimal fixture or "empty backlog" case.
3. Check staged diffs for whitespace and formatting issues.

This pattern keeps the bridge simple and reproducible without needing the full orchestration stack to validate basic behavior.
