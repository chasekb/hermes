# Remote build verification session note

Use this when the user asks to commit, push, and verify a GitHub Actions build.

Checklist:
1. Commit and push the exact SHA you want to prove.
2. Find the run created by that push with `gh run list --branch <branch> --limit <n>`.
3. Verify the run object with `gh run view <run_id> --json status,conclusion,headSha,url,name,updatedAt`.
4. Treat `gh run watch` as live monitoring only; if it times out, keep polling the exact run id with `gh run view` until the final conclusion is available.
5. Report the run URL and the verified `headSha` together.

Notes:
- Long-running Docker builds may remain `in_progress` for several minutes after early steps and still finish successfully.
- Prefer the push-triggered run for proof; do not use a sibling PR run on the same SHA as evidence for the push that the user asked you to verify.
- If a newer push creates a newer run on the same branch, switch to the newest run and verify that SHA instead.
