---
name: backlog-implementation-workflow
description: Execute a codebase backlog or implementation plan end-to-end with repo grounding, task tracking, targeted tests, and real verification.
---

# Backlog Implementation Workflow

Use this skill when the user asks to complete one or more backlog items, P1/P0 tasks, or a written implementation plan inside an existing repository.

## Core principles
- Ground every item in the repository before editing.
- Keep each backlog item separate until it is individually verified.
- Use TodoWrite to mirror the backlog and track progress.
- Add or update focused tests for the behavior you introduce.
- Do not report completion until you have a real build/test signal.

## Workflow

### 1) Orient
1. Check git status.
2. Read the relevant backlog/plan documents.
3. Trace the code paths, types, and call sites affected by each item.
4. Create a todo list that mirrors the work one-for-one.
5. If the request is framed as a backlog, preserve the backlog's existing priority order rather than re-sorting it by convenience.

### Backlog-specific implementation patterns
- Treat each P0/P1 item as a separate deliverable with its own code change, test coverage, and verification step.
- When the work spans ML/trading code, keep cohort/metrics logic, sizing logic, and UI/API wiring distinct until each layer is proven.
- If a new metric or policy depends on historical results, wire it through serialization/cache paths at the same time so downstream consumers can use it immediately.
- For validation runs that may take a while, start the real build/test and continue until the process exits; don’t stop after seeing early progress logs.
- Use a support reference for the trade-project pattern: `references/backlog-implementation-notes.md`.

### 2) Implement
1. Mark one item in progress.
2. Make the smallest code change that addresses that item.
3. Update build wiring if new sources/tests are added.
4. Add or adjust tests that prove the new behavior.
5. Repeat for the next item only after the current one is verified.

### 3) Verify
1. Run the narrowest test or build command that exercises the change.
2. If the task spans multiple subsystems, verify each subsystem separately, then run one broader build pass.
3. If verification is long-running, keep tracking it until it exits successfully.
4. Mark todo items complete only after verification.

## Reporting
- Summarize what changed, where it changed, and what was actually verified.
- Mention blockers plainly if the environment or build still prevents proof.
- Prefer path references and command results over narrative claims.

## Supporting material
- Session-specific implementation notes belong in references/.
- See references/backlog-implementation-notes.md for the reusable pattern from the trade project.
