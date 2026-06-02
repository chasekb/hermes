# Hermes capability priority list

This is an implementation-ready ordering of the highest-value capability work surfaced by the capability audit. It separates:
- already-present but untracked work
- items that mostly need activation/wiring
- items that require new implementation
- items to defer

## P0 — Activate and verify the core orchestration path

### 1) Hook router / hook coverage remains the top leverage point
- Status: already wired in `config.yaml` to `/Users/bernardchase/.hermes/agent-hooks/hook_router.py` across the major hook surfaces.
- Category: mostly activation / verification, not new implementation.
- Why now: this is the control plane for making all other capabilities reliable.
- Next action:
  - verify every intended event is actually routed at runtime
  - confirm `hooks_auto_accept: true` is behaving as intended
  - keep the router single-sourced instead of adding ad hoc hook logic elsewhere
- If it fails: fix hook routing or router dispatch first before adding new capabilities.

## P1 — Commit the highest-value capability bundles already present in the working tree

### 2) Containerized build verification is the strongest immediate capability win
- Status: already exists in the working tree as `skills/devops/containerized-build-verification/` and is heavily used in `skills/.usage.json`.
- Category: already exists untracked; needs activation/commit/cleanup, not new implementation.
- Why now: it directly improves local build triage, Podman/compose failures, CI verification, and safe cleanup boundaries.
- Evidence:
  - new skill directory is present but untracked
  - telemetry shows it is already active and high-use
  - it absorbed the old `workspace-cleanup` behavior
- Next action:
  - commit/activate the skill as the canonical container-debug workflow
  - keep the cleanup-boundary note attached to it
  - make sure the doc references are linked from the main skill entry

### 3) Kanban backlog bridge should be the execution backbone for Hermes-native work
- Status: already exists untracked under `skills/devops/kanban-orchestrator/` with scripts and reference docs, plus `backlog/README.md` and `backlog/backlog.json`.
- Category: already exists untracked; needs activation/wiring, not new implementation.
- Why now: it gives durable intake → triage → execution → closeout for project work.
- Next action:
  - wire the backlog bridge into the orchestrator skill as the default path for project work
  - keep backlog items as the source of truth and Kanban as the execution surface
  - standardize the review cadence (`weekly-backlog-review`, `stale-item-review`)
- Likely follow-up:
  - decide whether the backlog JSON should stay empty until real items are added or whether the current audit should seed an initial item set

### 4) GitHub PR workflow needs the remote-build-only verification path made canonical
- Status: the core skill already exists and is bundled; new reference docs are untracked (`remote-build-only.md`, `github-actions-verification.md` updates).
- Category: mostly activation / doc wiring, not new implementation.
- Why now: it prevents false-positive “passed” claims when CI is still running or only partly successful.
- Next action:
  - make the remote-build-only path the default when the user forbids local verification
  - keep `gh run view` as the authoritative completion check
  - ensure the skill points to the new verification reference instead of duplicating guidance

### 5) Systematic debugging should absorb the new DB/artifact fallback patterns
- Status: the core debugging skill already exists; the new fallback reference is untracked.
- Category: already exists with new reference material; needs activation/merge, not new implementation.
- Why now: it sharpens root-cause work on startup failures, missing tables, artifact write failures, and rootless Podman issues.
- Next action:
  - fold the fallback patterns into the main debugging playbook
  - keep the schema-optional query and writable-artifact patterns easy to find
  - avoid duplication between the main SKILL and the reference notes

## P2 — Fix and normalize maintenance capabilities

### 6) Agent self-improvement telemetry is already present; use it as a maintenance gate, not a new feature
- Status: already active and tracked in `skills/.usage.json`.
- Category: already exists and is active.
- Why now: it helps identify which skills are actually being used and which are becoming stale.
- Next action:
  - keep telemetry readouts tied to curator decisions
  - use it to detect low-value overlap before creating more skills
- Do not prioritize new implementation here unless the curator workflow itself is broken.

### 7) Repo publishing / hygiene helpers are useful, but secondary to the core workflow stack
- Status: already exists in the repo as bundled skills plus new untracked quickstart/reference docs.
- Category: mostly activation / doc polish.
- Why lower priority: useful for publishing repos, but less central than hooks, debugging, GitHub PR flow, and backlog routing.
- Next action:
  - keep the quickstart docs aligned with the main repo-management skill
  - only invest further if publishing existing workspaces is a frequent Hermes workflow

## P3 — Defer for now

### 8) Finance skill suite and other domain-specific additions
- Status: many finance skills exist as untracked directories.
- Category: likely new/expanded implementation, but not core to the Hermes platform priority stack.
- Why defer: they are valuable only for a narrower user segment and do not improve the core agent loop as much as the items above.
- Recommendation: leave them uncommitted unless there is an immediate finance-focused use case.

### 9) Docker language-server / LSP support
- Status: `lsp/package.json` and `lsp/package-lock.json` changed; `lsp/bin/docker-langserver` is untracked.
- Category: support tooling; likely new implementation or wiring work.
- Why defer: helpful for editor/tooling ergonomics, but lower impact than the workflow capabilities above.
- Recommendation: verify it after the core orchestration and debugging stack is stabilized.

## Retired / absorbed

### 10) `workspace-cleanup` should stay retired
- Status: archived and absorbed into `containerized-build-verification`.
- Category: no new implementation needed.
- Recommendation: do not resurrect it as a standalone capability unless the new umbrella proves insufficient.

## Recommended implementation order
1. Verify hook routing and keep it centralized.
2. Commit/activate `containerized-build-verification`.
3. Wire `kanban-orchestrator` to the backlog bridge.
4. Canonicalize the GitHub PR remote-build-only path.
5. Fold the DB/artifact fallback notes into systematic debugging.
6. Use telemetry to prune overlap and keep the skill set lean.
7. Defer finance and LSP support unless a concrete use case justifies them.
