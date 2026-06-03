# Remote build verification with GitHub Actions

Use this when the user wants the change validated by GitHub Actions instead of a local build.

Checklist:
1. Commit and push the branch.
2. Find the workflow run created by that exact push.
3. Verify both the workflow run and its job(s) on the same `headSha`.
4. Do not report success until `status=completed` and `conclusion=success`.

Practical sequence:
```bash
BRANCH=$(git branch --show-current)
SHA=$(git rev-parse HEAD)

gh run list --branch "$BRANCH" --limit 10 --json databaseId,status,conclusion,workflowName,headSha,displayTitle,url,createdAt

gh run view <RUN_ID> --json status,conclusion,jobs,url,headSha,workflowName,displayTitle
```

Verification rules:
- Match the run to the latest push by comparing `headSha`.
- If the run is still in progress, keep polling the same `RUN_ID`.
- If one job is still running, the workflow is unresolved.
- Use the run URL in the final report so the verified build is unambiguous.
- If the Actions API blips, retry the same run id rather than assuming failure.

Common mistake to avoid:
- Do not treat an older successful run on the same branch as proof for the new commit.
