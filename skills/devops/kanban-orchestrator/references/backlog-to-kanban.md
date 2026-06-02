# Backlog to Kanban bridge

The bridge exists so Hermes backlog items can become runnable Kanban work without losing the durable spec.

## Canonical flow

1. Read `execution_criteria` from the backlog item.
2. Derive the smallest runnable slice that can satisfy those criteria.
3. Materialize a Kanban task with the backlog id preserved in metadata or a backlink comment.
4. Keep dependency edges in Kanban so downstream tasks stay blocked until prerequisites finish.
5. Capture verification evidence in the Kanban completion metadata.
6. Reflect final status and evidence back into the backlog item.

## What should move into Kanban

- the runnable slice for today
- dependency edges
- reviewer or verifier tasks
- evidence required for closeout

## What should stay in the backlog

- scope and summary
- execution criteria
- closeout criteria
- project ownership / tenant
- long-lived notes and links

## Bridging conventions

- Preserve the stable backlog id wherever the execution tool allows it.
- If the execution tool has no metadata field, include the id in the card title or body.
- Keep status changes monotonic: backlog `accepted` → Kanban `in_progress` → backlog `done/closed`.
- Never close a backlog item without evidence.
