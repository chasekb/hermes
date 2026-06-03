# Remote Build Verification Runbook

Use this when the user asks to verify that a build completed on GitHub Actions instead of building locally.

## Rules
- Do not run local build/test verification first when the request is explicitly remote-CI-only.
- Treat the GitHub Actions run as the source of truth.
- Only report success when the run is `completed` with `conclusion=success`.
- If the run is still in progress, poll the same run again later rather than assuming failure.

## Preferred command flow
1. Identify the run tied to the latest commit or branch.
2. Inspect the run summary.
3. If needed, watch or poll until completion.

## Match the exact push
When the repo may have multiple recent workflow runs on the same branch, verify the run by branch and head SHA before calling it done.

```bash
gh run list --branch <branch> --limit 10 --json databaseId,status,conclusion,workflowName,headSha,displayTitle,url,createdAt
```

Use the entry whose `headSha` matches the commit you just pushed. If the newest run does not match, keep scanning older runs on the same branch until you find the one created by your push.

## gh commands
```bash
# List recent runs for the branch or commit
gh run list --branch <branch> --limit 10 --json databaseId,status,conclusion,workflowName,headSha,displayTitle,url,createdAt

# Inspect a specific run
gh run view <RUN_ID> --json status,conclusion,jobs,url,workflowName,headSha,displayTitle

# Optional live stream
gh run watch <RUN_ID> --exit-status
```

## Verification checklist
- Run id matches the commit or branch you intended to verify
- Every job is completed
- Workflow conclusion is success
- Any warnings are noted, but do not override a successful conclusion