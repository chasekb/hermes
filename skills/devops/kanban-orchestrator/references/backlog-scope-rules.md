# Backlog scope and snapshot rules

This reference defines which backlog surface is authoritative and which surfaces are filtered or serialized views. It exists to prevent a project report, checked-in JSON file, or Kanban board snapshot from being mistaken for the shared backlog state.

## Authority order

Use these surfaces in this order:

| Surface | Role | Authority |
| --- | --- | --- |
| `~/.agent-commons/backlog/` through `backlog.py` | Shared backlog for Claude Code, Codex, Hermes, and humans | **Canonical** for records, status, criteria, audit events, and mutations |
| `backlog.py list --project NAME` | Project-scoped query over the shared backlog | Read-only **projection**; it does not create a second backlog |
| `backlog.py export` or a generated JSON/Markdown report | Serialized full or filtered data | **Snapshot**; it may be stale or incomplete |
| `~/.hermes/backlog/backlog.json` | Legacy Hermes JSON store/export | Compatibility or migration **snapshot**, not canonical after the shared store migration |
| Repository-local `backlog/backlog.json` or TODO documents | Project documentation or imported source material | **Project-local snapshot**; not the shared backlog |
| Kanban board and cards | Runnable work, dependencies, handoffs, and evidence | **Execution projection**; not backlog authority |

The shared store contract is `~/.agent-commons/backlog/SPEC.md`. Reads and writes to the canonical store go through the CLI:

```sh
python3 ~/.agent-commons/backlog/backlog.py --actor hermes <command>
```

Do not edit `backlog.db` or any JSON snapshot directly and then report the result as current canonical state.

## Scope semantics

- A project scope is the exact value carried by the item (`project` in the shared schema; `project_id` is accepted as a legacy/import alias). Match the requested value exactly after applying the CLI's normal string handling.
- An empty project value means **unscoped**. It is not an implicit project named `global`, and it must not be silently assigned to the current Hermes project.
- `tenant` is a separate namespace. A project filter does not replace tenant isolation, and a tenant match does not imply a project match.
- Filtering by project, status, priority, or tag only narrows what is displayed. It must not be interpreted as deleting, archiving, or changing records outside the projection.
- A project-scoped count is the count of matching records in the selected source and status filter, not a count of all records in the canonical store.

## What to read and when

### Current global or project state

Use the shared CLI and state the scope in the report:

```sh
# All records in the canonical shared backlog
python3 ~/.agent-commons/backlog/backlog.py --actor hermes export

# One project projection
python3 ~/.agent-commons/backlog/backlog.py --actor hermes list --project hermes

# One project and selected statuses, when supported by the CLI contract
python3 ~/.agent-commons/backlog/backlog.py --actor hermes list --project hermes --status proposed,ready,in_progress
```

Re-run the query when the source may have changed. Do not use a prior chat summary, a stale generated report, or the number of Kanban cards as a substitute for the canonical query.

### Legacy or repository-local JSON

Read `~/.hermes/backlog/backlog.json` or a repository `backlog/backlog.json` only when one of these is true:

- the user explicitly names that path;
- a migration or import is being audited;
- a compatibility helper still requires the legacy JSON format; or
- the file is being compared with the canonical shared export.

Label the result as a snapshot, include its `generated_at`/source metadata when present, and do not claim it represents current global state without comparing it with the shared CLI. Existing bridge helpers that default to `~/.hermes/backlog/backlog.json` are legacy JSON workflows until they are migrated; treat their output and write-back as snapshot operations.

For a migration, import through the supported command, then verify the canonical result with a fresh project-scoped query:

```sh
python3 ~/.agent-commons/backlog/backlog.py --actor hermes import-json <FILE> --source <SOURCE>
python3 ~/.agent-commons/backlog/backlog.py --actor hermes list --project <PROJECT>
```

### Kanban status

Kanban answers “what execution work is queued or running?” The backlog answers “what work exists, what scope owns it, and what criteria/state define it?” Show the two separately. Preserve the stable backlog id on the Kanban card, but do not treat a card count or board filter as proof that the corresponding backlog projection is complete.

## Reporting checklist

Every global or project backlog report should make these facts explicit:

1. **Source:** canonical shared CLI, legacy JSON snapshot, repository-local document, or Kanban board.
2. **Scope:** global/unscoped, exact `project` value, and tenant where relevant.
3. **Status filter:** for example, all statuses, open statuses, or `status != closed`.
4. **Freshness:** query time or snapshot `generated_at` value.
5. **Counts:** distinguish the canonical total from the filtered/project total; do not add counts from different sources.
6. **Fallbacks:** if there are no canonical matches, report zero matches before separately describing repository-local docs or Kanban tasks.

A project report should use a compact row shape such as `id | priority | status | title`, preceded by the project count and status mix. If only a snapshot is available, say so plainly.

## Common mistakes

- Calling `~/.hermes/backlog/backlog.json` “the live backlog” after the shared `~/.agent-commons/backlog/` store has been established.
- Treating `list --project NAME` as a separate database rather than a filtered read of the canonical store.
- Mixing unscoped records into a project's count because the records came from the same global export.
- Treating a repository TODO file as durable intake without importing it into the shared backlog.
- Treating Kanban's open cards as an authoritative list of backlog records; cards can be absent, archived, duplicated, or still awaiting materialization.
- Falling back from zero canonical project matches to local docs without labeling the source change.
- Mutating a snapshot and assuming the shared backlog or another agent will observe the change.

## Related references

- `~/.agent-commons/backlog/SPEC.md` — shared CLI/schema contract.
- `project-backlog-model.md` — backlog/Kanban responsibility split.
- `project-backlog-display-and-fallback.md` — concise project display and repo-local fallback.
- `project-status-snapshot.md` — combined backlog and Kanban status report.
- `backlog-kanban-migration.md` — migration inventory and reconciliation gates.
