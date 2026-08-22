# Remote CI evidence checklist

1. Confirm the intended branch and exact commit SHA before pushing.
2. After push, query workflow runs by branch and filter by `head_sha` equal to the pushed SHA.
3. Distinguish push and pull-request events; use the requested event as proof.
4. Poll the same run id until top-level `status=completed` and `conclusion=success`.
5. Inspect every required job, including all architecture variants and manifest/publish jobs.
6. Record the run URL, SHA, terminal conclusion, and job names in the backlog note.
7. Check runtime-only criteria only after actually collecting the requested logs, API output, artifact, or screenshot.
8. If closeout rejects incomplete criteria, leave the item `done` or `in_progress` and report the missing evidence instead of forcing closure.
