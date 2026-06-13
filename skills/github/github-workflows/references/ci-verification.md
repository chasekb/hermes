# GitHub Actions verification checklist

Use this when the task is "commit, push, and verify via GitHub Actions".

1. Check auth:
   - `gh auth status`
2. Commit the work locally.
3. Push to the target branch.
4. Identify the exact workflow run created by the push:
   - `gh run list --branch main --limit 5`
5. Verify the run is the pushed commit:
   - `gh run view <run_id> --json status,conclusion,headSha,url,name,updatedAt`
6. If desired, watch until completion:
   - `gh run watch <run_id> --exit-status`
   - If the watch command is too chatty or times out, poll with:
     - `gh run view <run_id> --json status --jq '.status'`
7. Report the final result with:
   - workflow run URL
   - head SHA
   - conclusion

Important:
- A successful run on the same branch is not enough; always confirm the head SHA matches the pushed commit.
- If `git push` is rejected because the remote moved, rebase onto the remote branch, then push again.
