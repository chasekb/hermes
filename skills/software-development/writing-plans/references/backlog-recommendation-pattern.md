# Backlog Recommendation Pattern

Use this pattern when the user asks for a project backlog recommendation rather than an implementation plan.

## When to use
- The user wants a durable backlog item created in a project-scoped backlog.
- The work needs execution and closeout criteria, not code yet.
- The request is about fixing a visible product problem, but the implementation should be deferred.

## Recommended shape
- Title: short, outcome-oriented, action verb first.
- Summary: one sentence describing the user-visible problem and desired outcome.
- Details: 2–4 short paragraphs or bullets covering the root issue and constraints.
- Execution checklist: concrete steps with checkboxes, ordered from discovery to implementation to verification.
- Parallel workstreams: 2–3 lanes that can be worked independently when practical.
- Closeout criteria: observable user-facing behavior and verification gates.
- Tags: include project, subsystem, and workflow labels.

## Quality rules
- Prefer specific observable behavior over vague intent.
- Make every checklist item testable or reviewable.
- Include visible failure states when the issue currently fails silently.
- If the problem involves large inputs or request limits, specify whether the fix is removal of a cap, pagination, batching, or streaming.
- If a fix spans frontend and backend, call out the contract boundary explicitly.

## Example fragments
- "Make Start Trading trigger an immediate status/statistics refetch"
- "Remove client-side symbol truncation in favor of paginated signal delivery"
- "Show loading and error states so the UI cannot appear stuck"
- "Confirm backend response includes pagination metadata and total counts"
