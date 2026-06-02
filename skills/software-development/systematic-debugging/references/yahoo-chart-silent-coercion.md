# Yahoo chart request coercion notes

Session-specific debugging note for time-series pipelines that read Yahoo Finance chart data.

## Observed behavior

- `range=max&interval=1m` does not reliably return true 1-minute bars.
- Yahoo may silently coerce unsupported combinations to coarser historical data instead of failing.
- If `main_1d` and `main_1m` look identical, inspect the outbound request first; the root cause may be request normalization, not storage duplication.

## Practical fix pattern

- Normalize minute requests to a valid intraday window before building the URL.
- Use a short supported range for 1m data (for example `5d/1m`) rather than `max/1m`.
- Keep daily requests on their own valid chart shape (for example `max/1d`).
- When promoting overlapping minute bars into a final table, prefer interval-aware upsert semantics instead of `DO NOTHING`.

## Debug checklist

1. Log or inspect the exact outbound Yahoo chart URL.
2. Confirm the returned granularity matches the requested interval.
3. Compare row counts and timestamps between the source interval table and the promoted table.
4. If the API response is valid but the final table is stale, inspect conflict handling / promotion SQL.
