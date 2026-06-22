# Repo-local backlog fallback

Use this note when a user asks for a project backlog but the live Hermes backlog has no matching `project_id` entries.

Observed pattern:
- Live Hermes backlog can be empty for a repo/project even when the repository contains backlog docs.
- For the cohida repo, the relevant docs were `docs/TODO.md` and `docs/cpp_todo.md`.
- Report the two sources separately:
  1. Hermes backlog / board state
  2. Repo-local backlog documents

Response shape:
- State whether any live Hermes backlog items match the project.
- Summarize each repo backlog doc independently with an open-count and the most important open items.
- Avoid merging the two into one list, because the user may want to know whether the work is already in Hermes or only captured in docs.
