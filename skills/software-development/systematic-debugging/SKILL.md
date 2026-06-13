---
name: systematic-debugging
description: "4-phase root cause debugging: understand bugs before fixing."
version: 1.1.1
author: Hermes Agent (adapted from obra/superpowers)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [debugging, troubleshooting, problem-solving, root-cause, investigation]
    related_skills: [test-driven-development, writing-plans, subagent-driven-development]
---

# Systematic Debugging

## Overview

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**Violating the letter of this process is violating the spirit of debugging.**

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## When to Use

Use for ANY technical issue:
- Test failures
- Bugs in production
- Unexpected behavior
- Performance problems
- Build failures
- Integration issues

**Use this ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work
- You don't fully understand the issue

**Don't skip when:**
- Issue seems simple (simple bugs have root causes too)
- You're in a hurry (rushing guarantees rework)
- Someone wants it fixed NOW (systematic is faster than thrashing)

## The Four Phases

You MUST complete each phase before proceeding to the next.

---

## Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

If the issue is a macOS CPU spike and the top process is `com.apple.Virtualization.VirtualMachine` (or similar Apple Virtualization framework binary), treat that as a VM-level symptom: inspect `podman machine list`, `podman stats --no-stream`, and container logs to find the underlying workload before blaming the host process itself.

### 1. Read Error Messages Carefully

For Hermes capability requests, confirm whether the user is asking for a toolset, a skill, or a model/provider change before acting. For example, if they ask to "install debugging toolset," check whether the active build actually exposes a `debugging` toolset; if not, treat it as a skill discovery/install question instead of repeatedly retrying the same command.

For long-running panes, logs, or streamed service output, isolate the relevant interval before you analyze:
- capture pane/log output starting from the last known-good marker or command
- if the user names a sentinel string or launch command, anchor the capture to the last occurrence of that string and read forward from there
- keep the exact failure window small enough to read end-to-end
- avoid reasoning from stale output that predates the current failure
- if a build is already running in a tmux pane or background session, prefer the live failure window over restarting it; overlapping runs often interleave cleanup noise and make the wrong failure look current

If a database-backed service is failing during startup, verify whether the failing table/view actually exists before treating the query error as the root cause. Optional/late-created tables should be checked explicitly so you can distinguish "missing initialization" from a true query bug.

If a UI action appears to do nothing, compare the exact frontend request target against the live backend route exposed by the running service before assuming the frontend is at fault. Verify the live endpoint with a direct request, then decide whether the fix belongs in the frontend, the backend, or both.

For Next.js dev dashboards, always verify the browser origin plus the resolved proxy target before changing code. If `/api/*` works via the browser origin but an absolute backend URL hits a different port, align `BACKEND_URL`, `NEXT_PUBLIC_API_URL`, and any websocket fallback ports with the live backend and restart the dev server.

For live dashboards and trading UIs, treat the rendered browser options as authoritative over stale docs or assumptions:
- inspect the actual select values/options in the running UI before patching code
- confirm the active request path/payload from the browser/network layer before changing backend routes
- if signal/trade tables grow without bound, look for append-only history where active rows should be deduped or replaced at the source
- prefer server- or data-layer ordering/pagination over client-only sorting when the dataset is large or continuously updating
- if a panel becomes stale after Start Trading / Stop Trading / strategy updates, verify the exact React Query keys used by the hooks and invalidate those exact keys; similarly named keys are a common no-op
- for large symbol universes, prefer chunked parallel requests plus merge/sort/re-paginate over silent truncation of the symbol filter
- make trading/simulation failures loud: if the API fails, surface the error instead of letting the button appear to succeed
- if simulated trading is “running” but no trades occur, verify the status endpoint, persisted trade list, and active-session state together; a signal-only loop can look healthy while execution is broken

If the user asks for logs or pane output "since" a marker in tmux (or any long-lived log stream), anchor the capture at the last occurrence of that marker or launch command, then read forward from there. Keep the failure window small and avoid analyzing earlier boot noise as if it were the current fault.

