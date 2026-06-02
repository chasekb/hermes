# Hermes project workflow registry

This registry is the canonical project-level workflow index for intake, execution, review, and closeout.
Use the "Next action" column to decide what to do next without consulting a separate prose playbook.

| Workflow id | Trigger / entrypoint | Inputs | Outputs | Next action | Gate |
| --- | --- | --- | --- | --- | --- |
| backlog-intake | New idea, request, or gap | User request, backlog template | Draft backlog item | Fill the intake template, then hand off to backlog triage | Pre-flight |
| backlog-triage | Intake review | Draft backlog item | Accepted, deferred, or rejected item | Decide accept/defer/drop and capture the reason in backlog history | Revision |
| recommendation-to-task | A backlog item is accepted | Backlog item + dependencies | Runnable Kanban task slice | Render the accepted item into a runnable Kanban slice with preserved ids | Pre-flight |
| weekly-backlog-review | Scheduled weekly | Backlog store snapshot | Prioritized review notes and item updates | Run `scripts/review_backlog.py`, then write the review summary back to `backlog.json` | Revision |
| stale-item-review | Item has stopped moving | Old items + timestamps + blockers | Keep / defer / drop recommendation | Re-read the item, apply the stale heuristics, and if dropped hand off to `scripts/kanban_closeout_sync.py` | Escalation |
| review-closeout | Task claims completion | Kanban evidence + backlog item | Status transition + closeout note | Run `scripts/kanban_closeout_sync.py`; only close when evidence is attached | Abort if evidence missing |
| risky-change-review | Workflow, skill, hook, or backlog change is proposed | Diff, change budget, eval plan, rollback note | Promote / defer / abort decision | Apply `references/risky-change-gates.md`, then record the decision in backlog history or decision memory | Abort if eval or rollback proof is missing |
| skill-maintenance | Curator or review detects skill drift | Skill usage telemetry | Skill patch / archive / keep decision | Feed the result back into backlog or curator notes so the same rule can be reused | Revision |
| skill-promotion | A repeatable workflow emerges | Workflow notes + reusable steps | New or updated skill | Promote the workflow into a reusable skill and register the new path here | Revision |

Practical rule:
- The backlog store owns scope, criteria, and state.
- Kanban owns task execution and evidence collection.
- Workflow output should always write back to the backlog record, not just to chat.

Review cadence entry points:
- Weekly: `references/weekly-backlog-review.md` → `scripts/review_backlog.py`
- Stale-item: `references/stale-item-review.md` → `scripts/review_backlog.py` and `scripts/kanban_closeout_sync.py` when closeout is warranted
