# Trade Podman Compose Runtime Debugging

Use this note when debugging the trade repo under rootless Podman and tmux.

## Failure-window capture
- If the user says "since <marker>" or names a launch command, capture the tmux pane starting at the last occurrence of that marker/command.
- Keep the window tight: the current failure may be preceded by stale boot noise or an older attempt.
- Prefer the live pane over restarting the stack when a run is already in progress.

## Remote-image compose triage
1. Run `podman-compose config` and inspect the rendered image refs.
2. Verify that compose is not falling back to `build:` or `localhost/...` tags.
3. If GHCR returns `manifest unknown`, confirm the tag that actually exists before editing app code.
4. If unpacking fails with `no space left on device`, check `podman system df`, image size, and the Podman VM disk/guest filesystem.
5. If the VM disk was resized but free space did not change, grow the guest partition/filesystem too (for example `growpart` + `xfs_growfs`).

## Runtime workflow failures after startup
- Treat container startup health and application workflow health as separate checks.
- If the app starts but a training or request path fails, rerun the exact request and read the backend logs for the new failure window.
- Missing tables/views are root-cause candidates for DB-backed workflow failures; check whether the relation exists before changing query code.
- If artifact copy/write fails with permissions, verify whether the target is a bind mount versus a named volume.
- For persistent artifact paths, prefer a writable named volume when host ownership or SELinux keeps interfering.

## Good verification sequence
- `podman-compose config`
- `podman manifest inspect <image:tag>` for the exact remote ref
- `podman ps` and service logs after startup
- Re-trigger the failing API/job and inspect the newest log window
