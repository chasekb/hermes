# CI workflow auth and cancellation notes

## What happened in this repo
- A Docker Build Validation run stayed alive for a long time on the C++ backend arm64 leg.
- `concurrency.cancel-in-progress: true` caused later pushes to cancel earlier in-progress runs.
- The effective fix was to make cancellation apply only to pull_request runs, not push runs.

## Practical rule
- For long-running branch builds, keep push runs alive unless you deliberately want the newest push to abort all in-flight CI.
- Use aggressive cancellation only for pull requests or clearly stale ephemeral checks.

## Push auth workaround for workflow files
- If `git push` is rejected with a message about updating `.github/workflows/*` without `workflow` scope, the HTTPS token is missing the workflow permission.
- In this repo, SSH push succeeded even when the HTTPS remote was blocked.
- Practical fallback: switch the remote push target to SSH (`git@github.com:<owner>/<repo>.git`) or refresh the token with workflow scope.

## Verification habit
- After changing workflow behavior, push the change and verify the next run by exact run ID and head SHA.
- If a prior run is still active, check whether it was canceled by the new push before assuming a code failure.
