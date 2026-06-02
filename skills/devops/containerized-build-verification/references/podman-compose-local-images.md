# Podman Compose local-image workflow

## What this covered
A local `TAG=dev podman-compose up --no-build` run kept trying to pull remote GHCR images instead of reusing local builds. The compose file was updated to default to local tags:

- `localhost/trade-cpp-backend:dev`
- `localhost/trade-frontend:dev`

The README was updated so the default dev flow is:

```bash
podman-compose build
podman-compose up --no-build
```

If GHCR images are wanted explicitly, override the image names:

```bash
CPP_BACKEND_IMAGE=ghcr.io/chasekb/trade/cpp-backend:main \
FRONTEND_IMAGE=ghcr.io/chasekb/trade/frontend:main \
podman-compose pull

CPP_BACKEND_IMAGE=ghcr.io/chasekb/trade/cpp-backend:main \
FRONTEND_IMAGE=ghcr.io/chasekb/trade/frontend:main \
podman-compose up --no-build
```

## Verification step that mattered
Run `podman-compose config` and confirm the rendered `image:` fields match the intended tags before launching.

## Diagnostic pattern
When the stack fails with dependency errors like a missing `cpp-backend` container after an image pull failure, check the first image pull/unpack error in the log stream. In this case, the upstream issue was an image unpack failure during GHCR pull, and the durable fix was to stop relying on implicit remote image tags for the dev loop.
