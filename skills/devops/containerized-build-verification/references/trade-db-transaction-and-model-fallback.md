# Trade stack tmux capture + DB/model fallback note

Session summary:
- Repro path: `TAG=dev podman-compose up --no-build` in the trade repo, then simulate trading in the UI.
- When asked to capture a tmux pane "since" a launch marker, anchor the capture at the last occurrence of the launch command (for example `TAG=dev podman-compose up --no-build`) and read forward from there. This avoids stale boot noise and unrelated cleanup messages.
- The observed backend runtime failure was `Database query failed: Started new transaction while transaction was still active.` Root cause: `DatabaseManager` was reusing one `pqxx::connection` across concurrent requests.
- Durable fix pattern: keep the DB URL in the manager, but open a short-lived `pqxx::connection` per query instead of sharing one connection across concurrent backend requests.
- A separate ML-path issue surfaced as a transformer/model-load warning. If feature engineering is present but model sessions are unavailable, the request path can remain healthy by returning neutral fallback values plus explicit `models_ready=false` / `warning` metadata instead of hard-failing the endpoint.
- For CI proof after a push, verify the exact GitHub Actions run tied to the pushed `headSha`; do not reuse an earlier green run on the same branch.
