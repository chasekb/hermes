# Long-running GitHub Actions polling pattern

Use this when a remote build is expected to run for many minutes and a single `gh run watch` session is likely to time out or produce too much log output.

## Pattern
1. Push the branch.
2. Get the newest run id for the branch.
3. Poll `gh run view <run_id>` until the run is `completed`.
4. Only report success when the final conclusion is `success`.

## Commands
```bash
# Find the latest run for a branch
gh run list --branch <branch> --limit 10 \
  --json databaseId,status,conclusion,workflowName,headSha,displayTitle,url,createdAt

# Inspect run status and per-job progress
gh run view <run_id> --json status,conclusion,jobs,url,workflowName,headSha,displayTitle

# Poll in a shell loop instead of relying on one long watch session
while true; do
  gh run view <run_id> --json status,conclusion,jobs \
    --jq '.status, .conclusion, [.jobs[] | {name,status,conclusion}]'
  state=$(gh run view <run_id> --json status --jq '.status')
  concl=$(gh run view <run_id> --json conclusion --jq '.conclusion // ""')
  [ "$state" = completed ] && break
  sleep 60
done
```

## Notes
- If `gh run watch` is useful, use it for visibility, but do not depend on it as the sole verification mechanism for long builds.
- A long-lived watch can stall or time out even while the workflow keeps progressing; treat that as a polling problem, not proof of failure.
- If `gh` or the GitHub API times out temporarily, retry later and re-query the same run id.
- A background shell loop that prints the current status every 30-60 seconds is often the most reliable way to verify a very long remote build.
- Treat jobs individually: if one job is still `in_progress`, the workflow is not complete.
- Keep the final claim aligned with the run state: `completed` + `success` only.
