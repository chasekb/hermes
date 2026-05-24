# Project backlog model (Hermes-native)

A project backlog is the project's durable intake/spec layer. It belongs to Hermes, not to an external system.

Recommended division of responsibility:
- Project backlog: intake, prioritization, and criteria
- Kanban: execution, dependency management, handoff, and evidence

Item shape for backlog entries:
- title
- summary
- project scope / tenant
- execution_criteria (what must be done to start/complete the runnable slice)
- closeout_criteria (what must be true before the backlog item is considered finished)
- dependencies / blockers
- status
- notes / links

How Kanban should consume backlog items:
1. Copy the runnable slice into the Kanban task body.
2. Preserve the backlog item's stable id in task metadata or a backlink comment.
3. Keep dependency edges in Kanban, not only in prose.
4. Complete the Kanban task with evidence, not just a claim of done.
5. Reflect completion back into the project backlog once the closeout criteria are satisfied.

Placement guidance for criteria:
- execution_criteria belongs in the backlog item so it is visible before work starts.
- closeout_criteria belongs in the backlog item so completion is unambiguous.
- Kanban task bodies may repeat a compressed checklist for the worker, but they do not replace the backlog's criteria.
- kanban_complete(metadata=...) should carry verification details, changed files, tests run, and residual risk.

Example intent:
- backlog item says what must be true to count as ready/done
- Kanban task says how to execute the work today
- completion metadata proves what happened
