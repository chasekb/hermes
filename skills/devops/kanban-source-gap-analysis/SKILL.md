---
name: kanban-source-gap-analysis
description: "Use when comparing live data with upstream sources."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [kanban, gap-analysis, source-data, databases, reconciliation]
    related_skills: [project-backlog-workflows, kanban-orchestrator, shared-backlog]
---

# Kanban Source/Data Gap Analysis

Use this class-level workflow when a project needs durable Kanban tasking to compare a live database or object store with an upstream source, identify missing coverage, and route any remediation through implementation and review.

## Intake and scope

1. Confirm the target board, project, repository, live endpoint, collection/database, and source family.
2. Discover real worker profiles before assigning cards; never invent assignee names.
3. Read existing board/project tasks and deduplicate before creating new work.
4. Treat live data as read-only by default. Make destructive or bulk-ingestion scope explicit and separately approved.
5. Bound source probes and honor upstream rate limits; gap analysis is not an unbounded harvest.

## Canonical task graph

Create independent research parents first:

1. Storage audit: exact endpoint/collection, schema/config, total count, distinct identifiers, timestamp range, representative payloads, and access limitations.
2. Source audit: exact URLs, query parameters, sets, date windows, pagination/resumption, retry/rate-limit behavior, fields, and identifier semantics.

Then gate dependent work with explicit parent IDs:

3. Reconciliation: define join keys and date/set normalization; compare expected versus stored coverage; separate missing data from query-window, pagination, parser, normalization, persistence, embargo, and measurement gaps.
4. Remediation specification: rank gaps, name exact files/symbols/tests, define fixtures and negative controls, and state safety/rollback requirements.
5. Implementation: make only approved changes; add deterministic tests and update docs/config when behavior changes.
6. Review: verify implementation against source and storage evidence, run targeted tests/build/smoke checks, and report residual gaps.

Do not create dependent tasks as ready cards before their parents are complete. Use the board's dependency mechanism at creation time.

## Handoff and evidence contract

Every research task must return bounded commands, timestamps, raw or attached evidence, confidence/uncertainty, and the exact input required by its child. Reconciliation must include a gap matrix, counts, source queries/URLs, normalization rules, and at least one negative control or counterexample. Implementation and review must report exact files, tests, safety limits, and residual unknowns.

Record the next unblock requirement as a durable task comment on every gated card. A task is blocked only when human input, missing access, or an unresolved decision prevents progress; unfinished parents should remain dependency-gated `todo`, not be manually promoted.

## Creation and verification discipline

After each graph tranche:

- re-list the board and verify every returned task ID;
- show each new dependency boundary and confirm parent/child edges;
- check status counts and active diagnostics after dispatch;
- if a compound command fails, assume earlier creates may have committed, re-read the board, and retry only the missing card using an idempotency key;
- distinguish “no blocked tasks” from “all work is unblocked”—dependency-gated todo tasks are expected.

Set the board default workdir explicitly when workers need repository access. Use read-only directory workspaces for audits and isolated worktrees for implementation/review.

## Closeout

Do not mark research complete without reproducible evidence. Do not mark implementation complete without test/build/smoke proof. Do not mark review complete while unexplained residual gaps or required decisions remain; block with the exact missing input and the next action instead.

## Reference

See `references/kanban-gap-analysis-tasking.md` for the reusable graph template, handoff fields, safety rules, and failure/retry pattern.
