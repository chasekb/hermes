# GitHub Actions verification when the repo has no workflow yet

Use this when the user asks for a remote build proof but `gh run list` or `gh api .../actions/runs` shows nothing because the repository does not yet have an Actions workflow.

Pattern:
1. Add a minimal verification workflow to `.github/workflows/`.
2. Make the workflow validate the specific artifacts or files you need as proof.
3. Commit and push that workflow on the target branch.
4. Resolve the exact run created by that push.
5. Report the workflow name, run URL, and head SHA.

Checklist:
- Prefer a small, deterministic smoke workflow over a broad build matrix for the bootstrap run.
- Verify the workflow file itself is present in the pushed commit.
- Do not call the push verified until the run finishes successfully on GitHub.
- If the repo has multiple branches or workflow files, match the run by both branch and head SHA.
