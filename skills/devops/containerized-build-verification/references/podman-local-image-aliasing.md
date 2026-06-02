# Podman local image aliasing and compose verification

When a compose stack is supposed to use local dev images, verify the rendered config before launching:

- Run `podman-compose config` and confirm the `image:` fields are the exact local tags you expect.
- Check the local image list with `podman images`.
- If `podman image exists <name>` succeeds for both `trade-frontend:dev` and `localhost/trade-frontend:dev`, treat that as one local image being addressable by multiple references, not as proof that compose is using the intended name.
- If `up --no-build` still tries to resolve a registry pull, inspect any exported image overrides such as `CPP_BACKEND_IMAGE` and `FRONTEND_IMAGE` and compare them against the rendered config.
- Prefer explicit local dev tags like `trade-cpp-backend:dev` and `trade-frontend:dev` when the goal is to avoid remote registry resolution during development.

Observed failure mode from the trade stack:

- `podman-compose up --no-build` tried to pull `localhost/trade-cpp-backend:dev` and `localhost/trade-frontend:dev` from `https://localhost/v2/`, which failed with connection refused.
- After changing the compose defaults to explicit local tags, `podman-compose config` resolved the intended image names.
