# Board slug vs current-board reconciliation

Use this note when a user asks to rename or replace a project board and the CLI seems to keep pointing at the old board.

## What the CLI distinguishes

- Slug: the immutable board identifier used in paths and commands.
- Display name: the human-readable label shown in `boards list`.
- Current board: the active selection the CLI uses when no explicit `--board` is passed.

Renaming a board changes the display name only. It does not change the slug.

## Recommended migration sequence

1. Create the replacement board with the desired slug if you need a new identifier.
2. Switch to the new board explicitly.
3. Delete the old board only after the new board exists and is verified.
4. Re-run `hermes kanban boards current` immediately after deletion.
5. If the current board falls back to `default`, switch to the new board again and verify once more.

## Pitfall

Deleting the old board can cause the active-board marker to fall back to `default` even if a new board already exists. Do not assume the prior switch still sticks; always verify the current board after deletion.

## Verification checklist

- `hermes kanban boards list` shows the new slug.
- `hermes kanban boards current` reports the new slug.
- `hermes kanban list` resolves against the intended project board without needing an explicit `--board`.
