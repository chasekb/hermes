# DB and artifact fallback patterns

Reusable patterns surfaced while debugging service startup and model packaging issues.

## Schema-optional queries

If a service may start before all tables exist, check the table first and short-circuit cleanly instead of letting downstream queries emit noisy errors.

PostgreSQL example:

```sql
SELECT to_regclass('public.individual_trades') AS relname;
```

If it is NULL, return an empty/default response or perform one-time initialization first.

## Ensure tables before consumers run

When a background collector depends on a table that other parts of the app also query, create the table/indexes in the collector's setup path before any reads/writes.

## Writable artifact destinations

When copying trained artifacts into a package directory:

1. Probe the actual destination path for writability.
2. If it is not writable, fall back to a temp directory that is known to be writable.
3. Create the package directory only after choosing the final path.
4. Copy to a temp file first, then promote atomically if possible.

## tmux capture for long-running processes

When debugging a live pane, capture output from a marker onward instead of reading the whole history. That isolates the exact run that introduced the failure and reduces noise.

Example:

```bash
tmux capture-pane -p -t 0:10.0 -S -5000
```

Then search backward/forward for the last known-good command or marker string.

If the capture is too sparse to explain the failure, widen the window and confirm you are looking at the correct pane/process before drawing conclusions.

## Container runtime storage vs host disk

A build that fails with `no space left on device` inside Podman may be hitting Podman machine/image storage even when the host filesystem still has free space.

Check both views:

```bash
podman system df
du -sh ~/.local/share/containers
```

If the host has space but Podman does not, prune builder/cache layers or remove stale machine storage before assuming the code/build is at fault.

## Rootless Podman compose startup triage

When `podman-compose up --no-build` fails in a rootless environment, separate runtime compatibility issues from registry access issues:

- Unsupported sysctls in compose (for example `vm.overcommit_memory`) can fail the container before the app starts; remove them for rootless Podman.
- A `403 Forbidden` while fetching a GHCR bearer token usually means the image pull is blocked by auth/registry policy, not that the image tag is invalid.
- If pulls are blocked, switch to the local build fallback (`TAG=dev podman-compose build`) and then retry the same `up --no-build` command using locally available images.
- Compose paths like `./data/databases/postgres` and `./data/cache/...` are often host bind mounts, not managed Docker volumes; deleting them erases local persisted state.

## Schema-guarded startup DDL

When startup DDL depends on a table that may be created lazily, preflight the table with `to_regclass()` (or equivalent) and only install dependent triggers/functions after the table exists.

This avoids noisy startup failures where the real issue is missing initialization, not a broken query.

## Writable artifact copy fallback

For packaging paths that may reject temp-file promotion, keep a fallback that copies directly into a writable destination, then normalize permissions and verify the final artifact size.
