# Remote Build Monitoring Notes

Use this when a push should trigger a GitHub Actions verification run and you need the remote build to be the source of truth.

Checklist:
1. Commit the intended changes locally.
2. Push to the target branch.
3. Get the newest run for that branch with `gh run list --branch <branch> --limit 1`.
4. Verify the run's `headSha` matches the pushed commit SHA.
5. Only trust the run once `status=completed` and `conclusion=success`.
6. If an older run on the same branch succeeded, ignore it unless its `headSha` matches the current commit.
7. `gh run watch <run_id> --exit-status` is useful, but if it times out, fall back to `gh run list`/`gh run view` polling until the newest run finishes.
8. Report the run URL and head SHA together as proof.

Pitfalls:
- A successful older run does not prove the latest push built.
- The newest run can still be queued or in progress when a previous run already finished.
- Don't stop at a watched run if a newer push has already created a new run.
