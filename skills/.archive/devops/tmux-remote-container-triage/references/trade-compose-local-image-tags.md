# Trade compose local image tags

Session note: while capturing tmux pane `0:8.0` during `TAG=dev podman-compose up --no-build`, the stack logged attempts to pull:

- `localhost/trade-cpp-backend:dev`
- `localhost/trade-frontend:dev`

That produced registry lookup failures and a downstream missing-container error for `trade_cpp-backend_1`.

The compose fix was to make the default image names local build tags and keep explicit build contexts so the stack can be built once and reused with `--no-build`:

- backend default image: `trade-cpp-backend:dev`
- frontend default image: `trade-frontend:dev`
- backend build context: repo root, `Dockerfile.cpp`
- frontend build context: `./frontend`, `Dockerfile`

Useful checks:

- `tmux list-panes -a` before capturing so the pane target is confirmed.
- `tmux capture-pane -t 0:8.0 -p -S -400` to get the live failure window.
- `podman-compose config` to inspect the effective image names before editing anything else.

Pitfall:

- A compose service can still try to pull an image even when a build section exists if the resolved image tag points at an unreachable registry namespace. Always verify the post-interpolation image name, not just the YAML defaults.
