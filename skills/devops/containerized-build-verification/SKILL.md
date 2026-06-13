---
name: containerized-build-verification
description: Debug, stabilize, and verify containerized builds and CI runs for local compose/Podman/Docker workflows.
---

# Containerized Build Verification

Use this skill when a task involves:
- local container/compose startup failures
- build logs inside a tmux pane or background job
- deciding whether a workflow is actually finished
- pushing a fix and confirming success in CI
- stopping a local build and cleaning up only transient artifacts

## Core workflow

1. Identify the current execution mode.
   - Local build/runtime? Inspect live logs first.
   - CI verification? Inspect the authoritative workflow/run status, not just a single job.

2. Capture only the relevant log window.
   - If the failing process is in tmux, capture from the last clear sentinel/marker so the new failure is isolated from older noise.
   - Prefer a short, targeted slice over a full-pane dump.

3. Classify the failure.
   - Startup/runtime issue
   - Build/packaging issue
   - Dependency/image pull issue
   - CI orchestration issue
   - Resource exhaustion or timeout

4. Fix the smallest layer that explains the failure.
   - Compose/config before code when the failure is in wiring.
   - Code before build flags when the failure is in the app.
   - Build flags or resource limits before redesigning dependencies.

5. Verify the fix at the same layer that failed.
   - If local startup failed, rerun local startup.
   - If CI is the source of truth, verify the workflow run to completion.

## CI verification rules

- When GitHub Actions is the source of truth, treat the request as remote-only verification: do not spend time on a local build/test if the user explicitly wants the CI run as proof.
- Verify the exact workflow run created by the latest push by matching both the branch and the commit SHA (`headSha`); do not confuse it with an older run on the same branch.
- If `gh run list` returns an older or unrelated run on the same branch, do not trust it just because it is the newest displayed row. Re-query with the Actions API and match `headSha` against the pushed commit before you start polling.
- For ambiguous branch results, prefer `gh api 'repos/<owner>/<repo>/actions/runs?branch=<branch>&per_page=<n>'` or `gh run view <run_id> --json ...` over a one-line `gh run list` summary so you can see the exact `headSha`, `status`, and `conclusion` for each candidate run.
- If `gh run list` is empty for the branch or commit, do not call that success or failure yet: first confirm that workflow files exist and that their event filters include the push. If workflow inventory is zero, report that GitHub Actions verification is unavailable until a workflow is added.
- If a workflow is still in progress, keep polling the same run id; do not infer failure from an intermediate state.
- Do not report success until every required job in the run is completed with `conclusion=success`.
- When you report success, include the run URL and the verified `headSha` so the result is unambiguous.
- If the user explicitly asks to use GitHub Actions to verify build completion, follow the remote-only proof pattern instead of doing a local build first.
- When merging a fix to `dev`, verify the workflow run created by the merge commit on `dev` itself; if `gh pr merge` fails because the branches have diverged or fast-forwarding is impossible, merge through the GitHub API and then re-anchor CI verification to the merge commit SHA.
- When a CI failure is a link-time failure after changing a smoke test to call a production helper, inspect the test target’s source list and linked libraries before touching the app code. A common cause is the test compiling the new call site without linking the implementation file or transitive dependency library.
- If a smoke test only exported the raw artifact but the production flow writes a config/metadata sidecar too, switch the test to the same higher-level packaging helper used in production so the runtime package is exercised end-to-end.
- See `references/no-workflow-no-run-verification.md` for the short checklist when workflow inventory is zero or `gh run list` comes back empty.

### Polling discipline for long builds

- `gh run watch` is convenient for live logs, but polling `gh run view <run_id> --json status,conclusion,jobs,headSha,url` is the source of truth when the run is long-lived or matrix-heavy.
- If a watch command times out, resume from the same run id instead of starting over or assuming failure.
- A run is only complete when the top-level `status` is `completed` and the top-level `conclusion` is `success`.
- If one required job is still running, the workflow is unresolved even if other jobs are green.
- When the user asks for proof of completion, capture the final run URL, verified `headSha`, terminal `status`, terminal `conclusion`, and the required job names that actually mattered.

### Remote-build run selection pitfalls

- The branch’s visible run may lag behind the most recent commit if a newer push is still being indexed. Always compare the run’s `headSha` to the commit you just pushed.
- A pull-request workflow may show the PR number/title rather than the exact push event; use the run’s `headSha` as the anchor, not the display title.
- If you need to recover from an interrupted check cycle, re-query the same run id; do not replace it with a different in-progress run unless the head SHA matches the pushed commit.

