# GitHub Actions verification for long-running builds

Use this when you need to confirm a pushed commit is still building or has finished successfully.

## Recommended sequence

1. Identify the latest run for the exact commit:

```bash
gh run list --limit 10 --json databaseId,status,conclusion,workflowName,headSha,displayTitle,url
```

2. Inspect the run with jobs included so you can see step-level progress:

```bash
gh run view <RUN_ID> --json status,conclusion,jobs,url
```

3. If the run is still in progress, poll by re-running the same JSON view. The `jobs[].steps[]` array will show whether the workflow is actually moving forward even when the top-level status is unchanged.

4. Prefer `gh run view --json ...` over `gh run watch` when GitHub API latency/timeouts interfere with interactive watching.

## What to record

- run id
- workflow name
- head SHA
- status / conclusion
- current job and step names

## Useful fields

- `status`: `queued`, `in_progress`, `completed`
- `conclusion`: `success`, `failure`, `cancelled`, or empty while still running
- `jobs[].steps[]`: the best place to see which stage is active
