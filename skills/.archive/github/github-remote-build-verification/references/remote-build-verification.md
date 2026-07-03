# Remote build verification pattern

Observed pattern for completion-proof builds:

- Commit the code change locally.
- Push the branch to trigger GitHub Actions.
- Capture the pushed commit SHA immediately after push.
- Use `gh run list --branch <branch> --limit 10` to find the push-triggered run.
- Use `gh run view <run_id> --json status,conclusion,headSha,url,name,createdAt,updatedAt` for final proof.
- Require `conclusion == success` and `headSha == pushed SHA`.
- Keep the workflow run URL as part of the delivery evidence.

Why this matters:
- A successful run on the branch is not enough if it belongs to an older commit.
- `gh run watch` is fine for progress, but the final proof should come from `gh run view`.
- The run URL and head SHA make the verification auditable later.

Suggested delivery format:
- commit SHA
- run URL
- run status/conclusion
- matched head SHA