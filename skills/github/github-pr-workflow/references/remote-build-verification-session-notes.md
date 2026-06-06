# Remote build verification session notes

Compact field notes for verifying GitHub Actions builds as the source of truth.

## Pattern that worked well

1. Identify the exact workflow run for the branch/commit.
2. Confirm the run's `headSha` matches the commit you intend to verify.
3. Poll the same `run_id` until `status=completed`.
4. Declare success only when `conclusion=success` and every required job is completed successfully.
5. Report both the run URL and the verified `headSha` to remove ambiguity.

## Useful commands

```bash
OWNER_REPO=$(git remote get-url origin | sed -E 's|.*github\.com[:/]||; s|\.git$||')
BRANCH=$(git branch --show-current)
SHA=$(git rev-parse HEAD)

gh run list --repo "$OWNER_REPO" --branch "$BRANCH" --limit 10

gh run view <RUN_ID> --repo "$OWNER_REPO" \
  --json status,conclusion,headSha,url,workflowName,displayTitle,jobs
```

## Polling guidance

- `gh run view` is the authoritative check for final status.
- `gh run watch` is fine for interactive use, but for long matrix builds it can be noisy and may time out in Hermes even while the run is healthy.
- If a workflow is still running, keep polling the same `RUN_ID`; do not switch to a different run on the same branch unless the user explicitly wants the newest one.
- A partially green matrix is not a success signal. Wait until every required job is complete.

## Field note from a real matrix build

In trade's `Docker Build Validation` workflow, the frontend jobs finished quickly while the backend jobs kept running for much longer. The run was only a real success once the slowest backend job finished and the run's final `conclusion` flipped to `success`.

The backend failure that preceded the fix was not a container/build-system problem; it was a consumer-contract mismatch in the ONNX smoke test. The exported model expected input shape `[1, 60, 10]`, but the smoke test supplied `[1, 10, 60]`, so onnxruntime rejected the input dimensions.

That field note matters because it reinforces two rules:
- do not read frontend success as overall workflow success
- when validating generated artifacts, check the consumer's expected tensor shape/order, not just file existence or parseability

## Final reporting checklist

- Run URL
- Verified `headSha`
- Final workflow `status`
- Final workflow `conclusion`
- Any still-running or failed jobs, if the run is not successful
