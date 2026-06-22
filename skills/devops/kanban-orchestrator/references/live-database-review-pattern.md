# Live database review pattern for backlog intake

Use this when a backlog recommendation depends on the live state of a database rather than a static doc or empty shell.

## Verification order
1. Identify the exact container and database name the user means.
2. Confirm the target database is the one in scope; do not assume the default `postgres` database.
3. Enumerate non-system schemas and tables.
4. Pull row counts, distinct symbol counts, and min/max timestamps for the key tables.
5. Record whether the source is truly empty, partially populated, or fully populated.
6. Feed those facts back into the backlog item so execution criteria match the actual source shape.

## Practical notes
- For the db-postgres service in this workspace, `unordered_map` is the populated database to inspect for symbol-review work.
- The `priority_queue` schema carries the main market-data, metrics, options, and derived-signal tables.
- Use the live counts and freshness windows in the backlog recommendation; do not describe the source abstractly when the real tables are available.

## Good evidence to capture
- `current_database()` and the current schema/user.
- Table inventory by schema.
- Row counts, distinct symbol counts, and min/max timestamps.
- Any empty-source or stale-source conditions that should become explicit fallback behavior.
