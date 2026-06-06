# Remote build proof bundle

Use this when the user wants GitHub Actions to be the source of truth for build verification.

Minimal proof bundle to collect before reporting success:
- Workflow run URL
- Run id
- Branch name
- Verified `headSha`
- `status=completed`
- `conclusion=success`
- All required jobs in a terminal success state

Checklist:
1. Find the exact run created by the latest push.
2. Match both branch and `headSha`; do not rely on the most recent run alone.
3. Inspect `gh run view <run_id> --json status,conclusion,headSha,url,jobs`.
4. If any required job is still running or queued, keep polling the same run id.
5. Only declare success when the whole run is completed and successful.
6. In the final reply, include the run URL and the verified `headSha` so the evidence is unambiguous.

Failure modes to avoid:
- Reporting a single green matrix leg as proof that the workflow finished.
- Concluding success while another required job is still in progress.
- Citing a run that matches the branch but not the commit SHA.
- Omitting the run URL or SHA from the final proof.
