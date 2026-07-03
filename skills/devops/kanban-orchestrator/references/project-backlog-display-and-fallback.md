# Project backlog display and fallback

This note captures the display pattern that came up when showing a project backlog from the live Hermes backlog store.

## Live backlog read pattern

- Read `~/.hermes/backlog/backlog.json` fresh.
- Filter items by `project_id == <requested project>`.
- For a generic "show the backlog" request, prefer `status != "closed"`.
- If the user specifically wants actionable work, consider excluding `archived` as well; `archived` items are not closed, but they are usually not active work.

## Project-scoped reporting shape

- When the user asks for a specific project such as `project_id=trade`, report the item count and status mix before the item list.
- Keep the item list concise: `id | priority | status | title`.
- If the user references `.hermes/backlog.json`, treat it as a path shorthand to resolve; the live store to read is `~/.hermes/backlog/backlog.json`.
- If there are no live matches, say so explicitly and then fall back to repo-local backlog docs separately so the user can tell durable Hermes intake apart from documentation.

## Fallback pattern

If there are no live matches for the requested project:

1. Say so explicitly.
2. Summarize repo-local backlog docs separately, such as:
   - `docs/TODO.md`
   - `docs/cpp_todo.md`
3. Keep the live Hermes backlog and repo-local backlog distinct so the user can tell whether the work is durable Hermes intake or just documentation.

## Practical reporting shape

When returning a backlog, keep the list concise:

- id
- priority
- status
- title

If a project has only archived items, say that clearly instead of implying there is active work.
