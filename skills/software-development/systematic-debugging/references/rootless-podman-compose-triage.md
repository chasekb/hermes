# Rootless Podman compose triage

Session-derived notes for debugging compose startup under rootless Podman.

## Capture the right log window

When the user asks for pane/log output "since" a launch command or marker, capture from the last occurrence of that marker forward. This avoids analyzing stale boot noise.

## Common failure classes

- Unsupported sysctls in compose can stop startup before the app code runs.
- A registry auth failure during image pull is often an image-access problem, not an application failure.
- `no space left on device` during image unpack usually means Podman storage is full, not that the build itself is broken.
- `TAG=dev` does not guarantee local tags are being used. Always inspect the rendered compose config and any exported image override environment variables.
- If `podman-compose up --no-build` still resolves to registry-like names, make the compose defaults explicit local dev tags (for example `trade-cpp-backend:dev` and `trade-frontend:dev`) so the no-build path uses images already present locally instead of trying to pull.

## Useful checks

```bash
podman-compose config
podman system df
podman images --format '{{.Repository}}:{{.Tag}} {{.ID}} {{.Size}}'
```

## Cleanup / recovery pattern

If storage is the blocker, prune stale image layers and builder cache before changing code:

```bash
podman image prune -f
podman builder prune -af
podman rmi -f <dangling-image-ids>
```

## Compose-specific reminder

Bind-mounted `./data/...` paths are host data. Do not remove them casually during cleanup.
