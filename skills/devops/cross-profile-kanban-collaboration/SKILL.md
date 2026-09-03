---
name: cross-profile-kanban-collaboration
description: "Use for cross-profile Kanban collaboration."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [kanban, profiles, collaboration, orchestration, research]
    related_skills: [kanban-orchestrator, hermes-orchestrator-layout]
---

# Cross-Profile Kanban Collaboration

Use this umbrella when a user wants multiple Hermes profiles to inspect one another, study an existing board, or develop a durable autonomous workflow together. The goal is not merely to create cards: it is to establish a verifiable collaboration graph whose handoffs are explicit, whose board reads are scoped, and whose workers are actually spawnable.

## When to Use

Use when two or more named Hermes profiles must exchange structured findings, inspect a shared Kanban board, or jointly design a restart-survivable workflow. Use a simpler one-card task for a single specialist and no downstream synthesis.

## Core pattern

Use a fan-out / fan-in graph:

1. Discover the actual profiles before planning. Never invent assignee names.
2. Create one independent reconnaissance card per specialist. Each card should inspect the other profile and any relevant board read-only, then return a structured handoff.
3. Create one synthesis or workflow-design card with `parents=[...]` in the original create call. Keep it in `todo` until every reconnaissance parent is complete.
4. Dispatch only the independent parents first. Verify the returned task IDs, live status, worker claims, heartbeat, and lease.
5. Let the synthesis card promote only after the parent handoffs exist. Create follow-up implementation cards only when the synthesis findings determine their shape.

This preserves parallelism while preventing a synthesizer from running on missing evidence.

## Profile discovery and readiness

Before assigning work:

- Run `hermes profile list` and `hermes kanban assignees`.
- Confirm each intended assignee is on disk and has a configured model/provider.
- If a profile directory exists but `profile show` reports no model, configure it before dispatching.
- Prefer existing authenticated providers and role-specific profiles; do not silently substitute a different specialist.
- Verify with `hermes doctor` or per-profile `hermes -p <profile> config check`.

A profile name appearing in a board row is not sufficient evidence that it is spawnable. Treat `skipped_nonspawnable`, missing config, and immediate protocol exits as readiness failures that must be surfaced.

## Card design

Reconnaissance cards should include:

- Exact profile paths and role surfaces to inspect.
- The target board slug, explicitly named.
- A read-only constraint when inspecting an existing board.
- Required evidence: active tasks, statuses, assignees, dependencies, and recurring patterns.
- A structured handoff contract: findings, paths, evidence, proposed inputs/outputs, risks, and collaboration opportunities.

Synthesis cards should include:

- The parent handoffs as the source of truth.
- Role boundaries and task decomposition.
- Handoff schemas and artifact expectations.
- Validation gates and escalation conditions.
- Retry/idempotency behavior and a bounded pilot graph.
- An explicit prohibition on changing the source board or production systems unless a later card grants that scope.

For research, analysis, or trading workflows, require canonical data lineage, preprocessing rules, leakage controls, negative controls, uncertainty, and out-of-sample or execution-aware validation where applicable.

## Safe creation and dependency wiring

Use stable idempotency keys for each card. The CLI's JSON response uses `id` as the task identifier; do not assume a `task_id` field. Capture the returned `id` values before creating dependent cards.

Create parents first, then create the synthesis card with repeated `--parent <id>` flags (or the equivalent Kanban API `parents=[...]`). Do not create the synthesis card as an independent ready task and repair the graph afterward.

Use an explicit board selection, for example:

```bash
HERMES_KANBAN_BOARD=hermes hermes kanban create \
  "data-scientist: inspect quant profile and market board" \
  --assignee data-scientist \
  --idempotency-key profile-collab-ds-v1 \
  --body "Inspect profiles and read the market board only. Return structured evidence."
```

## Dispatch and verification

After creating the graph:

1. Run a dry-run dispatch to confirm intended assignees are spawnable.
2. Dispatch only the independent parents, capped to the intended fan-out.
3. Re-read `hermes kanban list` and `hermes kanban stats`.
4. For each running parent, verify `current_run_id`, `worker_pid`, `last_heartbeat_at`, and `claim_expires` in the board state.
5. Confirm the dependent synthesis card remains `todo` with the expected parent IDs.
6. If a worker exits without `kanban_complete` or `kanban_block`, reclaim the stale claim and report the protocol failure; do not mark the task done or repeatedly respawn blindly.

A successful dispatch call is not enough. The acceptance condition is a live worker claim with a recent heartbeat and a correctly gated downstream card.

## Collaboration boundaries

Keep profile reconnaissance and board inspection read-only by default. Do not let a cross-profile discovery card modify the source board, production trading systems, live orders, or durable project configuration. Route any mutation into a separate implementation card with explicit scope, tests, and review gates.

## Pitfalls

- Unknown or unconfigured profiles can leave cards apparently ready forever.
- A child without parent links may run before its evidence exists.
- A broad dispatch can launch unrelated ready work; cap it when starting a new collaboration graph.
- A task's title is not a handoff; require structured evidence and exact paths.
- A dispatcher returning `spawned` does not prove health; check heartbeats and process liveness.
- Do not normalize CLI response fields from memory; inspect the actual JSON shape.

## Supporting reference

See `references/profile-discovery-and-market-board.md` for a concrete, reusable reconnaissance and synthesis contract derived from a data-science / quantitative-trading collaboration pattern.
