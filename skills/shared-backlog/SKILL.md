---
name: shared-backlog
description: Add, triage, or review items in the shared cross-agent backlog at ~/.agent-commons/backlog/ (used by Claude Code, Codex, and Hermes identically). Use when the user mentions the backlog or wants to capture a future task/recommendation.
---

# Shared agent backlog

Canonical cross-agent conventions (backlog contract, shared credentials,
operating discipline) live in `~/.agent-commons/AGENTS.md`; read that file
first. Hermes specifics below.

Contract: `~/.agent-commons/backlog/SPEC.md`. All reads and writes go through
the CLI — never edit `backlog.db` directly:

```sh
python3 ~/.agent-commons/backlog/backlog.py --actor hermes <command>
```

Commands: `add`, `list [--status a,b]`, `show ID`, `move ID STATUS`,
`note ID TEXT`, `close ID --note EVIDENCE`, `export`.

Status flow: `proposed → triaged → accepted → ready → in_progress → (blocked ⇄) → done`;
`closed` only via `close` with a non-empty evidence note.

Conventions: always pass `--actor hermes` (use `human` only for words the user
actually said); set `--provenance` on adds; no secrets or personal data in any
field; close instead of delete. This store supersedes
`~/.hermes/backlog/backlog.json` (kept as cold history; already imported with
`hermes:` provenance on 2026-07-15).
