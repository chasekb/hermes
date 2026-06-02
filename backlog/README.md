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
  - render backlog items as a bridge payload, or apply them directly to a Kanban board with `--apply --board <slug>`
- `skills/devops/kanban-orchestrator/scripts/review_backlog.py`
- `skills/devops/kanban-orchestrator/scripts/kanban_closeout_sync.py`

Operational notes:
- `skills/devops/kanban-orchestrator/references/workflow-registry.md` is the registry of the project workflows that move items from intake to review and closeout.
- `skills/devops/kanban-orchestrator/references/capability-bridge-implementation-notes.md` captures the live bridge pattern and smoke-test recipe.
- The bridge preserves the backlog item id in the created Kanban task title/body so closeout evidence can be synced back unambiguously.

Review cadence:
- weekly backlog review
- stale-item review when items stop moving or remain blocked without updates

The backlog is the source of truth. Kanban is the execution surface.
