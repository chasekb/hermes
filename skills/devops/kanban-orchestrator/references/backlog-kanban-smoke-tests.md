# Backlog ↔ Kanban smoke tests

Concise operational notes from a live backlog-to-Kanban rollout.

## What worked
- Treat the backlog item as the durable spec and Kanban as the execution surface.
- Preserve stable backlog ids in Kanban metadata and/or a backlink comment.
- Materialize backlog items with a small, repeatable smoke test before bulk apply.
- Use `triage` as the entry state for freshly materialized cards.
- Verify the board with `hermes kanban --board <slug> stats` after apply.
- Record a backlog history event when the materialization step succeeds.

## Closeout / archive pattern
- When a test card is created only for verification, archive it immediately so it does not pollute the live board.
- Verify the archive with board stats rather than trusting the archive command alone.
- Use the closeout sync helper to write evidence back to the backlog store after a real item is archived or completed.

## Pitfalls
- Do not assume `hermes kanban create` accepts arbitrary priority strings; normalize to the CLI's expected form before generating commands.
- Do not rely on prose like "wait for X" for dependencies; use parent links at creation time.
- Do not bulk-apply before verifying the single-item smoke test path.
- Keep the backlog item ids stable; do not mint new ids when mirroring to Kanban.