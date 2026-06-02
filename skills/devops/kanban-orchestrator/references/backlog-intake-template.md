# Backlog intake template

Use this template when capturing a new Hermes backlog item.

```yaml
id: HERMES-BL-0001
title: Short, action-oriented title
summary: One or two sentences describing the user-facing outcome.
scope: ~/.hermes
tenant: default
status: proposed
execution_criteria:
  - Condition that must hold before work starts
  - Testable behavior that defines the runnable slice
closeout_criteria:
  - Condition that must hold before the item can be closed
  - Evidence that proves completion
dependencies:
  - HERMES-BL-0000
notes:
  - Any constraints, links, or implementation clues
links:
  - https://example.com/reference
```

Guidelines:
- Write execution criteria before implementation details.
- Keep closeout criteria unambiguous and observable.
- Use stable ids so Kanban and reviews can backlink to the backlog item.
- Prefer small items that can be promoted into a single runnable slice.
