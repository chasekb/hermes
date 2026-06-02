# Podman compose remote-image triage

Session note for trade repo / GHCR-backed compose flows.

## What to check first
- Run `podman-compose config` before chasing runtime errors. It reveals whether compose is still resolving local tags or has switched to remote registry images.
- If `up --no-build` still behaves like a local-build path, inspect for remaining `build:` sections or environment overrides such as `CPP_BACKEND_IMAGE` / `FRONTEND_IMAGE`.
- Remote-image flows should use explicit registry refs in compose, and no `build:` blocks for the services you want to pull.
- Do not assume a tag like `:main` exists just because CI publishes images. If a pull says `manifest unknown`, verify the actual published tag with `podman manifest inspect` or `podman pull` before changing compose again.

## Practical sizing note
For pulling and running the trade stack’s remote images reliably on rootless Podman, disk pressure is usually the first limiter.
- If the VM disk was resized but image unpack still fails or `df` inside the VM barely changes, grow the guest partition/filesystem too (for example `growpart` followed by `xfs_growfs`) so the extra disk becomes usable by container storage.
- 8 CPUs is usually sufficient for this class of triage; memory increases may be constrained by the host, so prioritize storage first when unpack is the failure point.

## Why this matters
- `TAG=dev` does not guarantee local tags if compose is still pointing at registry refs.
- A clean `config` render is the best proof that compose will pull instead of build.
- When image pull/unpack fails with storage pressure, the fix is usually more usable VM disk or pruning stale layers, not application changes.
