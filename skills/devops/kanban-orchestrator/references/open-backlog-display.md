# Open Hermes backlog display recipe

When asked to show the open Hermes project backlog:

1. Query the canonical shared backlog through `~/.agent-commons/backlog/backlog.py`.
2. If a project is requested, pass the exact project scope and report it as a filtered projection.
3. Filter items where `status != "closed"` when the request means open work.
4. Present a concise list with:
   - id
   - priority
   - status
   - title
5. Report the project count and status mix before the item list.
6. If there are no canonical matches, say so before separately describing repository-local docs or Kanban tasks.
7. Keep the response short unless the user explicitly asks for more detail.

Do not call `~/.hermes/backlog/backlog.json` the live backlog. Read it only for an explicit legacy snapshot or migration check, and label its `generated_at` value/source.

Useful when the backlog has been through patch churn or restoration and the previous conversational summary may be stale.
