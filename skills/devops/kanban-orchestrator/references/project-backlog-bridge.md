# Backlog ↔ Kanban bridge

This document defines the bridge between the Hermes-native project backlog and Kanban execution.

Canonical backlog store:
- `~/.hermes/backlog/backlog.json`

Bridge contract:
- backlog owns scope, criteria, and state
- Kanban owns task execution and evidence collection
- completion writes back to the backlog item

Operational flow:
1. Read `execution_criteria` from the backlog item.
2. Turn those criteria into a runnable slice and tests.
3. Create or update a Kanban task with the backlog id preserved in metadata or a backlink comment.
4. Keep dependency edges in Kanban so downstream work remains blocked until prerequisites finish.
5. When the task completes, capture evidence and update the backlog item to `done` or `closed`.
6. If evidence is missing, keep the backlog item open and mark the closeout review as incomplete.

Use the helper scripts in `scripts/` for the common bridge operations:
- `backlog_to_kanban.py` (render the backlog as a bridge payload or apply it directly to a Kanban board)
- `review_backlog.py`
- `kanban_closeout_sync.py`

What should stay in the backlog:
- long-lived scope and summary
- execution criteria
- closeout criteria
- ownership / tenant
- notes and links
- incident-derived recovery guidance when a live run exposes a reusable failure mode (stash refs, conflicted paths, decision tree, verification)

What should move into Kanban:
- the runnable slice for today
- dependency edges
- reviewer or verifier tasks
- evidence required for closeout

Bridging conventions:
- preserve stable ids whenever the execution tool allows it
- if no metadata field exists, include the id in the card title or body
- keep status transitions monotonic
- never close a backlog item without evidence
