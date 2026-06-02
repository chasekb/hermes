# DB auth + tmux capture notes

Session takeaway:
- In a running compose stack, capture the tmux pane from the last clear marker (e.g. the last `podman-compose up`) so older noise does not obscure the first new failure.
- A Postgres error like `FATAL: password authentication failed for user "postgres"` can be the primary cause even when later logs only show `Database not connected` or `Cannot execute query: not connected`.

Practical checks that resolved the issue:
1. Compare the app's configured DB env vars/defaults against the live container's environment.
2. Inspect the live Postgres container directly.
3. Verify the target database actually exists inside the container with `psql`.
4. Restart the compose stack after aligning the environment.
5. Confirm the application log eventually shows a successful connection line before declaring victory.

Pattern to remember:
- Downstream 'not connected' errors are often symptoms of an earlier auth/config mismatch, not separate bugs.
- If the runtime recovers after an env fix, prefer fixing configuration over changing database topology or application code.
