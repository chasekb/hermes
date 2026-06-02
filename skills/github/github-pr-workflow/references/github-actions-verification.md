# GitHub Actions verification runbook

Use this when the user wants a remote build/CI check instead of local verification.

## Goal
Verify a workflow run on GitHub Actions is fully successful before claiming success.

## Recommended sequence
1. Identify the most recent run for the branch or commit.
2. Inspect run-level status and jobs.
3. If the run is still in progress, re-check the same run later.
4. Only report success when the run is `completed` and `conclusion=success`.

## Commands
```bash
# List recent runs for a branch
gh run list --branch <branch> --limit 10 --json databaseId,status,conclusion,workflowName,headSha,displayTitle,url,createdAt

# Inspect the selected run
gh run view <run_id> --json status,conclusion,jobs,url,workflowName,headSha,displayTitle

# Optional live log stream when you want the full tail
# Prefer short use; for long builds, re-query gh run view instead of waiting on a long watch session.
gh run watch <run_id> --exit-status
```

## Practical notes
- `gh run view` is the authoritative check for completion state.
- `gh run watch` is useful for live logs, but for long-running builds it is better to poll `gh run view` again.
- If one job is still running, do not call the workflow successful yet even if other jobs have passed.
- When a build emits deprecation warnings or annotations, note them separately from the pass/fail result.
