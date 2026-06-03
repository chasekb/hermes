# GitHub Actions Remote Build Proof

Use this when the user explicitly wants GitHub Actions to prove a build completed successfully.

## Goal

Verify the exact workflow run created by the latest push, not just a branch-wide status.

## Checklist

1. Capture the commit SHA that was pushed.
2. Find the workflow run for that branch and SHA.
3. Confirm the run matches both:
   - the intended branch
   - the exact `headSha`
4. Poll the same run until:
   - `status = completed`
   - `conclusion = success`
5. Do not report success while any required job is still running.
6. When reporting back, include:
   - the run URL
   - the verified `headSha`

## Pitfalls

- Do not confuse an older successful run on the same branch with the newest pushed commit.
- Do not treat partial green jobs as completion.
- If GitHub API calls are transiently noisy, retry the same run id rather than changing the target.

## Recommended commands

- `gh run list --branch <branch> --limit 10 --json databaseId,status,conclusion,headSha,url`
- `gh run view <RUN_ID> --json status,conclusion,jobs,url,headSha`
- `gh run watch <RUN_ID> --exit-status`
