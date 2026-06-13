# Order book client-cap triage

Session note: the simulated trading tab on the trade dashboard used the ML-enhanced order book strategy with a full "all used pairs" universe. Pressing "Train new model" and then "Start trading" left the simulated trading statistics and order book widgets blank.

Root cause pattern:
- The frontend built a very large `symbols` query for `/api/orderbook/live-signals`.
- The proxy/backend began returning `socket hang up` / transport shutdown errors.
- The backend also logged a protective trim from 396 to 100 symbols.

Fix pattern:
- Cap the client-side order book symbol filter to the same backend limit before building the query URL.
- Apply the cap in both the API client helper and the hook that forms the cache key, so the request URL and query cache stay aligned.
- Emit a visible warning when trimming so oversized universes fail loudly instead of appearing to do nothing.

Verification:
- Rebuild the frontend after the cap is added.
- Confirm the order-book request URL is now bounded and the dashboard widgets populate again.
