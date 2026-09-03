# Profile discovery and market-board collaboration contract

## Reusable task graph

Use two independent reconnaissance cards followed by one gated synthesis card:

- `data-scientist`: inspect the quantitative-trader profile and read the `market` board without mutation.
- `quantitative-trader`: inspect the data-scientist profile and read the `market` board without mutation.
- `engineering`: synthesize both handoffs into a bounded autonomous workflow, with both reconnaissance IDs as parents.

The reconnaissance handoff should contain:

1. Profile paths, model/provider, role instructions, and relevant skills.
2. Market-board counts, active task titles, statuses, assignees, and dependency patterns.
3. Data/artifact inputs and outputs the profile can provide.
4. Risks, validation gates, and concrete collaboration opportunities.

The synthesis handoff should contain role boundaries, task decomposition, handoff schemas, read-only discovery rules, artifact lineage, leakage/cost/survivorship/out-of-sample gates, escalation rules, retry/idempotency behavior, and a bounded pilot graph.

## Creation details

The Kanban CLI returns the task identifier under JSON key `id`, not `task_id`. Use idempotency keys when creating cards, capture the two returned IDs, and pass them as repeated `--parent` arguments on the synthesis card. Explicitly set `HERMES_KANBAN_BOARD` or use `--board`-equivalent selection; do not rely on a stale current-board assumption.

## Dispatch proof

A dry run should show the intended assignees under `spawned` and no `skipped_nonspawnable` entries. The real dispatch should be capped to the independent parent count. Verify `hermes kanban list`, `hermes kanban stats`, and the board's current run, worker PID, heartbeat, and lease for both parents. Leave the synthesis card in `todo` while either parent is incomplete.

## Safety boundary

Board inspection is read-only. Do not let discovery cards modify `market`, production trading systems, live orders, or durable configuration. Turn any mutation into a separately scoped implementation card with tests and review gates.
