# Simulated trading backend mismatch case study

Context:
- The simulated-trading tab showed an “unknown error” when Start Trading was pressed.
- The backend logs stayed quiet, which suggested the request was not reaching a matching server route.

What was probed:
- Direct HTTP calls were made against the running backend image for:
  - `/api/trading/simulated/start`
  - `/api/simulated-trading/start`
  - `/api/simulated-trading/status`
  - `/api/orderbook/live-signals`
- These probes returned 404 on the running container, confirming the feature was missing from the live image surface even though the frontend expected it.

Root cause pattern:
- The client and backend contract drifted.
- The UI had a route assumption that did not exist in the deployed image.
- Generic error handling turned the mismatch into an unhelpful “unknown error”.

Fix pattern:
- Add explicit route/payload verification against the live container.
- Prefer a visible failure state over silence.
- If a fallback is introduced, ensure it is clearly scoped and does not masquerade as a real backend session.
- Rebuild the frontend and re-run the same HTTP probe after the fix.

Practical lesson:
- When the UI depends on backend-generated signals/trades, first verify the backend exposes the endpoint in the running image before debugging the UI logic.