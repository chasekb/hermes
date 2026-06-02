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
- `backlog/decision-memory.json` is the durable decision-memory store for execution summaries, recommendations, and review evidence; keep secrets out of it.

Review cadence:
- Start with `skills/devops/kanban-orchestrator/references/workflow-registry.md`; it is the canonical index and shows the next action for each review path.
- weekly backlog review (`skills/devops/kanban-orchestrator/references/weekly-backlog-review.md`)
- stale-item review when items stop moving or remain blocked without updates (`skills/devops/kanban-orchestrator/references/stale-item-review.md`)
- use the decision-memory store to feed the next weekly or stale review recommendation instead of rebuilding the session from scratch

The backlog is the source of truth. Kanban is the execution surface.
