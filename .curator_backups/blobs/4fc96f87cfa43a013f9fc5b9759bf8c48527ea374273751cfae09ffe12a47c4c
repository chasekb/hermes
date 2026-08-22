# Tmux sentinel capture and DB storage migration notes

Session-derived playbook for containerized debugging:

## Tmux log capture
- When a service log is buried in a long-lived tmux pane, capture from the last clear sentinel/marker before the failure instead of replaying the whole pane.
- The marker should be a meaningful command boundary or repeated log phrase that reliably separates the current attempt from older noise.
- This keeps the failure window short enough to inspect line-by-line.

## Postgres storage migration in compose
- If switching Postgres from a named volume to a host bind mount, migrate the existing data into the host path before deleting the old volume.
- Restart the service after the copy and verify both of these:
  1. the container inspect output shows a bind mount at the expected host path
  2. the database still answers a simple query (for example `SELECT 1`)
- Only remove the old named volume after the bind mount works and the database is readable.

## Verification mindset
- Treat storage-layout changes as runtime changes, not just compose-file edits.
- Verify mount type and database health after restart; do not assume the container will automatically preserve data across storage backends.
