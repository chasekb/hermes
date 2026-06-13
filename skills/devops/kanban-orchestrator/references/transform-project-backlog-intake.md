# Transform project backlog intake notes

Session note for the transform repo backlog bridge.

## Backlog surface
- Repo wrapper: `transform/scripts/backlog`
- Underlying store: `~/.codex/MCP/backlog/backlog.json`
- Default project scope: `CODEX_BACKLOG_PROJECT=transform`

## Intake shape
- `./scripts/backlog intake` reads a JSON payload from stdin.
- Required field: `title`
- Useful fields: `kind`, `summary`, `details`, `priority`, `source`, `tags`, `related_id`, `parent_id`, `project_id`
- Without `title`, the manager returns `{"error": "missing_title"}`.

## Verification
- `./scripts/backlog status` reports the live project backlog and counts.
- After a successful intake, the JSON file mirrors the new recommendation immediately.
- The status output includes the project id and the open recommendation count for the transform scope.

## Practical guidance
- Use a rich `details` body with explicit `Execution checklist:` and `Closeout criteria:` sections for implementation-oriented recommendations.
- Keep the title short and action-oriented; the detailed checklist belongs in `details`.
- When creating transform backlog items, prefer the repo wrapper so the correct project scope is selected automatically.
