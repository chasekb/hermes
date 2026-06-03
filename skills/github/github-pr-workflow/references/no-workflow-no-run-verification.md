# No-Workflow / No-Run GitHub Actions Verification

Use this note when a user asks for GitHub Actions proof of a build.

## Rule

An empty `gh run list` result is not proof of success. It usually means one of three things:

1. There is no workflow file in `.github/workflows/` that matches the event/branch.
2. The workflow exists but has not been triggered for the pushed commit.
3. The branch filter or event filter excludes the current push.

## Minimum checks

- Confirm workflow inventory first:
  - `gh api repos/<owner>/<repo>/actions/workflows --jq '.total_count'`
- If the count is `0`, report that Actions verification is unavailable until a workflow is added.
- If workflows exist but no runs appear, inspect the workflow triggers and the commit SHA/branch filters.
- Only claim success when a run exists with a matching `headSha`, `status=completed`, and `conclusion=success`.
- Include the run URL and verified `headSha` in the final report.