If container startup fails under rootless Podman, check for runtime-specific compose incompatibilities before touching the app code:
- unsupported sysctls (for example `vm.overcommit_memory`) may need to be removed from compose
- a registry `403 Forbidden` during bearer-token fetch usually means image pull auth is unavailable or insufficient, not that the image itself is broken
- when pull is blocked, use the local build fallback path and then re-run the same `up --no-build` command against locally available images
- run `podman-compose config` to confirm the rendered image names; `TAG=dev` alone does not guarantee the dev stack is using local tags
- if image unpack fails with `no space left on device`, check `podman system df` / `podman images` before changing app code and prune stale builder/image layers if needed
- if the Podman VM disk was resized but free space inside the guest barely changed, grow the guest partition/filesystem too (for example `growpart` followed by `xfs_growfs`) before assuming the resize failed
- before chasing app bugs from a failed `up`, capture the failure window from the last launch marker in tmux and ignore earlier boot noise
- if the dev stack is pulling unexpectedly, verify the rendered image names and any exported `CPP_BACKEND_IMAGE` / `FRONTEND_IMAGE` environment overrides before editing compose
- if `podman-compose up --no-build` still tries to resolve registry images, check whether the compose defaults are naming the images in a way that forces a pull (for example `localhost/...`), and prefer explicit local dev tags such as `trade-cpp-backend:dev` / `trade-frontend:dev`
- if a rootless Podman build gets deep into vcpkg and then fails on protobuf with `BUILD_FAILED`, treat it as a resource/concurrency problem first; try lowering `VCPKG_MAX_CONCURRENCY` before changing application code
- remember that `./data/...` paths in compose are often host bind mounts, not managed Docker volumes, so deleting them destroys local state

If a path-based artifact copy fails with permissions, probe the destination you actually intend to write to and use a writable fallback path before blaming the copy step.

For packaged ML/model artifacts, validate the copied runtime package, not just the source export:
- ONNX checker passing on the checked-in artifact does not guarantee the packaged copy will activate successfully
- compare the packaged `transformer.onnx` and its config/metadata against the source artifact when reload fails after training
- if the load error mentions `cannot create std::vector larger than max_size()`, suspect a shape/layout/metadata mismatch in the load path before assuming file corruption
- when packaging succeeds but activation fails, inspect the runtime reload path and package metadata before changing the training/export code
- keep exporter, loader, and packaged config in one contract; add a regression check for the canonical runtime `input_layout` (or equivalent) written by the exporter
- if a CI smoke test only exercises a lower-level export helper, switch it to the same higher-level packaging helper used in production so the generated config/metadata sidecars are present; otherwise you can get a false failure on a missing sidecar rather than the real runtime contract

**BEFORE attempting ANY fix:**

### 1. Read Error Messages Carefully

- Don't skip past errors or warnings
- They often contain the exact solution
- Read stack traces completely
- Note line numbers, file paths, error codes

**Action:** Use `read_file` on the relevant source files. Use `search_files` to find the error string in the codebase.

### 2. Reproduce Consistently

- Can you trigger it reliably?
- What are the exact steps?
- Does it happen every time?
- If not reproducible → gather more data, don't guess

**Action:** Use the `terminal` tool to run the failing test or trigger the bug:

```bash
# Run specific failing test
pytest tests/test_module.py::test_name -v

# Run with verbose output
pytest tests/test_module.py -v --tb=long
```

### 3. Check Recent Changes

- What changed that could cause this?
- Git diff, recent commits
- New dependencies, config changes

**Action:**

```bash
# Recent commits
git log --oneline -10

# Uncommitted changes
git diff

# Changes in specific file
git log -p --follow src/problematic_file.py | head -100
```

### 4. Gather Evidence in Multi-Component Systems

**WHEN system has multiple components (API → service → database, CI → build → deploy):**

**BEFORE proposing fixes, add diagnostic instrumentation:**

For EACH component boundary:
- Log what data enters the component
- Log what data exits the component
- Verify environment/config propagation
- Check state at each layer
- If an external API returns the same-looking data in multiple pipelines, verify the exact outbound request shape and the returned granularity before assuming the database is wrong
- Some APIs silently normalize unsupported parameter combinations instead of failing; compare the requested URL/params to the actual response contract
- If local build/test validation is blocked by the current machine's toolchain or dependency state, commit/push the narrow fix and use GitHub Actions (or the project’s remote CI) as the source of truth for final verification; watch the exact workflow run and only call it done when the run completes successfully

