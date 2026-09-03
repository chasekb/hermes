# Configuration-remediation Kanban intake

Use this reference when a Hermes settings review produces durable Kanban work.

## Recommended lane split

- Reliability: gateway state, cron failures, update backups, timezone, service verification.
- Provider/cost: fallback providers, local endpoint tests, auxiliary model routing, free-only policy.
- MCP/reproducibility: enabled-server inventory, package pinning, read-only database wrappers, stale-key cleanup.
- State maintenance: session retention, pruning, vacuum, live-session and agent-cache bounds.
- Security: strict gateway mode, platform allowlists, Tirith policy, media limits, unattended-operation boundaries.

Do not merge these into one card unless the work is genuinely sequential. Each lane should name the exact config keys and observed evidence that motivated it.

## Card contract

Every remediation card should contain:

- Scope and source report path.
- Execution checklist with discovery before mutation.
- Snapshot/rollback requirement.
- Explicit secret-handling prohibition.
- Explicit prohibition on deleting database data directories.
- Closeout criteria with config/doctor/runtime verification.
- Blocker behavior when credentials, model IDs, or human approval are missing.

## CLI details learned from a live creation pass

Use the board flag before the subcommand:

```text
hermes kanban --board hermes create "title" --body "..." --assignee engineering --priority 0 --project hermes --idempotency-key hermes-config-example-v1 --json
```

`--priority` is an integer. A lower integer is the stronger queue priority; use a consistent local convention such as `0` for P0 and `10` for P1. Assignees must come from `hermes profile list`.

Use idempotency keys on every card. If creation must be retried, reusing the same key should return the existing non-archived task rather than creating a duplicate.

## Verification

After creation, read back the board as JSON and verify each requested title exactly once, with the expected assignee, status, priority, workspace kind/path, and resolved project identifier. A successful create response is not sufficient proof that the board contains the intended task set.
