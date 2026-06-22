---
project_id: hermes
note_type: decision
updated_at: 2026-06-12T00:00:00Z
---
# Hermes decision log

## Decisions
- Use `~/.hermes/notes` as the vault root for Hermes project continuity.
- Route note lifecycle telemetry through `~/.hermes/agent-hooks/hook_router.py`.
- Keep note retrieval selective: index first, then only directly relevant linked notes.
- Keep telemetry redacted and reviewable in `~/.hermes/backlog/decision-memory.json`.
- Use `[[Activity Tracking Checklist]]` as the canonical Hermes action checklist.
- Promote only closed or verified checklist outcomes into decision memory automatically, and keep transient status chatter out of memory.
- Use `[[Harness Loop Gap Analysis]]` as the durable gap-analysis record for harness and loop engineering research.
- Keep `subagent-driven-development` as a compatibility alias only; the canonical guidance lives in `software-development-workflows`.
- Keep the Obsidian vault anchored at `~/.hermes/notes` and use the vault-activation checklist when verifying fresh shells or bootstrap state.

## Follow-up
- Add or update linked notes only when they are directly relevant to a task or decision.
