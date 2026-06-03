# Frontend/Backend Endpoint Diagnostics

Use when a browser dashboard shows a 500 or a generic "Failed to load ..." error, but the backend may still be healthy.

## Pattern observed
- Next.js dev server at `http://localhost:3000` can proxy `/api/*` through `next.config.ts` rewrites.
- The real backend for this repo was listening on `http://localhost:8081`, not `:8000`.
- A stale fallback in frontend dev config caused the dashboard to hit the wrong port and surface a 500 on `GET /api/trades/stats`.

## Fast triage steps
1. Check the browser origin and request target.
   - In the browser, verify `window.location.origin`.
   - Use an absolute URL when probing from console: `fetch(window.location.origin + '/api/trades/stats')`.
2. Probe the backend directly.
   - `curl http://localhost:8081/api/trades/stats`
   - `curl http://localhost:8081/api/health`
3. Inspect the frontend proxy config.
   - `frontend/next.config.ts` rewrites `/api/:path*` to `BACKEND_URL` or `NEXT_PUBLIC_API_URL`.
   - Dev fallbacks in `frontend/lib/config.ts`, `frontend/hooks/useWebSocket.ts`, and `frontend/hooks/useTrading.ts` must match the live backend port.
4. Restart the frontend dev server after changing proxy/env defaults.

## Common fix
Align all dev fallbacks to the live backend port and restart the Next.js server. When the browser app is already open, hard refresh after the restart so it picks up the new proxy target.

## Verification
- `fetch(window.location.origin + '/api/trades/stats')` returns HTTP 200.
- The dashboard renders trading statistics without the 500 banner.
- No separate backend 404/500 appears for the stats endpoint.
