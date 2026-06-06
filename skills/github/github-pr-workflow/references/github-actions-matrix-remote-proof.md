# GitHub Actions matrix remote proof

Use this note when a push triggers a matrix workflow and you need to prove the build really completed.

## What to verify

1. Match the exact run created by the push.
   - Confirm the branch name.
   - Confirm the `headSha` matches the commit you pushed.
   - Use the run URL from `gh run view` or `gh run list`.

2. Check the whole run, not just one job.
   - A workflow is not successful while any required job is still `in_progress` or `pending`.
   - For matrix builds, one axis finishing early does not prove the others passed.
   - If there is a publish/manifest job, it is part of the success criteria when the workflow depends on it.

3. Prefer structured polling over a single watch.
   - `gh run watch` is convenient, but `gh run view <id> --json status,conclusion,headSha,url,jobs` is the reliable source of truth.
   - If watch times out, keep polling the same run id rather than switching to a newer run by accident.

4. Report with the exact evidence.
   - Include the run URL.
   - Include the verified `headSha`.
   - Mention the final run conclusion and which jobs succeeded/failed/skipped.

## Minimal command set

```bash
gh run list --branch <branch> --limit 10 --json databaseId,status,conclusion,workflowName,headSha,url

gh run view <RUN_ID> --json status,conclusion,headSha,url,jobs

gh run view <RUN_ID> --log-failed
```

## Common trap

A backend job can still be running even after the frontend jobs are green. Do not report success until the backend shard(s) and any downstream manifest/publish jobs have finished successfully.

## Field note

In the trade repo, a matrix workflow showed frontend success first while backend jobs were still running. The run was only verifiable once every required job reached a terminal state; early green jobs were not enough.
