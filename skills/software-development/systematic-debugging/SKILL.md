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

For long-running panes, logs, or streamed service output, isolate the relevant interval before you analyze:
- capture pane/log output starting from the last known-good marker or command
- if the user names a sentinel string or launch command, anchor the capture to the last occurrence of that string and read forward from there
- keep the exact failure window small enough to read end-to-end
- avoid reasoning from stale output that predates the current failure
- if a build is already running in a tmux pane or background session, prefer the live failure window over restarting it; overlapping runs often interleave cleanup noise and make the wrong failure look current

If a database-backed service is failing during startup, verify whether the failing table/view actually exists before treating the query error as the root cause. Optional/late-created tables should be checked explicitly so you can distinguish "missing initialization" from a true query bug.

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

Run once to gather evidence showing WHERE it breaks.
THEN analyze evidence to identify the failing component.
THEN investigate that specific component.

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

- **`search_files`** — Find error strings, trace function calls, locate patterns
- **`read_file`** — Read source code with line numbers for precise analysis
- **`terminal`** — Run tests, check git history, reproduce bugs
- **`web_search`/`web_extract`** — Research error messages, library docs

### Field references

- **`references/db-and-artifact-fallback-patterns.md`** — practical notes on schema-optional startup, tmux capture windows, rootless Podman compose triage, Podman storage vs host disk, host bind-mounted artifact/data paths, and writable artifact fallback paths.
- **`references/rootless-podman-compose-triage.md`** — tmux-window capture and compose-startup triage for rootless Podman, including sysctl rejection, GHCR pull fallback, local-tag verification, and storage exhaustion.
- **`references/tmux-pane-capture-window.md`** — exact recipe for capturing a tmux pane from the last named marker or launch command, preserving the failure window without stale boot noise.
- **`references/cpu-hotspot-triage.md`** — macOS + Podman CPU-spike workflow: identify host hotspots, recognize Virtualization.framework VM load, and correlate with `podman stats` / `podman logs`.
- **`references/rootless-podman-vcpkg-protobuf.md`** — protobuf/vcpkg build failures under rootless Podman and the concurrency-cap workaround.
- **`references/rootless-podman-vcpkg-host-triplet.md`** — when vcpkg failures land in host/debug packages, align host+target triplets and force release-only overlay triplets.
- **`references/vcpkg-bootstrap-download-workarounds.md`** — deterministic CMake/bootstrap and GitHub archive download fallback pattern for vcpkg-heavy builds under rootless Podman.
- **`references/trade-podman-vcpkg-build-pressure.md`** — session-specific trade repo notes: tmux failure-window capture, local-tag verification, and storage-pressure triage for vcpkg-heavy builds.
- **`references/podman-remote-image-compose.md`** — remote GHCR image triage for compose: verify rendered refs with `podman-compose config`, remove stray `build:` blocks, and size the Podman machine for image unpack/runtime pressure.
- **`references/live-build-overlap-notes.md`** — tmux-captured build sessions with overlapping `podman-compose` runs, stale logs, and storage-pressure cleanup.

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
