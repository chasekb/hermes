---
name: project-backlog-workflows
description: "Class-level workflow for project backlog work: ingesting recommendations, researching scoped items, delivering implementations, and closing with evidence."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [backlog, project-planning, recommendations, research, delivery, ci, verification, closeout]
    related_skills: [shared-backlog, software-development-workflows, github-pr-workflow, containerized-build-verification]
    created_by: agent
---

# Project Backlog Workflows

Use this umbrella whenever the user asks to work from a project backlog, turn findings into backlog items, research an existing item, implement backlog criteria, or close items with evidence. It absorbs the narrower recommendation-ingestion, project-backlog-recommendations, project-backlog-research, and project-backlog-delivery lanes.

## Decide the lane first

1. **Ingestion / recommendation capture** — source material is a review, tmux pane, transcript, research note, or gap analysis and the requested output is new backlog items.
2. **Research / scoping** — backlog items already exist and the user wants exact files, symbols, tests, or feasibility without edits.
3. **Delivery / closeout** — backlog items already exist and the user wants implementation, validation, commit/push, and status closeout.
4. **Mixed project work** — split the session into lane-sized tranches; do not close items from mere research or create duplicates while implementing.

Always load the shared backlog contract if available before using the backlog CLI. Use the CLI/API contract; never edit backlog storage directly.

## Shared rules for every lane

- Preserve the user's requested project id; do not infer a different project from memory or another repository.
- Read/show the relevant project items before acting on them.
- Keep provenance precise and secret-safe.
- Deduplicate by title, description, provenance, and active project scope, not by exact title only.
- Treat execution criteria as the implementation checklist and closeout criteria as the evidence checklist.
- If repo state is dirty, avoid unrelated changes and mention only what affects the work.

## Lane A: ingest recommendations into backlog items

Use when the user says things like “file backlog items from this review,” “capture tmux pane recommendations,” “turn these findings into project backlog entries,” or “create backlog items with execution and closeout criteria.”

1. Capture/read the source without flooding context.
   - For large tmux panes, capture to a temp file and search for recommendation markers such as `recommend`, `P0`, `P1`, `critical`, `high`, `medium`, `TODO`, and review headings.
   - Preserve transient provenance such as `tmux:<session>:<pane>` plus durable artifacts such as `docs/reports/review.md:section`.
2. Extract independently actionable recommendations.
   - Split multi-topic reviews into separate items.
   - Ground candidates in the repo or source system where possible before writing final criteria.
3. Dedupe against active project items.
   - Existing closed/done items may justify a narrower follow-up, but do not recreate active work.
4. Create one backlog item per recommendation.
   - Map explicit priority: P0/P1/critical/high -> high, P2/medium -> medium, hygiene/nice-to-have -> low.
   - Include a description, provenance, repeated execution criteria, and repeated closeout criteria.
5. Verify creation.
   - Show the created ids and run a project-scoped list/status check.

### Criteria style for ingestion

Execution criteria should name trace/design/implementation/test paths. Closeout criteria should name proof: test commands, CI URLs, logs, artifacts, screenshots, queries, or no-action rationale.

## Lane B: research existing backlog items without editing

Use when the user asks to “research backlog item N,” “return exact files/symbols/tests,” “scope this item,” or explicitly says not to edit files.

1. Load/show the item and treat its description, provenance, execution criteria, and closeout criteria as the task source.
2. Preserve research-only boundaries.
   - Do not edit, format, stage, commit, move status, add notes, or close the item.
3. Trace from provenance to live code.
   - Inspect named files/lines and follow definitions/usages across UI, hooks, API clients, services, controllers, tests, docs, and configuration as needed.
4. Verify both sides of contracts.
   - For UI/config work, trace control rendering, state changes, payload building, and backend consumption.
   - For backend/API work, trace request shape, parsing, internal state, response, and test coverage.
5. Return implementation-ready scope.
   - Include exact files/line ranges, symbols, current flow, minimal implementation points, tests to add/update, and `Files modified: None`.

## Lane C: deliver and close backlog work

Use when the user asks to complete backlog items or a backlog project through implementation and proof.

1. Load project context.
   - List project items, show every item to implement, preserve priority/order, and mirror work in the session todo list.
2. Ground the implementation in the repo.
   - Read files named by criteria, trace usages before editing, and keep changes scoped.
3. Implement coherent tranches.
   - Group shared code paths when useful; keep docs/generated artifacts synchronized.
4. Verify before closeout.
   - Run targeted tests and required gates. If CI will be proof, still run local gates unless the user explicitly asks for remote-only proof.
5. Close through the backlog criteria workflow.
   - Move items through valid statuses, check execution criteria, mark done, check closeout criteria, and add evidence notes.
6. Commit/push when requested or required.
   - Stage intended files, commit with a scoped message, push, and verify the remote branch SHA.
7. Verify CI when available.
   - Match workflow runs by branch and head SHA, poll to completion, inspect failures, fix/repush if needed, and report the final URL and SHA.

## Report shapes

### Ingestion final
- Created ids with titles, priorities, and statuses.
- Provenance used.
- Verification command/result.
- Any duplicates intentionally skipped.

### Research final
- What I inspected.
- Key finding.
- Exact flow/contracts.
- Minimal implementation plan.
- Tests to add/update.
- Files modified: None.

### Delivery final
- Items completed/left open.
- Files changed and validation commands.
- Commit SHA and CI URL/head SHA when applicable.
- Any remaining blockers or intentionally deferred work.

## Pitfalls

- Do not create one huge catch-all item from a multi-point review.
- Do not close backlog items because code was written; complete execution criteria and closeout criteria with evidence.
- Do not treat research evidence as delivery unless the item explicitly only required investigation.
- Do not trust stale or unrelated CI runs; the run head SHA must match the pushed commit.
- Do not store secrets, personal data, live tokens, or giant transcripts in backlog fields.
- Do not let a path with spaces or shell metacharacters make you conclude a tool is broken; quote paths or run from a safe directory.

## Support files

- `references/backlog-recommendation-ingestion.md` — preserved detail from the recommendation-ingestion skill.
- `references/project-backlog-recommendations.md` — preserved detail and CLI pattern for review/log capture.
- `references/project-backlog-research.md` — preserved research-only boundaries and report outline.
- `references/project-backlog-delivery.md` — preserved delivery and CI closeout checklist.
