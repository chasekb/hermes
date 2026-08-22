# Podman storage exhaustion during build/unpack

Use this note when a local Podman or podman-compose build fails with `no space left on device`, especially while unpacking image layers or writing build cache.

## Symptom pattern

- The visible error may appear in a later build step, but the root cause is often storage exhaustion in rootless Podman storage.
- Follow-on errors can include missing containers, failed unpacking, or retries that fail immediately with the same storage error.

## Triage sequence

1. Confirm the failure is storage-related.
   - Look for `no space left on device` in the build or compose log.
   - If the error happened during image unpacking, assume Podman storage before changing compose or application code.
2. Free only transient Podman artifacts.
   - Prune dangling images and unused builder cache first.
   - Keep persistent data volumes and bind-mounted data directories intact unless the user explicitly approves removing them.
3. Retry the same build/start command.
   - Re-run the identical command that failed so you verify the fix at the same layer.
4. If the build still fails, inspect whether the workflow is pulling large remote images or writing excessive cache, and adjust that layer next.

## Practical cleanup boundaries

- Safe defaults: dangling images, unused build cache, intermediate layers.
- Do not delete database data directories or other persistent state by default.
- If a compose workflow is supposed to use local tags, confirm the rendered config before retrying so you do not re-trigger remote pulls.
