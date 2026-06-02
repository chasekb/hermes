# Project backlog model (Hermes-native)

A project backlog is the project's durable intake/spec layer. It belongs to Hermes, not to an external system.

Canonical store:
- `~/.hermes/backlog/backlog.json`

Recommended division of responsibility:
- Project backlog: intake, prioritization, scope, and criteria
- Kanban: execution, dependency management, handoff, and evidence

Item shape for backlog entries:
- id
- title
- summary
- scope / tenant
- execution_criteria
- closeout_criteria
- dependencies / blockers
- status
- notes / links
- created_at
- updated_at
- history
- evidence

Suggested lifecycle:
- proposed
- triaged
- accepted
- ready
- in_progress
- blocked
- done
- closed
- archived

How Kanban should consume backlog items:
1. Read the backlog item's execution_criteria first and derive tests from them.
2. Derive concrete worker tasks from those tests.
3. Copy the runnable slice into the Kanban task body.
4. Preserve the backlog item's stable id in task metadata or a backlink comment.
5. Keep dependency edges in Kanban, not only in prose.
6. Complete the Kanban task with evidence, not just a claim of done.
7. Reflect completion back into the project backlog once the closeout criteria are satisfied.

Placement guidance for criteria:
- execution_criteria belongs in the backlog item so it is visible before work starts.
- closeout_criteria belongs in the backlog item so completion is unambiguous.
- For backlog-driven work, derive tests before implementation tasks; tests should prove execution criteria and gate closeout criteria.
- Kanban task bodies may repeat a compressed checklist for the worker, but they do not replace the backlog's criteria.
- kanban_complete(metadata=...) should carry verification details, changed files, tests run, and residual risk.

Backlog review cadence:
- weekly backlog review for reprioritization and promotion into execution
- stale-item review for old or blocked items that need keep / defer / drop decisions

Example intent:
- backlog item says what must be true to count as ready/done
- Kanban task says how to execute the work today
- completion metadata proves what happened
