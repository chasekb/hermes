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
