# Transformer and order-book readiness in simulated trading

Use this reference when a simulated multi-symbol order-book run reports transformer shape warnings or missing market-data coverage.

## Root-cause pattern

A shared `FeatureEngineer` rolling history is unsafe when a worker processes multiple symbols in one tick. The first symbols can produce sequences of `1..lookback-1` rows, while later symbols receive mixed-symbol history. The same contamination can affect rolling time-series features, not only the transformer input window.

## Durable implementation pattern

- Key rolling feature history and transformer sequence buffers by symbol (or another explicit stream identity).
- Pass the same key through preprocessing and sequence retrieval in every caller: simulated worker, live worker, and prediction/API paths.
- Keep the model contract explicit: validate both sequence length and every row's feature width before invoking ONNX.
- During cold start, mark the symbol as `warming_up`/`insufficient_history`; do not call the model with padding unless padding is an intentional, validated model contract.
- Do not classify warm-up, rejected input, or fallback inference as a valid ML signal or trade. Keep it separate from HOLD, executable intents, and profitability metrics.
- Add a regression test that interleaves two symbols and verifies each stream's sequence length/state independently.

## Market-data failure contract

For live-data or live-parity simulated modes, a failed quote must not silently disappear from the selected universe or become synthetic data. Use bounded retries, classify the final error (`network`, `tls`, `dns`, `timeout`, `cancellation_or_shutdown`, or `exchange_response`), and expose per-symbol status, retry count, last-success timestamp, and error detail in diagnostics. Exclude failed/unavailable symbols from signal and execution counts while preserving reconciliation to the selected universe.

## CI proof discipline

When local container builds are prohibited, make only non-build repository checks locally, commit and push the scoped source/test changes, then select the GitHub Actions **push** run by exact `headSha`. A same-SHA pull-request run is not proof of the push build. Keep backlog items open until the exact push run is terminal with `status=completed`, `conclusion=success`, and all required architecture jobs green.
