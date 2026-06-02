# GHCR dev-tag triage for `podman-compose up --no-build`

Session note: the compose stack failed because the rendered image tags did not exist in GHCR, not because the container runtime was trying to build locally.

Observed pattern:
- `TAG=dev podman-compose up --no-build`
- `podman-compose config` rendered `ghcr.io/chasekb/trade/cpp-backend:main` and `ghcr.io/chasekb/trade/frontend:main`
- `podman pull` reported `manifest unknown` for `:main`
- `podman manifest inspect` succeeded for `:dev`

Practical fix pattern:
1. Verify the rendered compose image refs with `podman-compose config`.
2. Verify the exact registry tag exists with `podman manifest inspect <image:tag>`.
3. If `TAG=dev` is only a shell env var and compose defaults still point to `:main`, update the compose defaults or pass `CPP_BACKEND_IMAGE` / `FRONTEND_IMAGE` explicitly.
4. Re-run the same `podman-compose up --no-build` command after the tag mismatch is fixed.

Key lesson:
- `TAG=...` alone does not guarantee the compose file is using that tag unless the compose template actually references it.