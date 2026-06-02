# Remote-build-only workflow

Use when the user explicitly forbids local build/test verification and wants GitHub Actions to be the source of truth.

## Required sequence
1. Make the change.
2. Commit locally.
3. Push to the remote branch.
4. Query GitHub Actions for the resulting workflow run.
5. Wait for `completed` + `success` before claiming the build passed.

## Practical notes
- Use `gh run list --limit ...` to find the run triggered by the push.
- Use `gh run view <RUN_ID> --json status,conclusion,jobs,url` for the authoritative state.
- For long-running workflows, repeated `gh run view` polling is often more reliable than a single long `gh run watch` session.
- Treat `queued` and `in_progress` as unfinished even if logs show early setup steps completed.

## Failure handling
- If the workflow fails, inspect the failing job/step logs before changing code again.
- Keep the scope of the next change small so you can tell whether the failure was actually fixed.

## Related pointer
See `references/github-actions-verification.md` for the compact command set.