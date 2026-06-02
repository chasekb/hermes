# Trade repo: rootless Podman + vcpkg build pressure

Use this when a `podman-compose up --no-build` / `podman-compose build` session in the trade repo looks healthy at first but dies late in the C++ backend build or during image unpack.

Observed failure modes in this session:
- tmux pane logs contained older `podman-compose up --no-build` runs, interleaved with later runs; the relevant failure window started at the last launch marker, not the beginning of the pane.
- `podman-compose up --no-build` initially tried to pull GHCR images and later failed to unpack them with `no space left on device` while writing `/app/vcpkg_installed/.../libtorch_cpu.so`.
- `TAG=dev` was not enough to guarantee local dev tags; `podman-compose config` showed the effective image names were `localhost/trade-cpp-backend:dev` and `localhost/trade-frontend:dev`.
- The rootless Podman VM had accumulated enough dangling images / builder cache that `podman system df` showed substantial reclaimable space; pruning dangling images and builder cache helped.
- The C++ Docker build still hit late vcpkg pressure on protobuf/libtorch, so lowering `VCPKG_MAX_CONCURRENCY` to 1 and setting `VCPKG_BUILD_TYPE=release` reduced the amount of work and storage churn.

Useful triage sequence:
1. Capture the tmux pane from the last launch marker forward; ignore earlier boot noise.
2. Run `podman-compose config` and verify the rendered image names.
3. Check `podman system df` / `podman images` for storage pressure if unpack/build errors mention disk space.
4. If needed, prune dangling images and builder cache before changing application code.
5. For protobuf/vcpkg failures under rootless Podman, treat resource pressure as the first hypothesis: reduce concurrency, keep the build release-only, then rerun.
