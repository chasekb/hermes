---
name: software-development-workflows
description: "Class-level development workflow: plan, implement, verify, debug, review, and simplify."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [development, planning, debugging, testing, review, delegation, refactoring]
---

# Software Development Workflows

Use this umbrella when the work is not just "write code" but a full development loop: clarify the change, plan it, implement it, verify it, debug failures, review for quality, and simplify the result.

## Core loop
1. Understand the goal and constraints.
2. Pick the right workflow: plan, test-first, debug, review, or orchestrate.
3. Make the smallest change that moves the work forward.
4. Verify with tests or an independent review.
5. Refactor only after behavior is locked in.

## Workflow families

### Planning
Use when the task is multi-step or needs a handoff-ready implementation path.
- Break the work into bite-sized tasks.
- Name files, commands, and expected verification.
- Keep the plan executable, not aspirational.

### Evidence-backed dashboard backlog recommendations
Use when the task is to turn a live UI/problem into multiple backlog recommendations that each prove one calculation or widget.
- Drive the real UI or frontend API enough to gather live evidence for every displayed value you intend to test.
- Capture a durable evidence note/report with the observed values, the widget/table rows, and the reproduction path.
- Create one recommendation per calculation or widget; do not bundle unrelated assertions into a single item.
- Each recommendation should carry its own execution checklist and closeout checklist, plus a link to the evidence report.
- Prioritize explicit formulas and normalization boundaries in the checklist so the eventual tests mirror the real data flow.
- When the UI depends on a local fallback session or simulated data path, record the exact activation path in the evidence note so future agents can reproduce it.
- See `references/trade-dashboard-evidence-workflow.md` for the reusable checklist and session notes.

### Test-first implementation
Use when creating or changing behavior.
- Write a failing test before production code.
- Watch it fail for the right reason.
- Implement the minimum to pass.
- Refactor only after green.

### Systematic debugging
Use when something is broken and the cause is unclear.
- Reproduce the issue.
- Read the error and trace the data flow.
- Form one hypothesis at a time.
- Fix the root cause, not the symptom.
- When frontend and backend response shapes differ, add one normalization boundary instead of scattering fallback logic across the component tree.
- If a helper has to support both authoritative backend values and local fallback derivations, test both paths explicitly.
- When a TypeScript error appears in one React component, trace the shared prop/hook shape upstream and fix the seam in all sibling consumers before loosening the type.
- Use small coercion helpers for render-time values (number/string/boolean) instead of widening the shared config object to `any`.
- When multiple sibling dashboard panels share the same config, fix the seam once and keep the setter semantics consistent (`React.Dispatch<React.SetStateAction<T>>`) across consumers.
- Avoid impure render fallbacks like `Date.now()`; render a safe placeholder or format an existing timestamp.
- Avoid synchronous `setState` inside `useEffect` when a user event or derived value can produce the same result.
- If `Object.values()` is iterating a record of unknown shape, cast it to `Record<string, T>` before filtering so the predicate can narrow cleanly.
- See `references/react-typescript-shared-shape-debugging.md` for a compact checklist and example failure patterns.
- See `references/trade-dashboard-normalization.md` for a concrete trade-dashboard normalization pattern and verification sequence.

### Independent review
Use before committing or merging.
- Inspect the diff in fresh context.
- Check security, correctness, and regression risk.
- Prefer an external reviewer or subagent over self-review.

### Subagent execution
Use when the work needs parallelism or isolated context.
- Give each task a narrow goal.
- Keep review separate from implementation.
- Use dependency links when tasks truly depend on each other.
- Prefer this umbrella skill over the legacy standalone `subagent-driven-development` file name; if older docs or prompts mention the narrow skill, treat them as referring to this section.

See `references/legacy-skill-aliases.md` for the absorbtion map and the `subagent-driven-development` history.

### Simplification and spikes
Use when the change is sprawling or uncertain.
- Simplify code after behavior is verified.
- Use a spike only to reduce uncertainty, then discard or rework it into the proper solution.

## Decision rules
- If the task has a clear spec and a testable result, prefer test-first implementation.
- If the task fails unexpectedly, prefer systematic debugging.
- If the task spans several files or steps, write a plan first.
- If the task is ready to land, run an independent review.
- If the task needs parallelism or isolated context, use subagents.

## Pitfalls
- Do not mix planning, implementation, and review into one undifferentiated pass.
- Do not skip tests because the change seems small.
- Do not patch symptoms before understanding the cause.
- Do not use a spike as a permanent solution.
- Do not accept your own review as sufficient when another perspective is available.

## Legacy subclasses absorbed into this umbrella
This class-level workflow replaces the narrower standalone skills for code review, debugging, TDD, implementation planning, subagent execution, simplification, and spikes.

## References
- Use support files under `references/` for reusable checklists, example prompts, and repo-specific diagnostics.
