# tmux capture + local-tag verification for podman-compose

Use this when a long-lived tmux pane is logging a `podman-compose up --no-build` run and the output has already mixed old startup noise with the current failure.

## Capture the relevant failure window

- Find the last occurrence of the launch marker or sentinel string, then capture from there forward.
- In tmux, `capture-pane -p -J -S <start>` is safer than reading the whole pane when the session has restarted or been interrupted multiple times.
- Keep the slice small enough to read end-to-end so earlier boot messages do not mask the first real error.

## Verify rendered compose config before assuming local images

- Run `podman-compose config` with the same env you plan to use for `up --no-build`.
- Confirm the rendered `image:` values are local tags if that is the intended path (for example `localhost/<name>:dev`).
- If `up --no-build` tries to pull GHCR refs anyway, check for env overrides and the rendered config before editing code.

## Storage-exhaustion failure pattern

- If the first explicit error is `no space left on device` during image unpacking or layer addition, treat later dependency errors like “container not found” as fallout.
- Free rootless Podman image/build cache first, then rerun the same build or up command.
- Avoid changing application code until the storage issue is cleared and the same command reproduces cleanly.

## Useful verification sequence

1. Capture the failure window from the last launch marker.
2. Run `podman-compose config` and inspect the rendered image names.
3. Check `podman system df` / image inventory if unpacking or layer addition failed.
4. Prune only transient images/cache if storage is the blocker.
5. Retry the same `build`/`up --no-build` command and confirm the first real error changed or disappeared.
