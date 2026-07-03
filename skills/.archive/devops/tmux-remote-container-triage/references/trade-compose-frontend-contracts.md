# Trade repo: tmux + compose frontend/backend contract notes

Session note for diagnosing live pane failures in the trade repo.

## What the live stack expects
- `docker-compose.yml` runs the backend from an image (`CPP_BACKEND_IMAGE`) and does not bind-mount the source tree into the container.
- Frontend env points at `http://cpp-backend:8080`.
- The frontend API client calls these backend routes directly:
  - `GET /api/health`
  - `GET /api/products`
  - `POST /api/log`
  - `GET /api/ml/config`
  - `POST /api/ml/config`

## Shape expectations
- `/api/products` must return `{ categories: Record<string, string[]> }`.
- ML config form defaults expected by the UI:
  - `continuous_training_enabled: false`
  - `training_interval: 3600`
  - `new_data_threshold: 100`
  - `batch_training_enabled: true`
  - `batch_size: 1000`

## Triage lesson
If the tmux pane shows frontend-side `ECONNRESET` / `socket hang up` while proxying to the backend, do not assume it is a network problem. First check whether the backend image actually exposes the route the frontend is calling. Missing legacy compatibility endpoints can manifest as transport errors in the pane.

## Verification pattern
1. Capture the pane from the live failure boundary.
2. Confirm whether the stack is image-backed or bind-mounted.
3. Smoke-test the exact API route from the frontend error log.
4. Rebuild/restart the image-backed service if the code change is not mounted live.
5. Re-capture the same pane and verify the noisy calls stop.