Run once to gather evidence showing WHERE it breaks.
THEN analyze evidence to identify the failing component.
THEN investigate that specific component.

### 6. When a filesystem path disappears

If a directory or file is missing and the cause is unclear:
- capture the tmux pane or log window around the last known-good marker
- determine whether the path was already empty before it vanished
- search the relevant shell history file(s) for exact path matches first
- then search broad removal/move patterns (`rm -rf`, `rmdir`, `mv`, `find ... -empty -delete`, `git rm`)
- check the parent directory's mtime/ctime to distinguish navigation from actual deletion
- if there is no matching command, assume another shell/process/cleanup job may have performed the change and keep looking before concluding

### 5. Trace Data Flow

**WHEN error is deep in the call stack:**

- Where does the bad value originate?
- What called this function with the bad value?
- Keep tracing upstream until you find the source
- Fix at the source, not at the symptom

**Action:** Use `search_files` to trace references:

```python
# Find where the function is called
search_files("function_name(", path="src/", file_glob="*.py")

# Find where the variable is set
search_files("variable_name\\s*=", path="src/", file_glob="*.py")
```

### Phase 1 Completion Checklist

- [ ] Error messages fully read and understood
- [ ] Issue reproduced consistently
- [ ] Recent changes identified and reviewed
- [ ] Evidence gathered (logs, state, data flow)
- [ ] Problem isolated to specific component/code
- [ ] Root cause hypothesis formed

**STOP:** Do not proceed to Phase 2 until you understand WHY it's happening.

---

## Phase 2: Pattern Analysis

**Find the pattern before fixing:**

### 1. Find Working Examples

- Locate similar working code in the same codebase
- What works that's similar to what's broken?

**Action:** Use `search_files` to find comparable patterns:

```python
search_files("similar_pattern", path="src/", file_glob="*.py")
```

### 2. Compare Against References

- If implementing a pattern, read the reference implementation COMPLETELY
- Don't skim — read every line
- Understand the pattern fully before applying

### 3. Identify Differences

- What's different between working and broken?
- List every difference, however small
- Don't assume "that can't matter"

### 4. Understand Dependencies

- What other components does this need?
- What settings, config, environment?
- What assumptions does it make?

---

## Phase 3: Hypothesis and Testing

**Scientific method:**

### 1. Form a Single Hypothesis

- State clearly: "I think X is the root cause because Y"
- Write it down
- Be specific, not vague

### 2. Test Minimally

- Make the SMALLEST possible change to test the hypothesis
- One variable at a time
- Don't fix multiple things at once

### 3. Verify Before Continuing

- Did it work? → Phase 4
- Didn't work? → Form NEW hypothesis
- DON'T add more fixes on top

### 4. When You Don't Know

- Say "I don't understand X"
- Don't pretend to know
- Ask the user for help
- Research more

---

## Phase 4: Implementation

**Fix the root cause, not the symptom:**

### 1. Create Failing Test Case

- Simplest possible reproduction
- Automated test if possible
- MUST have before fixing
- Use the `test-driven-development` skill

### 2. Implement Single Fix

- Address the root cause identified
- ONE change at a time
- No "while I'm here" improvements
- No bundled refactoring

### 3. Verify Fix

```bash
# Run the specific regression test
pytest tests/test_module.py::test_regression -v

# Run full suite — no regressions
pytest tests/ -q
```

### 4. If Fix Doesn't Work — The Rule of Three

- **STOP.**
- Count: How many fixes have you tried?
- If < 3: Return to Phase 1, re-analyze with new information
- **If ≥ 3: STOP and question the architecture (step 5 below)**
- DON'T attempt Fix #4 without architectural discussion

### 5. If 3+ Fixes Failed: Question Architecture

**Pattern indicating an architectural problem:**
- Each fix reveals new shared state/coupling in a different place
- Fixes require "massive refactoring" to implement
- Each fix creates new symptoms elsewhere

**STOP and question fundamentals:**
- Is this pattern fundamentally sound?
- Are we "sticking with it through sheer inertia"?
- Should we refactor the architecture vs. continue fixing symptoms?

