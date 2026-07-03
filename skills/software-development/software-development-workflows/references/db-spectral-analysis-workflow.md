# DB spectral analysis workflow notes

Use this when implementing Fourier / spectral analysis against live Postgres-backed time-series tables.

## Practical pattern
1. Confirm the canonical source tables and the derived tables that actually exist in the live schema.
2. Normalize by series type before FFT:
   - daily bars: resample to business days and use log returns when prices are positive
   - intraday bars: choose a contiguous session block before resampling to minutes
   - sparse option quotes: aggregate to a daily underlying-symbol series first; do not FFT raw contract rows
3. Treat derived tables as lineage-backed outputs, not independent sources, until provenance is checked.
4. Add a negative-control test that demonstrates why the naive/raw series is misleading when sampling is irregular or sparse.
5. Generate a durable report artifact (markdown + JSON) so the analysis can be reviewed without rerunning the database queries.

## Testing and verification
- Use small, deterministic unit tests for the regularization helpers and the frequency-peaks helper.
- When importing the analysis module in pytest, insert the module into sys.modules before exec_module so dataclass-based modules initialize cleanly.
- If the full report takes a long time, run it in the background and verify the output files after completion instead of waiting in a foreground loop.

## Common pitfalls
- Computing FFT on raw irregular timestamps.
- Treating sparse option contracts as directly comparable to daily bars.
- Computing gap metrics after resampling, which hides the source irregularity.
- Letting a long-running report task block the whole session when the test suite already proves the helpers.
