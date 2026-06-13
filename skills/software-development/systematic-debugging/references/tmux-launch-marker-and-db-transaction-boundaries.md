# tmux launch-marker capture and pqxx transaction boundaries

Session-derived debugging note for long-lived tmux output and PostgreSQL access patterns.

## tmux capture rule
- When the user says to inspect output "since" a launch command, anchor the capture at the last occurrence of that exact launch marker (for example `TAG=dev podman-compose up --no-build`).
- Read forward from that marker only.
- Ignore earlier boot noise and overlapping stale runs.
- If the service is already running in tmux, prefer the live failure window over restarting it.

## Error signature observed
- `Database query failed: Started new transaction while transaction was still active.`

## Root-cause pattern
- Reusing one long-lived `pqxx::connection` across queries can make overlapping/recursive query paths trip over an active transaction on the same connection.
- The safer pattern is to store the DSN/URL and open a short-lived connection per query, or otherwise guarantee strictly non-overlapping transaction usage.

## Fix shape
- Preserve the connection string/URL on the manager.
- Create a fresh `pqxx::connection` for each query boundary.
- Keep the transaction scope local to the query call so concurrent callers cannot share transaction state accidentally.

## Verification
- Re-run the captured tmux flow from the same launch marker and confirm the transaction-active error no longer appears.
- If build verification is available, prefer a remote CI run as final proof when local rebuilds are blocked.
