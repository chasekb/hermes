---
project_id: hermes
note_type: workflow-registry
updated_at: 2026-09-04T00:00:00Z
---
# Branching and Workflow Integration

## Current workflow branch registry

- MacBook Air workflow: `workflow/macbook-air-m5` at review HEAD `45642bd5b138dd7d563b0ddd7185afaa76f45750`.
- Linux/Arch workflow delivery branch: `workflow/linux-arch` (this review's push target).
- Configuration gap artifact: [[MacBook Air Workflow Configuration Gap Analysis]].
- Verification workflow targets `main`, `workflow/macbook-air-m5`, and `workflow/linux-arch` after this delivery.

## Operating policy

- Use `main` as the integration branch, not as a long-lived scratchpad.
- Prefer one active working branch per machine.
- Keep the worktree clean before switching machines.
- If both machines may be used at the same time, use separate branches.
- Before editing on another machine: fetch origin, inspect status, reconcile with the intended base, and verify that generated files are not being mistaken for source changes.

## Handoff checklist

1. Run `git status --short --branch`.
2. Commit or intentionally park current work on a short-lived branch.
3. Push the branch when another machine will continue it.
4. Record branch-specific notes and exact commit SHAs here.
5. Verify the exact pushed SHA and every required CI job before closeout.
