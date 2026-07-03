# Remote Build Monitoring and Safe Cleanup

This note captures the reusable pattern used for GitHub Actions verification on the trade repo.

## Verification checklist

1. Commit and push the intended SHA.
2. Find the workflow run created by that push:
   - `gh run list --branch <branch> --limit <n>`
3. Verify the exact run against the pushed commit:
   - `gh run view <run_id> --json status,conclusion,headSha,url,name,workflowName,updatedAt,jobs`
4. Do not declare success until all jobs have final statuses and the run conclusion is `success`.
5. For matrix builds, inspect the individual jobs too:
   - frontend jobs may finish before backend jobs
   - publish/manifest steps may complete while compile jobs are still active
6. `gh run watch <run_id> --exit-status` is useful for live monitoring, but a timeout is not proof of failure; fall back to polling `gh run view` until the run finishes.

## Cleanup notes

Before trimming generated files after a push, run `git status` and remove only known build outputs.

Safe targets in this repo have included:
- `frontend/.next`
- `frontend/next-env.d.ts`
- `outputs/`
- `test_outputs/`

Do not remove local data or database directories without explicit approval. Treat `data/cache/` and `data/databases/postgres/` as preserved unless the user explicitly asks otherwise.
