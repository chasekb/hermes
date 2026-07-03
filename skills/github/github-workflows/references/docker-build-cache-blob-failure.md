# Docker BuildKit cache blob failure in frontend image builds

Observed failure pattern:
- `docker/build-push-action` frontend job compiles successfully in the builder stage.
- The failure occurs later during final image assembly, often at a `COPY --from=builder .../.next/standalone` step.
- BuildKit reports a missing blob from the GitHub Actions cache backend, e.g. `BlobNotFound` from `productionresultssa*.blob.core.windows.net`.

Practical fix:
- Treat this as a cache artifact failure, not an app-code failure, when the builder stage already completed.
- Disable the flaky GHA cache path for that build job, or rerun without cache, so image assembly is deterministic.
- Re-verify the exact pushed SHA with `gh run view <run_id> --json status,conclusion,headSha,url,jobs` after the new run completes.

Signal to look for in logs:
- `failed to copy: GET https://productionresultssa*.blob.core.windows.net/actions-cache/...`
- `404 The specified blob does not exist`
- `ERROR: failed to solve: failed to compute cache key`
