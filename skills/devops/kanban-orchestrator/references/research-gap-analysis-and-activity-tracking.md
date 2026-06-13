# Gap analysis and activity-tracking recommendation patterns

Use these patterns when turning Hermes research into backlog recommendations.

## Pattern 1: gap analysis recommendation
Use when the task compares best practices against Hermes surfaces.

### Required execution criteria
- Inventory the relevant Hermes runtime, note, config, and backlog surfaces.
- Compare each research best-practice area to Hermes and label it covered / partial / missing.
- Tie every gap to a concrete Hermes file, note, or workflow surface.
- Produce a keep / improve / defer decision for each gap with rationale.
- Add testable follow-up recommendations when gaps matter.

### Required closeout criteria
- A gap matrix maps best-practice areas to specific Hermes surfaces and statuses.
- Every partial or missing area has a follow-up recommendation or a documented defer rationale.
- The analysis distinguishes runtime behavior, documentation, and aspirational best practice.
- A reviewer can reproduce the analysis from written evidence alone.

## Pattern 2: checklist-based activity tracking recommendation
Use when the task standardizes operational tracking for Hermes actions.

### Required execution criteria
- Define a canonical checklist covering intake, inspection, action, verification, and closeout.
- Record step name, status, actor/session, order or timestamp, and evidence link.
- Keep the checklist aligned with backlog, notes, and Kanban instead of creating a parallel system.
- Document a smoke path showing one action from start through closeout.

### Required closeout criteria
- A reviewer can follow one real Hermes activity end-to-end.
- The checklist is integrated with existing Hermes surfaces.
- States are unambiguous: started, in-progress, blocked, verified, closed.
- The artifact states whether checklist entries are operational, review-only, or both.

## Pattern 3: backlog recommendation closure via durable note artifacts
Use when the backlog item is implemented by creating or updating a durable note, index, or checklist artifact.

### Required execution criteria
- Create the target note or artifact first, not just the backlog record.
- Link the artifact from the relevant project index and any session-summary / decision-log note that should surface it.
- Update the backlog item only after the durable artifact exists and is readable.
- Record the exact path of the new artifact in evidence/links.
- Keep any summary entries short and avoid describing the artifact as implemented until it has been verified by readback.

### Required closeout criteria
- The durable artifact exists at the recorded path and is readable.
- The project index links to the artifact.
- Any related session summary or decision log entries are updated.
- The backlog item status is closed only after the artifact and links are verified.
- A reviewer can open the artifact and follow the linked trail without reconstructing the session.

## Good practice
- Keep recommendations focused on the smallest durable slice.
- Put implementation detail in execution criteria; put acceptance proof in closeout criteria.
- Include exact file paths in evidence/links whenever possible.
- If a recommendation depends on runtime behavior, verify the runtime first rather than treating notes as proof.