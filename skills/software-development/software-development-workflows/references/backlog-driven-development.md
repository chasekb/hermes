# Backlog-Driven Development Pattern

This note captures the reusable parts of the former `backlog-driven-development` skill.

## Shared-component rule
When multiple tickets point at the same code path, prefer one shared helper, formatter, or component rather than duplicating fixes across surfaces.

## Recommended checklist
1. Inspect the live backlog or implementation plan first.
2. Group items by underlying code path, not by ticket title.
3. Identify the smallest shared contract that can satisfy all of them.
4. Add regression coverage at that shared boundary.
5. Verify locally with the narrowest command that proves the behavior.
6. Push the branch and verify the exact remote CI run for the pushed SHA.
7. Close backlog items only after the proof exists.

## Pitfall to avoid
Do not let a UI/reporting backlog split into duplicated row, formatting, or calculation logic across sibling panels when a shared component can make the behavior consistent.
