# Project status snapshot

When a user asks to show the Hermes project backlog or project status, provide a two-part live snapshot:

1. Backlog store (`backlog/backlog.json`)
   - Re-read the file first.
   - Report open items, closed items, and any history/evidence details that matter.
   - Do not rely on a stale chat summary.

2. Kanban board state
   - Show the current board list and counts.
   - Show the active board's live task list and stats.
   - Include archived rows when the user wants the closed/full picture.

Recommended command sequence:
- `hermes kanban boards list`
- `hermes kanban list`
- `hermes kanban stats`
- `hermes kanban list --archived`

Notes:
- `hermes kanban list` reports the current board; it does not take a `--board` flag.
- Use board selection/switching only with commands that support it.
- Keep the result concise: id, priority, status, title, and any relevant counts.