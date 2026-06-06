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
- For matrix builds, inspect `jobs` in `gh run view --json status,conclusion,headSha,url,jobs`; don't call the run successful while any required job is still `in_progress`.
- If `gh run watch` stalls or times out, switch back to polling the same run id with `gh run view` instead of assuming failure.
- When reporting the result, include the exact run URL and the verified `headSha` so the user can tell which build was checked.

Session note:
- In the trade repo, a workflow run can show the frontend job as successful while the backend job is still running. Do not report the build as successful until the overall run is `completed` with `conclusion=success` and every required job has reached a terminal success state.
