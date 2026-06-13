---
project_id: hermes
note_type: project-playbook
updated_at: 2026-06-12T00:00:00Z
---
# Activity Tracking Checklist

Canonical Hermes checklist for tracking action execution, verification, and closeout.

## Operational rule
- Use this checklist in session summaries, backlog handoffs, and Kanban closeouts.
- Treat the checklist as the action ledger; pair it with evidence links instead of prose alone.
- Record each item in order and keep the wording stable across runs.

## Canonical checklist
1. Intake
2. Inspection
3. Action
4. Verification
5. Closeout

## Required fields for each step
- Step name
- Status
- Actor or session id
- Timestamp or order
- Evidence link
- Short result note

## State definitions
- started
- in-progress
- blocked
- verified
- closed

## Template
### Action: <title>
- [ ] Intake — identify the work, owner, scope, and evidence target.
- [ ] Inspection — read the relevant notes, files, or runtime surfaces.
- [ ] Action — make the change or perform the work.
- [ ] Verification — re-read, test, or inspect the result.
- [ ] Closeout — capture evidence links and mark the activity complete.

## Example usage
- action: Update Hermes research pages
- scope: /Users/bernardchase/.hermes/notes/Research
- evidence: /Users/bernardchase/.hermes/notes/Research/Research Workflow.md
- status: closed

## Usage notes
- Keep entries lightweight enough to use every day.
- Use this template for operational work; if the item is review-only, label it explicitly.
- If a task needs durable traceability, reference the checklist from the backlog item, session summary, or Kanban card.
- Closed or verified checklist entries can be promoted into decision memory when they carry durable action, scope, evidence, and status fields.
- Transient progress notes stay in the session summary or live workflow surface; do not promote them into memory.
