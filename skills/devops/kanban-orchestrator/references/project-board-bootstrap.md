# Project board bootstrap

Use this when a user asks to initiate kanban for a specific project/repo.

## Goal
Create a project-scoped board and a project-specific orchestrator profile, then operate explicitly on that board.

## Recipe

```bash
hermes kanban boards create <slug> \
  --name "<Display Name>" \
  --description "Kanban board for <project>" \
  --default-workdir "/absolute/path/to/project" \
  --switch

hermes profile create <profile-name> \
  --clone-from default \
  --description "Project-specific kanban orchestrator for <project>"

hermes kanban boards list
hermes profile list
```

## Verification

- The new board appears in `hermes kanban boards list`.
- The new profile appears in `hermes profile list`.
- Later kanban commands target the board explicitly with `hermes kanban --board <slug> ...`.

## Practical notes

- Keep the board slug short and project-scoped.
- Use the project root as the board default workdir.
- Keep the orchestrator profile generic; create extra specialist profiles only if the project truly needs them.