**Discuss with the user before attempting more fixes.**

This is NOT a failed hypothesis — this is a wrong architecture.

---

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Pattern says X but I'll adapt it differently"
- "Here are the main problems: [lists fixes without investigation]"
- Proposing solutions before tracing data flow
- **"One more fix attempt" (when already tried 2+)**
- **Each fix reveals a new problem in a different place**

**ALL of these mean: STOP. Return to Phase 1.**

**If 3+ fixes failed:** Question the architecture (Phase 4 step 5).

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |
| "I'll write test after confirming fix works" | Untested fixes don't stick. Test first proves it. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new bugs. |
| "Reference too long, I'll adapt the pattern" | Partial understanding guarantees bugs. Read it completely. |
| "I see the problem, let me fix it" | Seeing symptoms ≠ understanding root cause. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. Question the pattern, don't fix again. |

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Root Cause** | Read errors, reproduce, check changes, gather evidence, trace data flow | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare, identify differences | Know what's different |
| **3. Hypothesis** | Form theory, test minimally, one variable at a time | Confirmed or new hypothesis |
| **4. Implementation** | Create regression test, fix root cause, verify | Bug resolved, all tests pass |

## Hermes Agent Integration

### Investigation Tools

Use these Hermes tools during Phase 1:

- **`search_files`** — Find error strings, trace function calls, locate patterns, and search shell history for exact path/removal commands
- **`read_file`** — Read source code with line numbers for precise analysis
- **`terminal`** — Run tests, check git history, reproduce bugs, capture tmux panes, and inspect live filesystem state
- **`web_search`/`web_extract`** — Research error messages, library docs

### Specialized debugging lenses consolidated into this umbrella

This umbrella now carries the class-level approach for several previously narrow debugging skills: live API contract checks, stateful runtime bugs, Hermes TUI command dispatch, and attach-based language debugging.

- **API contract checks** — verify the live route, payload, and transport before changing frontend or backend code.
- **Stateful service failures** — reproduce the exact user flow, identify the smallest shared resource, and prefer per-request lifetimes over global reuse.
- **Hermes TUI command debugging** — compare Python registry, gateway bridge, and Ink handlers side by side when a slash command works in one layer but not another.
- **Node / Python attach debugging** — use `node inspect`, CDP, pdb, or debugpy only when print/logging isn't enough.

## Field references

- **`references/frontend-backend-endpoint-diagnostics.md`** — endpoint mismatch triage for Next.js dashboards: verify the live browser origin, probe backend endpoints directly, and align rewrite/env fallbacks with the actual backend port before chasing 500s.
- **`references/db-and-artifact-fallback-patterns.md`** — practical notes on schema-optional startup, tmux capture windows, rootless Podman compose triage, Podman storage vs host disk, host bind-mounted artifact/data paths, and writable artifact fallback paths.
- **`references/onnx-model-activation-load-triage.md`** — session note for ONNX model packaging/activation failures where the exported file is valid but the copied runtime package still fails to load.
- **`references/onnx-package-contract-consistency.md`** — session note on keeping exporter, loader, and packaged config metadata aligned; includes the canonical-layout regression check.

- **`references/rootless-podman-compose-triage.md`** — tmux-window capture and compose-startup triage for rootless Podman, including sysctl rejection, GHCR pull fallback, local-tag verification, and storage exhaustion.
- **`references/tmux-pane-capture-window.md`** — exact recipe for capturing a tmux pane from the last named marker or launch command, preserving the failure window without stale boot noise.
- **`references/tmux-launch-marker-and-db-transaction-boundaries.md`** — note on anchoring tmux captures at the last launch marker and avoiding shared long-lived pqxx connections that can trigger "transaction still active" failures.
- **`references/tmux-and-venv-triage.md`** — tmux capture suffix anchoring plus project-venv targeting when shell activation leaves `python` on a shim instead of the repo interpreter.
- **`references/local-runtime-tmux-port-conflicts.md`** — tmux-captured local-stack troubleshooting notes: quote zsh extras, use `.venv/bin/python` explicitly, and confirm port ownership with `podman ps`/`lsof` before changing code.

