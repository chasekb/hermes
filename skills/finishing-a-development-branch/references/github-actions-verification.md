# GitHub Actions verification for feature branches

Use this pattern when a branch is pushed and the user wants remote build proof:

1. Push the branch with `git push -u origin <branch>`.
2. Discover the newest workflow run for that branch:
   - `gh run list --branch <branch> --limit 1 --json databaseId,status,conclusion,headSha,url,workflowName,createdAt,updatedAt`
3. Verify the run is tied to the pushed commit SHA:
   - `gh run view <run_id> --json status,conclusion,headSha,url,workflowName`
4. Prefer the run URL and head SHA in the final response.
5. If `gh run watch` times out or is inconvenient, poll with `gh run view` / `gh run list` rather than assuming failure.
6. Treat the build as complete only when `status=completed` and `conclusion=success`.

Useful note:
- On long-running builds, `gh run watch` is fine for live feedback, but `gh run view` is the reliable final proof source.
