---
name: kanban-evidence-capture
description: "Use when turning runtime logs into verified Kanban tasks."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [kanban, backlog, tmux, logs, evidence, triage, decomposition]
    related_skills: [shared-backlog, project-backlog-workflows, kanban-board-worktree-integration]
    created_by: agent
---

# Kanban Evidence Capture

Use this class-level workflow when a runtime observation, tmux pane, log stream, incident review, or dashboard failure must become durable project-scoped Kanban work. The workflow preserves enough evidence to reproduce the issue while keeping task bodies concise and actionable.

## 1. Establish scope and existing work

- Identify the exact project and board requested by the user; do not silently substitute the current/default board.
- Read the shared backlog contract and inspect active project items before creating work.
- Deduplicate by failure class, scope, provenance, and existing parent/child relationships. Create a narrower follow-up when an existing item already owns the broad investigation.
- Split independent concerns into separate cards. For runtime trading/dashboard failures, common separations are execution/no-trade reconciliation, scheduling/latency, and UI/data presentation.

## 2. Capture complete runtime evidence

- Capture full tmux scrollback, not only the visible tail, to a temporary text artifact.
- Parse the artifact for total lines/bytes, event counts, unique status/reason values, sequence and timestamp gaps, startup failures, and representative errors.
- Keep raw logs out of titles and descriptions. Put condensed, reproducible counts and exact pane provenance in the task body.
- Attach the raw artifact to a relevant Kanban task when durable evidence is needed. Never include secrets, credentials, or environment files.

See `references/tmux-log-evidence.md` for the capture and parsing checklist.

## 3. Create board work safely

- Use the Kanban CLI for board writes; never edit Kanban SQLite storage directly.
- Project-linked coding tasks should use the project and worktree workspace options so the task has a verified repository anchor.
- Kanban priority may use integer tiebreakers even when the shared backlog uses `low|medium|high`; consult the live CLI help rather than assuming the schemas match.
- Use deterministic idempotency keys containing the source provenance, board, and failure class.
- Use triage only when automatic specification/decomposition is desired. A triage create can promote the root to `todo` and create child tasks, so that behavior must be inspected rather than treated as an error.

## 4. Verify the resulting graph

- Verify each created root with `kanban show`, not only a single status-filtered list.
- Search all relevant statuses (`triage`, `todo`, `ready`, `running`, `blocked`) for auto-created children and inspect their assignees, project linkage, workspace kind, and scope.
- Verify attachments by task id, stored filename, content type, and byte size.
- Report exact ids, resulting statuses, child ids, attachment paths, and intentionally skipped duplicates. Do not claim a task was created from an unverified command result.

## 5. Runtime-trading evidence considerations

For simulated/live-parity ML order-book sessions, keep these dimensions separate:

- selected universe versus valid quote coverage and provider failures;
- transformer ready, warming, rejected input, and inference failure;
- valid HOLD versus generated signal;
- profitability/confidence gate blocker versus executable intent;
- local simulated fill versus persisted trade and closing outcome;
- worker cadence versus quote latency, WebSocket/API delivery, cache merge, and UI display cadence.

Do not recommend weakening risk gates or bypassing provider pacing merely to produce trades or increase refresh frequency.

## Pitfalls

- Do not create one catch-all card for several independently actionable failures.
- Do not count only `triage` results after using automatic decomposition.
- Do not treat a one-second worker sleep as proof of one-second UI refresh; measure every stage of the pipeline.
- Do not interpret a zero-trade run without reconciling HOLDs, quote failures, warm-up, blockers, intents, and fills.
- Do not call a wide per-symbol diagnostic table complete merely because pagination exists; verify readability, discoverability, and preservation of failed symbols.

## Support files

- `references/tmux-log-evidence.md` — reusable capture, parsing, attachment, and verification recipe.
