# Podman/compose build fetch fallbacks

Use this note when a local container build or compose startup stalls or fails while fetching third-party build inputs.

## Failure pattern

- The failing process is already running in tmux or a background job.
- The real error is often earlier than the visible stall; capture only the relevant window from the last known-good sentinel or launch command.
- `podman-compose up --no-build` can still try to pull registry images if the rendered config still references remote tags.
- Some containerized package-manager builds spend time on binary cache submission even after the actual package build is progressing.

## Triage sequence

1. Capture the failure window from the last clear marker, not the whole pane.
2. Verify the rendered compose config before relaunching.
   - Make image names explicit local tags when the workflow is meant to use local images.
   - Re-check with `podman-compose config` so you know what `up --no-build` will actually reference.
3. If the build stalls on an external fetch, swap to a reachable mirror or archive source for the build input.
4. If cache upload/submission is only slowing the build and not needed for the local run, disable it in the container build environment.
5. Re-run the same startup command so the fix is verified at the same layer that failed.

## Practical checks

- Confirm the compose file resolves to local tags before `up --no-build`.
- Confirm the new build input URL is reachable from the container build environment.
- Confirm the build progresses past the earlier fetch point and reaches later package compilation or runtime startup.
- Keep the verification command identical to the failing command whenever possible.
