# GitHub Actions verification checklist

Use this when the user wants remote CI/build verification instead of local build/test runs.

1. Identify the current branch and the latest commit SHA.
2. List recent workflow runs for that branch.
3. Select the run whose `headSha` matches the commit you want to verify.
4. Confirm the workflow is `completed` and every required job is `success`.
5. If the run is still in progress, keep polling the same run id; do not treat an intermediate snapshot as failure or success.
6. If another push lands while you are waiting, re-anchor on the newest matching `headSha`.

Practical rule:
- The authoritative answer is the workflow run view, not a local assumption or a single green job.
- Success means: workflow completed + all required jobs succeeded.
