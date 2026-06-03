# Remote Build Verification Runbook

Use this when the user wants GitHub Actions to be the source of truth for a build or deploy.

## Goal
Verify the exact workflow run created by the latest push, and do not report success until all required jobs are completed successfully.

## Minimal checklist
1. Commit the change locally.
2. Push to the target branch.
3. Find the newest workflow run for that branch.
4. Confirm the run belongs to the commit you just pushed by matching `headSha`.
5. Poll the same run until every required job shows `conclusion=success`.
6. If GitHub API calls briefly fail, retry the same run id instead of assuming failure.

## Recommended commands
```bash
# List recent runs on the branch
 gh run list --branch <branch> --limit 10 --json databaseId,status,conclusion,workflowName,headSha,displayTitle,url,createdAt

# Inspect the authoritative run
 gh run view <run_id> --json status,conclusion,jobs,url,workflowName,headSha,displayTitle

# Optional live watch
 gh run watch <run_id> --exit-status
```

## Verification rules
- Never mix an older successful run with the newest push.
- If `status` is still `in_progress`, keep polling.
- Treat a workflow as successful only when `status=completed` and `conclusion=success`.
- If any required job is still running, the workflow is unresolved.
- Prefer `gh run view` as the source of truth; `gh run watch` is convenience.

## Common pitfall
A run can have some green jobs while one backend job is still running. Do not declare success early.
