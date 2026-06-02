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

- Treat a workflow as incomplete until every required job is done.
- Do not call a build successful because one or two jobs passed.
- Use the workflow/run view as the source of truth for status and conclusion.
- If a watch command exits with a transport/annotation/API problem, re-check the run directly before inferring failure.
- Distinguish:
  - job success
  - workflow in progress
  - workflow success
  - workflow failure

## Local container-debugging rules

- Separate environment wiring problems from application bugs.
- When a compose stack starts partially, inspect the earliest failing service first.
- If the first explicit error is an auth/config failure (for example Postgres password mismatch), compare the app's env defaults to the live container's env before changing code.
- If DB auth is failing, verify the target database exists inside the container with `psql` so you know whether the issue is credentials or provisioning.
- For background builds, stop the process cleanly when the user asks; do not keep iterating in the background.
- When a compose stack is intended to use local images with `up --no-build`, make the image names explicit local tags (for example `trade-cpp-backend:dev` / `trade-frontend:dev`) and verify the rendered config with `podman-compose config` before launching. Otherwise Compose may try to pull registry tags again and fail during unpacking or dependency resolution.
- If `podman-compose config` looks correct but a launch still tries to pull from a registry, inspect the exported image override variables (`CPP_BACKEND_IMAGE`, `FRONTEND_IMAGE`, etc.) and compare them against `podman images` / `podman image exists` results before changing code.
- If the launch fails with `manifest unknown`, treat it as a tag mismatch first: confirm the exact image tag exists with `podman manifest inspect <image:tag>` before touching compose, and remember that a shell variable like `TAG=dev` only matters if the compose template actually references it.
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

- See references/ci-playbook.md for a concise playbook covering tmux log capture, CI run checks, and cleanup/verification patterns.
- See references/db-auth-tmux-debugging.md for a compact example of resolving a container DB auth mismatch discovered through tmux log capture.
- See references/tmux-sentinel-and-db-storage-migration.md for a compact playbook on slicing tmux logs from the last sentinel and safely migrating Postgres from a named volume to a bind mount.
- See references/podman-compose-build-fallbacks.md for a focused checklist on local-tag verification, upstream fetch fallbacks, and disabling nonessential build cache submission in container builds.
- See references/podman-local-image-aliasing.md for a concise note on Podman image aliasing, rendered compose verification, and avoiding accidental registry pulls from local dev stacks.
- See references/podman-ghcr-dev-tag-triage.md for the tag-mismatch pattern where `TAG=dev` was present but compose still resolved to `:main`, causing `manifest unknown` pulls.
- See references/podman-storage-exhaustion.md for a concise playbook on diagnosing `no space left on device` during Podman layer unpack/build and recovering without touching persistent data.
- See references/podman-vcpkg-download-fallbacks.md for vcpkg archive-download fallbacks, codeload usage, and exact-artifact cache seeding.
- See references/vcpkg-release-host-triplet.md for the host-triplet/release-only triplet pattern that removes debug host packages from the install plan.
- See references/rootless-podman-vcpkg-concurrency.md for the protobuf/vcpkg concurrency workaround on resource-limited rootless Podman builders.
- See references/tmux-capture-and-local-tags.md for the failure-window capture recipe, local-tag verification, and Podman storage-exhaustion triage.
- See references/cleanup-boundaries.md for the protected-path and live-data cleanup policy that keeps runtime state out of routine artifact removal.
