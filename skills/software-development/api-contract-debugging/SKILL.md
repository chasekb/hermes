---
name: api-contract-debugging
description: Debug and verify frontend/back-end API contract mismatches, endpoint availability, and silent no-op failures.
---

# API Contract Debugging

Use this skill when a UI action appears to do nothing, returns a generic error, or the backend logs show no activity even though the client says it sent a request.

## Core idea
Do not assume the app code is wrong first. First prove the running service actually exposes the route, shape, and mode the client is calling. A feature can be “implemented” in source but absent in the running image, behind a different route prefix, or only partially wired.

## Workflow
1. Reproduce the user-visible failure.
   - Capture the exact button/action, error text, and whether logs are quiet or noisy.
2. Probe the running backend directly.
   - Use HTTP requests against the live container/port.
   - Check both the expected endpoint and nearby variants that the client may have drifted to.
   - Verify status code, payload shape, and whether the route exists at all.
3. Inspect the frontend call path.
   - Find the actual client method, route, and request body.
   - Compare against docs and live backend behavior, not just source comments.
4. Distinguish capability gaps from transport failures.
   - 404/405 on the live image usually means the running service does not expose that API, even if source suggests it should.
   - If backend logs stay silent, the request may never have reached the service or may have been answered by a different layer.
5. Fix the narrowest contract mismatch first.
   - Align the route, payload, or response parsing.
   - If the backend image truly lacks the feature, add a safe fallback only when it preserves user value.
6. Rebuild and verify.
   - Run the frontend build or targeted tests.
   - Restart the stack if the image/runtime changed.
   - Re-run the same HTTP probe and confirm the UI now surfaces success or a visible failure.

## Common pitfalls
- The source tree and the running container are not always the same version.
- A client may call the wrong route prefix while still “handling” the response as if it succeeded.
- Generic catch blocks can hide a 404/500 and produce an “unknown error” with no useful context.
- A fallback that fabricates data can make the UI look healthy while the backend remains idle; only use it deliberately and document it.
- If a feature depends on real backend signals/trades/events, verify the backend routes exist before treating the UI as the source of truth.

## Verification checklist
- The live HTTP endpoint returns the expected status and shape.
- The backend logs show activity for the user action.
- The frontend shows a visible success or failure state, not a silent noop.
- The build passes after the contract fix.

## Supporting reference
- See `references/simulated-trading-backend-mismatch.md` for a concrete case study involving a simulated-trading tab, missing backend endpoints, and a frontend fallback pattern.