See `references/github-actions-remote-build-proof.md` for the shortest checklist when the user only wants GitHub Actions as proof of build completion.

## Local container-debugging rules

- Separate environment wiring problems from application bugs.
- When a compose stack starts partially, inspect the earliest failing service first.
- If the first explicit error is an auth/config failure (for example Postgres password mismatch), compare the app's env defaults to the live container's env before changing code.
- If DB auth is failing, verify the target database exists inside the container with `psql` so you know whether the issue is credentials or provisioning.
- For background builds, stop the process cleanly when the user asks; do not keep iterating in the background.
- When a compose stack is intended to use local images with `up --no-build`, make the image names explicit local tags (for example `trade-cpp-backend:dev` / `trade-frontend:dev`) and verify the rendered config with `podman-compose config` before launching. Otherwise Compose may try to pull registry tags again and fail during unpacking or dependency resolution.
- When the user asks for a tmux capture "since" a launch command or marker, anchor the capture at the last exact occurrence of that command (for example `TAG=dev podman-compose up --no-build`) and read forward from there; do not summarize from older boot noise.
- If a model-load warning is emitted after training but the service still has enough context to answer with degraded defaults, prefer an explicit fallback response over turning the warning into a request-level hard error; surface `models_ready=false` plus a warning field so the UI can continue.
- For simulated-trading dashboards, treat a "trained but empty widgets" report as a backend-liveness and request-shape problem first: verify `/api/simulated-trading/status`, inspect the live order-book request payload, and check the worker loop for per-tick exceptions before changing frontend polling code.
- If `podman-compose config` looks correct but a launch still tries to pull from a registry, inspect the exported image override variables (`CPP_BACKEND_IMAGE`, `FRONTEND_IMAGE`, etc.) and compare them against `podman images` / `podman image exists` results before changing code.
- If the launch fails with `manifest unknown`, treat it as a tag mismatch first: confirm the exact image tag exists with `podman manifest inspect <image:tag>` before touching compose, and remember that a shell variable like `TAG=dev` only matters if the compose template actually references it.
- For in-repo Python services, prefer mounting the repository root and launching with `python -m package.module` so imports resolve consistently inside containers.
- When a host-bound service answers on the expected port but returns the wrong API, verify the port owner before changing code; a port conflict can look like an application regression.
- When the build log shows `identifier is not a container` or a missing backend dependency after an unpack failure, treat it as fallout from the earlier image/volume failure and fix the first explicit error instead of chasing the cleanup noise.
- When pruning local artifacts, remove only transient build layers/images/cache unless the user explicitly approves data-directory removal.
- If Podman fails while unpacking images or building layers with `no space left on device`, check rootless storage pressure first; prune dangling images and builder cache before changing compose or code.
- If a heavy vcpkg/protobuf build stalls or fails repeatedly in a constrained rootless Podman builder, try lowering `VCPKG_MAX_CONCURRENCY` before changing source or dependency versions, then rerun the exact same compose command.
- If vcpkg is still building unwanted debug host packages, set `VCPKG_DEFAULT_HOST_TRIPLET` to the same overlay triplet and make the overlay triplet `release`-only with `set(VCPKG_BUILD_TYPE release)`. Verify that the install plan shrinks and the host-debug package set disappears before looking deeper.
- If a vcpkg manifest install fails on a specific port download, inspect the exact archive URL before changing application code. For pinned GitHub sources, `codeload.github.com` and a narrowly seeded downloads cache can be a reliable fallback when the normal archive path is flaky.

## Cleanup and data-boundary rules

- Remove only clearly transient build artifacts by default: build directories, compiler outputs, logs, coverage artifacts, and reproducible caches.
- Treat bind-mounted database directories and application state directories as protected unless the user explicitly approves deleting them.
- If a cleanup request touches live data directories, separate the transient cleanup from the destructive data removal and ask for explicit approval before the latter.
- After any approved data-directory deletion, verify the path is gone and report exactly what was removed.
- Use `references/cleanup-boundaries.md` as the compact policy note for protected paths, cleanup candidates, and the trade-repo example.

## Practical triage checklist

