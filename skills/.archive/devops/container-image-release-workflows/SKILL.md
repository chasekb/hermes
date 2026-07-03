---
name: container-image-release-workflows
description: "Align local compose defaults with container images published by CI/CD workflows, and verify the effective runtime image names before changing them."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [docker, compose, github-actions, ghcr, container-images, release-workflows]
---

# Container Image Release Workflows

Use this skill when a repository publishes container images in CI/CD and local compose files need to point at the same source of truth.

Typical signals:
- a GitHub Actions workflow builds and publishes images to GHCR or another registry
- `docker-compose.yml` / `podman-compose.yml` has both `image:` and `build:` sections
- `up --no-build` unexpectedly tries to pull a different image name than the CI workflow publishes
- you need the local defaults to match the remote build used in Actions

## Core workflow

1. Inspect the workflow first.
   - Find the build job, registry name, repository path, and final tags.
   - Do not assume local image names from old compose history.

2. Trace the repo history before editing compose.
   - Use `git log -- <compose file> <workflow file>` to find the last intentional shift between local and remote image defaults.
   - Prefer the most recent commit that explicitly changed the image source of truth.

3. Match compose defaults to the actual published image names.
   - If CI publishes `ghcr.io/org/repo/component:dev`, the compose default should use that exact string.
   - If local builds are the intended path, keep explicit `build:` blocks and local tags together.

4. Verify the effective config.
   - Run `docker compose config` or `podman-compose config` after the edit.
   - Confirm the resolved `image:` values are exactly what the workflow publishes or what local builds create.

5. Re-run the smallest relevant verification.
   - For image-name changes, config resolution is the key check.
   - For build-path changes, run a build only if it is reasonably bounded.

## Pitfalls

- A compose service can have `build:` and still pull by `image:` if the image name resolves to a registry name that is not present locally.
- `--no-build` does not mean "ignore `image:`"; it means "use the already-built image if available." If the name is wrong, compose still tries to pull it.
- Local rootless Podman often surfaces registry resolution issues earlier than Docker does. Treat that as a useful signal and confirm with `config`.
- When a repo uses remote CI as the release path, do not leave compose defaults pointing at `localhost/...` unless the team explicitly chose that convention.

## Verification checklist

- [ ] Workflow file inspected and tags confirmed
- [ ] Git history reviewed for prior intentional image-name shifts
- [ ] Compose defaults match the chosen release source of truth
- [ ] `compose config` resolves to the expected image names
- [ ] No unrelated compose refactors were introduced

## References

- `references/trade-gh-actions-compose.md` — concrete example from the trade repo: GH Actions publishes `ghcr.io/...` images, and compose defaults should follow that remote build layout.