When a managed host service is bound to the wrong port or collides with another local stack, move it to a free port and update every derived artifact together (`.ai-dev/config.json`, generated configs, entrypoints, Dockerfiles, tests, and docs) before re-verifying the live endpoint.
- **`references/cpu-hotspot-triage.md`** — macOS + Podman CPU-spike workflow: identify host hotspots, recognize Virtualization.framework VM load, and correlate with `podman stats` / `podman logs`.
- **`references/rootless-podman-vcpkg-protobuf.md`** — protobuf/vcpkg build failures under rootless Podman and the concurrency-cap workaround.
- **`references/rootless-podman-vcpkg-host-triplet.md`** — when vcpkg failures land in host/debug packages, align host+target triplets and force release-only overlay triplets.
- **`references/vcpkg-bootstrap-download-workarounds.md`** — deterministic CMake/bootstrap and GitHub archive download fallback pattern for vcpkg-heavy builds under rootless Podman.
- **`references/trade-podman-vcpkg-build-pressure.md`** — session-specific trade repo notes: tmux failure-window capture, local-tag verification, and storage-pressure triage for vcpkg-heavy builds.
- **`references/podman-remote-image-compose.md`** — remote GHCR image triage for compose: verify rendered refs with `podman-compose config`, remove stray `build:` blocks, and size the Podman machine for image unpack/runtime pressure.
- **`references/trade-podman-compose-runtime-debugging.md`** — session note for tmux-window capture, GHCR tag selection, Podman disk expansion, and post-start runtime failures in the trade stack.
- **`references/trade-simulated-trading-orderbook.md`** — trade-specific notes on Simulated Trading route mismatches, loud UI errors, live-UI option inspection, deduped signal tables, and starter configs for generating order-book training signals.
- **`references/orderbook-client-cap-triage.md`** — the client-side order-book symbol-cap pattern for large universes; keep the hook and API helper capped and log trims visibly.
- **`references/live-build-overlap-notes.md`** — tmux-captured build sessions with overlapping `podman-compose` runs, stale logs, and storage-pressure cleanup.
- **`references/yahoo-chart-silent-coercion.md`** — Yahoo Finance chart request note: unsupported `range`/`interval` pairs can silently coerce to coarse data; normalize intraday requests to a valid window and treat 1m promotion as interval-aware upsert territory.
- **`references/remote-ci-verification.md`** — commit/push + GitHub Actions verification loop for when local validation is blocked or incomplete.
- `references/hermes-debugging-capability-selection.md` — note on the Hermes-specific pitfall where users ask to install a "debugging toolset" but the build actually exposes debugging skills instead.
- `references/all-by-default-pagination-refactor.md` — checklist for converting capped pagination defaults to fetch-all-by-default behavior, including downstream callers and regression-test shape.
- `references/filesystem-disappearance-history-triage.md` — tmux + shell-history workflow for investigating when a directory seems to vanish, including empty-directory evidence and missing delete commands.
- `references/mlx-stack-rerun-and-tmux-triage.md` — repo-specific notes on stale tmux shell context, explicit repo interpreter verification, and making `ai-dev pull-models` rerunnable against existing local model directories.

### With delegate_task

For complex multi-component debugging, dispatch investigation subagents:

```python
delegate_task(
    goal="Investigate why [specific test/behavior] fails",
    context="""
    Follow systematic-debugging skill:
    1. Read the error message carefully
    2. Reproduce the issue
    3. Trace the data flow to find root cause
    4. Report findings — do NOT fix yet

    Error: [paste full error]
    File: [path to failing code]
    Test command: [exact command]
    """,
    toolsets=['terminal', 'file']
)
```

### With test-driven-development

When fixing bugs:
1. Write a test that reproduces the bug (RED)
2. Debug systematically to find root cause
3. Fix the root cause (GREEN)
4. The test proves the fix and prevents regression

## Real-World Impact

From debugging sessions:
- Systematic approach: 15-30 minutes to fix
- Random fixes approach: 2-3 hours of thrashing
- First-time fix rate: 95% vs 40%
- New bugs introduced: Near zero vs common

**No shortcuts. No guessing. Systematic always wins.**