- What changed since the last known-good run?
- Did the consumer runtime reject the artifact because of a contract mismatch (shape, dtype, axis order), not just a parse/load error?
- If the model file loads but downstream metadata/shape discovery fails, separate "artifact is valid" from "loader still lacks enough dimensions to run"; prefer recovering dimensions from packaged config/metadata before treating the artifact as bad.
- For packaged ML artifacts, validate the runtime package, not just the source export: compare the packaged artifact, its config/metadata, and the consumer's expected tensor contract. A valid source ONNX can still fail after packaging if layout or dimensions drift.
- If a CI smoke test is supposed to validate the runtime package, make sure it uses the same production packaging helper that writes the config/metadata sidecars; a model-only export helper can create a false regression by omitting required files.
- When a tmux log shows training has reached 100% and the next failure is during model activation, treat that as a packaging/load-path issue, not a training-convergence issue.
- If the packaged model copies both `transformer.onnx` and `transformer_config.json`, check that the layout and feature dimensions match the loader's expectations before blaming the ONNX graph itself; a layout mismatch can surface as a low-level vector/shape error even when the file is valid.
- If training packages a model successfully but activation fails, remove or quarantine the invalid package directory so later reloads do not keep rediscovering broken state.
- What is the first explicit error in the log stream?
- Is the failure reproducible with the same command?
- Is the fix local to compose/config, build flags, or source code?
- What is the smallest verification step that proves the issue is gone?

## Common pitfalls

- Reading a partial CI snapshot as a final result.
- Debugging from the newest log line instead of the first real error.
- Assuming a local container build failure means the code is broken; often it is config, resource, or packaging.
- Cleaning up local runtime data when the request was only to remove build artifacts.
- Reporting success before the backend/slowest job finishes.

## References

- See `references/ci-playbook.md` for a concise playbook covering tmux log capture, CI run checks, and cleanup/verification patterns.
- See `references/github-actions-remote-build-proof.md` for the shortest checklist when the user only wants GitHub Actions as proof of build completion.
- See `references/db-auth-tmux-debugging.md` for a compact example of resolving a container DB auth mismatch discovered through tmux log capture.

- See references/podman-compose-build-fallbacks.md for a focused checklist on local-tag verification, upstream fetch fallbacks, and disabling nonessential build cache submission in container builds.
- See references/podman-local-image-aliasing.md for a concise note on Podman image aliasing, rendered compose verification, and avoiding accidental registry pulls from local dev stacks.
- See references/podman-ghcr-dev-tag-triage.md for the tag-mismatch pattern where `TAG=dev` was present but compose still resolved to `:main`, causing `manifest unknown` pulls.
- See references/podman-storage-exhaustion.md for a concise playbook on diagnosing `no space left on device` during Podman layer unpack/build and recovering without touching persistent data.
- See references/podman-vcpkg-download-fallbacks.md for vcpkg archive-download fallbacks, codeload usage, and exact-artifact cache seeding.
- See references/vcpkg-release-host-triplet.md for the host-triplet/release-only triplet pattern that removes debug host packages from the install plan.
- See references/rootless-podman-vcpkg-concurrency.md for the protobuf/vcpkg concurrency workaround on resource-limited rootless Podman builders.
- See references/tmux-capture-and-local-tags.md for the failure-window capture recipe, local-tag verification, and Podman storage-exhaustion triage.
- See `references/cleanup-boundaries.md` for the protected-path and live-data cleanup policy that keeps runtime state out of routine artifact removal.
- See `references/podman-postgres-compose-hardware-tuning.md` for the verified Postgres/Metabase compose tuning used on a 16 GiB Apple Silicon host running rootless Podman.
- See `references/risky-change-gates.md` for the practical budget, eval, and rollback gate used when a container/debug fix changes behavior.
- See `references/transformer-onnx-artifact-validation.md` for the trade-repo lesson on validating generated ML artifacts after containerized training, including a real packaged-transformer reload failure where the export was valid but the runtime package still failed activation until the layout/config contract was aligned and stale package dirs were removed.
- See `references/transformer-runtime-package-activation-failure.md` for the concise session note covering tmux failure-window capture, production-helper smoke-test wiring, test-target linkage, and merge-to-dev CI verification for the same incident.
- See `references/trade-db-transaction-and-model-fallback.md` for the trade-stack note on tmux anchoring at the last launch marker, per-query pqxx connections, and non-fatal ML model-load fallback responses.
