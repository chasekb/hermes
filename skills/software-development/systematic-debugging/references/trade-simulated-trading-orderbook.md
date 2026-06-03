# Trade simulated trading + order book debugging notes

Session-specific notes for the trade repo when the Simulated Trading tab or ML-enhanced order book flow seems inert.

## Common failure mode
- The UI can look like it is doing nothing when the start request hits the wrong backend route or the backend returns a structured error that the frontend swallows.
- In this session, the frontend/backend contract needed to be verified directly from the running app and the live API before assuming docs were current.
- The fix pattern is: compare the exact outbound request path and payload against the live backend route contract, then make failures visible in the UI.

## Live UI was the source of truth
Use the running browser to inspect the actual controls before editing code:
- `Trading Strategy`: `ml_enhanced_orderbook`, `orderbook`, `sma`, `ema`, `rsi`, `bollinger`, `macd`, `stochastic`, `fibonacci`, `dca`, `buyandhold`
- `Universe Type`: `all_products`, `all_usd`, `all_eur`, `all_usdt`, `all_btc`, `major`, `minor`, `crypto`, `custom`
- `Order Prioritization`: `signal_strength`, `win_probability`, `expected_return`, `none`
- `Configuration Preset` for order book: `custom`, `conservative`, `moderate`, `aggressive`, `very-aggressive`

## Evidence to capture
- tmux pane output from the last launch marker onward.
- Browser console/storage only after the network request path is confirmed.
- Backend logs for route 404s, validation errors, or structured `{status:"error"}` responses.
- `podman-compose config` to verify rendered image names and runtime wiring before changing app code.
- In the browser, inspect the live `<select>` options/value list before trusting docs or screenshots.

## Best starter config for generating order-book training data
Use a small, liquid symbol basket and the order book strategy first so the session generates enough signals/trades to train on:
- strategy: `orderbook`
- preset: `aggressive`
- symbols: use a small liquid basket or a liquid USD universe first
- order prioritization: `signal_strength`
- position size: about `1%` to `2%`
- max positions per session: `100`
- order book level: `2`
- trade history limit: `1000`
- bid/ask spread threshold: `0.5`
- volume imbalance threshold: `0.3`
- large trade threshold: `2000`
- data analysis mode: `all`
- recent data limit: `200`
- sampling ratio: `0.1`

## ML-enhanced order book workflow
- Start with baseline orderbook trading to accumulate `order_book_signals` and `individual_trades`.
- Once enough data exists, switch to `ml_enhanced_orderbook` with:
  - `ml_server_url: http://localhost:8002`
  - `confidence_threshold: 0.6`
  - `fallback_to_baseline: true`
- The ML-enhanced flow is only useful if the backend is already collecting enough persisted signal/trade pairs.
- For training, the useful minimum target in this repo is roughly 100 signals and 50 completed trades.

## What to check when Start Trading appears to do nothing
1. Verify the start endpoint path in the frontend client against the live backend route.
2. Verify the backend route exists and returns something other than 404.
3. Verify the simulated-trading status endpoint reflects an active session and trades, not just generated signals.
4. If signals are unbounded, confirm the backend dedupes/replaces old active signals instead of appending every tick.
5. Paginate signal tables by default; do not rely on client-side rendering of the entire history.
6. Make backend errors visible in the UI instead of treating them as success.
7. Use a small/liquid symbol basket so trades arrive quickly enough to prove the execution loop is alive.
8. Confirm the data pipeline is persisting signal/trade pairs before expecting ML retraining to improve results.

## Notes from this session
- The backend can still boot and train even if the transformer ONNX warning appears at startup; do not treat that warning as the only cause of a dead UI.
- A backend warning about transformer model loading does not by itself explain a silent Start Trading action.
- When the job is remote-build oriented, commit/push first and verify the build in GitHub Actions rather than relying only on local rebuilds.
- For the trade dashboard, local simulated trading can be forced into a deterministic client-side fallback when needed so the UI still exercises the trading loop.
