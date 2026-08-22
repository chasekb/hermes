# Backlog Recommendation Ingestion (absorbed note)

Preserved details from the former `backlog-recommendation-ingestion` skill.

## Scope
Use when converting noisy source material—code review findings, terminal/tmux panes, documents, or captured transcripts—into project-scoped shared backlog items.

## Extra trigger phrases
- “capture tmux pane ... and create backlog recommendations”
- “file backlog items from this code review”
- “turn these recommendations into project backlog entries”
- “gap analysis recommendations into backlog”

## Pane capture details
- For large tmux panes, capture to a temp file rather than pasting scrollback into context.
- Preserve the pane target in provenance, e.g. `tmux:0:8.2`.
- Search for recommendation language, risk/gap wording, and explicit fixes.
- If the source is inaccessible or stale, scope the item as an investigation.

## Criteria reminders
Execution criteria should specify the work path: trace data/control flow, compare sibling tabs/modes, define formulas/policies, add edge-case tests, and create follow-up backlog items for separate fixes.

Closeout criteria should specify evidence: written file/line artifacts, passing tests/typecheck/lint/CI, manual UI evidence, proof that silent fallbacks are gone, or explicit no-action rationale.

## Verification
- Created items are assigned to the requested project.
- Each item has provenance, execution criteria, and closeout criteria.
- Duplicates were checked against active backlog items.
- `show` and a project-scoped `list` prove the created ids exist.
