# Trade simulated-trading widget stall

Session pattern:
- Path: trade repo, localhost:3000 simulated trading tab
- User flow: universe symbol selection mode -> ml-enhanced order book strategy -> train model -> start trading
- Symptom: training completes, but simulated trading statistics and order book signals widgets stay empty

Observed failure shape:
- Frontend requests to `/api/simulated-trading/status` and `/api/orderbook/live-signals` started failing with `socket hang up` / `ECONNRESET`
- Backend logs showed `FATAL Transport endpoint is not connected (errno=107) sockets::shutdownWrite - Socket.cc:110`
- tmux capture anchored at the last `TAG=dev podman-compose up --no-build` marker was required to avoid stale boot noise

Triage takeaways:
1. Confirm the backend is still answering `/api/simulated-trading/status` before blaming the widgets.
2. Inspect the actual live-order-book request payload from the browser layer; universe mode can produce an oversized `symbols` list.
3. If the live-signals request is pathological, cap or paginate the symbol list server-side rather than letting the UI send an unbounded request.
4. If the worker loop can throw per tick, catch and log exceptions so one bad tick does not silently stop the stats/signals pipeline.
5. Make the UI fail loudly when the backend is unreachable instead of appearing idle.

Related fixes from the session:
- A server-side cap was added to trim live-order-book symbol filters to 100 symbols per request.
- The simulated trading worker loop was hardened to catch and log per-tick exceptions instead of dying silently.
