---
project_id: hermes
note_type: session-summary
updated_at: 2026-06-12T00:00:00Z
---
# Hermes session summary

## Current implementation snapshot
- Note vault root is `~/.hermes/notes`.
- Note events are classified centrally by the hook router.
- MoA now emits redacted lifecycle hooks for start, retry, reference completion/error, review, synthesis, and end.
- The review ledger is `~/.hermes/backlog/decision-memory.json`.
- The research directory now lives under `~/.hermes/notes/Research` with an agents sub-hub.
- The Hermes project now has a canonical activity checklist note and a harness/loop gap-analysis note.
- The Hermes vault has a compatibility Obsidian skill wrapper plus a vault-activation checklist to keep the local note root anchored at `~/.hermes/notes`.
- The legacy `subagent-driven-development` name now resolves through a compatibility skill wrapper to the canonical workflow umbrella.
- Closed or verified checklist entries can now be promoted into decision memory automatically when the checklist carries durable action, scope, evidence, and status fields.

## Next action
- Use the index note first, then only the linked note that answers the current question.
