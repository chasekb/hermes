# Hermes project workflow registry

This registry describes the project-level workflows that turn backlog intake into execution and review.

| Workflow id | Trigger / entrypoint | Inputs | Outputs | Gate |
| --- | --- | --- | --- | --- |
| backlog-intake | New idea, request, or gap | User request, backlog template | Draft backlog item | Pre-flight |
| backlog-triage | Intake review | Draft backlog item | Accepted, deferred, or rejected item | Revision |
| recommendation-to-task | A backlog item is accepted | Backlog item + dependencies | Runnable Kanban task slice | Pre-flight |
| weekly-backlog-review | Scheduled weekly | Backlog store snapshot | Prioritized review notes and item updates | Revision |
| stale-item-review | Item has stopped moving | Old items + timestamps + blockers | Keep / defer / drop recommendation | Escalation |
| review-closeout | Task claims completion | Kanban evidence + backlog item | Status transition + closeout note | Abort if evidence missing |
| skill-maintenance | Curator or review detects skill drift | Skill usage telemetry | Skill patch / archive / keep decision | Revision |
| skill-promotion | A repeatable workflow emerges | Workflow notes + reusable steps | New or updated skill | Revision |

Practical rule:
- The backlog store owns scope, criteria, and state.
- Kanban owns task execution and evidence collection.
- Workflow output should always write back to the backlog record, not just to chat.
