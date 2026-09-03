# Hermes project backlog

This directory contains Hermes's repository-local backlog snapshot and intake documentation. It is not the canonical cross-agent backlog store.

Canonical store:
- `~/.agent-commons/backlog/`, accessed through `backlog.py`

Snapshot in this repository:
- `backlog.json` — checked-in project-local JSON snapshot for history, review, and compatibility
- Scope rules: `skills/devops/kanban-orchestrator/references/backlog-scope-rules.md`

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
- The shared backlog at `~/.agent-commons/backlog/` is authoritative after the 2026-07-15 migration; use its CLI for current reads and all mutations.
- `backlog.json` may be stale or project-filtered. Read it only for explicit snapshot, migration, or compatibility work, and label reports from it as snapshots.
- `skills/devops/kanban-orchestrator/references/workflow-registry.md` is the registry of the project workflows that move items from intake to review and closeout.
- `skills/devops/kanban-orchestrator/references/capability-bridge-implementation-notes.md` captures the live bridge pattern and smoke-test recipe.
- The bridge preserves the backlog item id in the created Kanban task title/body so closeout evidence can be synced back unambiguously.
- Hermes workspace backlog intake should default new `~/.hermes` items to `project_id=hermes` so the project scope stays isolated and reviewable.
- `backlog/decision-memory.json` is the durable decision-memory store for execution summaries, recommendations, and review evidence; keep secrets out of it.

Review cadence:
- Start with `skills/devops/kanban-orchestrator/references/workflow-registry.md`; it is the canonical index and shows the next action for each review path.
- weekly backlog review (`skills/devops/kanban-orchestrator/references/weekly-backlog-review.md`)
- stale-item review when items stop moving or remain blocked without updates (`skills/devops/kanban-orchestrator/references/stale-item-review.md`)
- use the decision-memory store to feed the next weekly or stale review recommendation instead of rebuilding the session from scratch

The shared backlog is the source of truth. This repository JSON is a project-local snapshot, and Kanban is the execution surface.
