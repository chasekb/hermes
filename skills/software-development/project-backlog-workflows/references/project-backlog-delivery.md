# Project Backlog Delivery (absorbed note)

Preserved details from the former `project-backlog-delivery` skill.

## Delivery focus
Use when completing backlog projects or recommendation sets through implementation, validation, commit, push, and closeout.

## Evidence note shape
Include:
- local validation commands and pass result;
- pushed commit SHA;
- GitHub Actions run URL and matching head SHA when CI is proof;
- any fallback or degraded behavior that remains intentionally documented.

## CI closeout rules
- Do not rely on stale or unrelated CI runs; match `headSha` to the pushed commit.
- When the user asked to push to trigger CI, prefer the push-triggered run for final proof.
- If the matching CI run is still in progress after polling, do not claim success or close the item. Add an evidence note with the commit SHA, run URL, completed jobs, and still-running jobs; leave the item open/in_progress.
- If CI fails, inspect logs, fix root cause, repush, and verify the new matching run.

## Closeout pitfalls
- Do not close backlog items just because code was written.
- Do not let local machine state make tests pass only locally; make tests hermetic.
- Do not store secrets or personal data in backlog descriptions, criteria, notes, or closeout evidence.
- Do not treat a forced amend/push as proof by itself; re-check the remote branch SHA and new CI run.
