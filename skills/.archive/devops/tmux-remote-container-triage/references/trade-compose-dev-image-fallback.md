# Trade compose dev image fallback

Session note: when the trade stack was started from tmux pane `0:8.0` with `TAG=dev podman-compose up --no-build`, compose attempted to pull default image names that resolved to `localhost/...` and failed before the app could start.

Observed log shape:
- `Trying to pull ...`
- `pinging container registry localhost: Get "https://localhost/v2/": dial tcp [::1]:443: connect: connection refused`
- `cpp-backend` then reported no matching container because the local image tag was never built/loaded

Fix pattern:
1. Use local dev image tags in compose defaults, e.g. `trade-cpp-backend:dev` and `trade-frontend:dev`.
2. Keep explicit `build:` contexts on the services so `podman-compose build` materializes those tags locally.
3. Re-run `podman-compose config` to confirm the resolved image names are local tags, not registry-prefixed names.
4. Build the stack once, then start with `up --no-build`.

Verification cues:
- `podman-compose config` shows `image: trade-cpp-backend:dev` and `image: trade-frontend:dev`.
- `podman images` shows the expected local tags after the build.
- The tmux pane no longer shows `localhost/v2/` pull failures on startup.
