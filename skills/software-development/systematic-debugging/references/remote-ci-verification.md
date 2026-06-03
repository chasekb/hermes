# Remote CI verification for debug fixes

Use when local build/test validation is incomplete, flaky, or unavailable and the goal is to verify the exact fix that was just committed.

## Pattern

1. Make the smallest fix that addresses the suspected root cause.
2. Commit and push the change.
3. Trigger or inspect the remote CI workflow that exercises the affected target.
4. Watch the exact run to completion; do not treat `queued` or `in_progress` as verified.
5. If the workflow fails, inspect the failing job log and restart Phase 1 with the new evidence.

## Practical commands

- `gh run list --branch <branch>`
- `gh run view <run-id> --json status,conclusion,jobs`
- `gh run watch <run-id> --exit-status`
- `gh run view <run-id> --log-failed`

## What to capture

- workflow name
- run id
- final conclusion
- the first failing job/step if it fails
- any warnings that are informational only and do not block the build
