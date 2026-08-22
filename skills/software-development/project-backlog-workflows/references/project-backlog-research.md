# Project Backlog Research (absorbed note)

Preserved details from the former `project-backlog-research` skill.

## Research-only boundary
Use when the user asks to research, scope, or trace an existing backlog item and explicitly wants exact files/symbols/tests rather than implementation.

Do **not**:
- edit repository files;
- move, note, close, or mutate the backlog item;
- commit, stage, format, or fix files;
- generalize from remembered conversation state when live repo evidence is available.

## Backlog item loading
- Read `~/.agent-commons/AGENTS.md` before using the backlog CLI when present.
- Show the item with:
```sh
python3 ~/.agent-commons/backlog/backlog.py --actor hermes show <ID>
```

## Report outline
- What I inspected
- Key finding
- Exact frontend/backend flow
- Backend/frontend contract proof
- Minimal implementation plan
- Tests to add/update
- Files modified: None
- Notes/blockers/pre-existing repo changes

## Shell/path pitfall
Some project paths contain spaces or shell metacharacters. If a tool refuses such a path as `workdir`, run commands from a safe directory with a quoted `cd '<repo path>' && ...` prefix.
