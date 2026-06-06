# GitHub Actions verification evidence bundle

Use this when the user explicitly wants GitHub Actions to prove a build completed successfully.

Minimal evidence to collect:
- workflow run URL
- run `status`
- run `conclusion`
- verified `headSha`
- required job list showing every required job reached a terminal success state

Authoritative query:
```bash
gh run view <RUN_ID> --json status,conclusion,jobs,headSha,url
```

Acceptance rule:
- Only report success when `status=completed` and `conclusion=success`.
- If the workflow is a matrix, every required job must be terminal and successful.
- If a newer push lands while verification is running, re-check the intended `headSha` before reporting.

Reporting template:
- Run URL: <url>
- Head SHA: <sha>
- Status: completed
- Conclusion: success
- Required jobs: all green

User-facing final answer rule:
- If the user asked for build verification, do not say "build passed" without the exact run URL and verified `headSha`.
- If the workflow is still running or queued, say so explicitly and continue polling the same run rather than switching to another run.
