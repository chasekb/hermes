# CI verification notes for trade repo

Use this when the user wants a push-and-verify flow backed by GitHub Actions.

Checklist:
1. Commit and push the branch.
2. Find the exact run created by that push with `gh run list --branch <branch> --limit <n>`.
3. Verify the run by exact SHA and URL, not just branch name.
4. Inspect job-level status when the overall run stays `in_progress` longer than expected.
5. Prefer `gh run view <run_id> --json status,conclusion,headSha,url,name,updatedAt` for the authoritative run record.
6. If `gh run watch` times out or is too noisy, poll with `gh run view` plus short sleeps instead of assuming failure.

Observed trade-repo notes:
- The repo’s Docker Build Validation workflow can keep one backend job in progress long after frontend jobs finish.
- A successful verification should cite the run URL and the pushed head SHA.
- Action deprecation warnings in the run log are informational unless they become job failures.