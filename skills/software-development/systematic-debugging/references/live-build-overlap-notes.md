# Live build / tmux capture notes

Session-derived debugging notes for long-running container builds captured from a tmux pane.

## Failure pattern
- The user asked for logs from a tmux pane since the last launch marker (`TAG=dev podman-compose up --no-build`).
- A second overlapping `podman-compose build` was still running in parallel.
- Cleanup output such as `identifier is not a container` was a side effect of mixed/stale process state, not the primary application bug.
- A prior `no space left on device` failure came from Podman image unpack/storage pressure, not source code.

## Practical rules
1. Anchor log capture to the last occurrence of the launch command or marker, not earlier boot noise.
2. Before interpreting build errors, check whether another build is still running and terminate duplicates.
3. If the current pane contains output from multiple attempts, separate the active run by its last launch marker before reading further.
4. If the first failure is storage-related under rootless Podman, free storage/prune stale layers first, then rerun the same build from a clean state.
5. Analyze the fresh run separately; do not mix it with historical output from a previous attempt.

## Useful verification commands
- `podman ps -a`
- `podman system df`
- `podman images`
- `podman-compose config`
