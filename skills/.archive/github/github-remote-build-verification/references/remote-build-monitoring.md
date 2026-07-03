# Remote build monitoring pattern

Use this when a push is meant to trigger GitHub Actions and that run is the source of truth.

## Reliable proof steps
1. Push the branch.
2. Record the pushed SHA immediately with `git rev-parse HEAD`.
3. Find the push-triggered run with:
   - `gh run list --branch <branch> --limit 10`
4. Inspect the run directly:
   - `gh run view <run_id> --json status,conclusion,headSha,url,name,workflowName,updatedAt`
5. Accept the build only if:
   - `status == completed`
   - `conclusion == success`
   - `headSha == pushed SHA`

## Monitoring notes
- `gh run watch` is useful for live progress, but it is not final proof.
- A run can stay `in_progress` for a long time while individual jobs finish at different times.
- Prefer `gh run view` for the final verdict and `gh run view --json jobs` if you need to see which job is still running.
- If multiple runs exist on the same branch, only the one whose `headSha` matches the pushed commit counts.

## Reporting format
When summarizing verification, report:
- pushed SHA
- run URL
- run status
- run conclusion
- whether the run matched the pushed SHA
