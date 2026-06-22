---
name: obsidian
description: "Filesystem-first Obsidian vault workflow for Hermes project notes, summaries, and decision logs."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [obsidian, notes, vault, context, project-memory]
---

# Obsidian Vault Workflow

Use this skill when Hermes needs durable project continuity in a local vault.

## Canonical vault
- Hermes workspace vault root: `~/.hermes/notes`
- If `OBSIDIAN_VAULT_PATH` is already set, respect it only when it still points at the Hermes vault root or another user-approved vault.
- Do not scan unrelated vault content when the project index and directly linked notes are sufficient.

## Core note set
The Hermes vault should stay shallow and navigable:
- `Projects/hermes/Index.md`
- `Projects/hermes/Decision Log.md`
- `Projects/hermes/Session Summary.md`
- `Projects/hermes/Open Questions.md`
- related research or reference notes only when they are directly linked from the index

## Retrieval rule
1. Start from the project index note.
2. Load the decision log and session summary next.
3. Follow only the links needed for the current task.
4. Stop after the first-hop set unless a linked note is clearly required.
5. Keep the whole vault out of context by default.

## Write-back rule
After a major boundary:
- update the session summary with the current implementation snapshot
- append decisions with rationale and consequences
- refresh the index links if the project structure changed

## File-tool guidance
- Use `read_file` / `write_file` / `patch` with absolute paths.
- Do not pass shell variables to file tools.
- Prefer deterministic paths and explicit note names.

## Smoke check
A valid smoke check is:
- open the project index note
- confirm the linked decision log and session summary exist
- verify the note path stays inside `~/.hermes/notes`
- stop after the linked notes, instead of loading the whole vault

See `references/vault-activation-checklist.md` for the quick bootstrap / verification sequence.
