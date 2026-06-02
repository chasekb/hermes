# Hermes project backlog

This directory is the durable intake/spec layer for Hermes-native project backlog work.

Canonical store:
- `backlog.json`

Expected item shape:
- `id`
- `title`
- `summary`
- `scope`
- `tenant`
- `execution_criteria`
- `closeout_criteria`
- `dependencies`
- `status`
- `notes`
- `links`
- `created_at`
- `updated_at`
- `history`
- `evidence`

Status flow:
- `proposed` → `triaged` → `accepted` → `ready` → `in_progress` → `blocked` → `done` → `closed`
- `archived` is reserved for intentionally retired items

Tooling:
- `skills/devops/kanban-orchestrator/scripts/backlog_to_kanban.py`
- `skills/devops/kanban-orchestrator/scripts/review_backlog.py`
- `skills/devops/kanban-orchestrator/scripts/kanban_closeout_sync.py`

Review cadence:
- weekly backlog review
- stale-item review when items stop moving or remain blocked without updates

The backlog is the source of truth. Kanban is the execution surface.
