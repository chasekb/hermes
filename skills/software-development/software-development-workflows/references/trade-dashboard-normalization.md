# Trade dashboard normalization pattern

This reference captures a useful pattern from the trade project backlog work.

## When it applies
Use when several React dashboard panels share a trading config shape, and one or more components are failing TypeScript or lint checks due to broad `any` usage, render-time fallbacks, or effect-driven state sync.

## Pattern that worked
- Define narrow local types for external API responses and row data, e.g. `CoinbaseProduct`, `TradeLike`, `PositionLike`.
- Keep the shared config object typed, but add explicit optional keys for the actual fields consumed by the form/panel.
- Prefer `React.Dispatch<React.SetStateAction<T>>` for config setters when sibling components may need the same state updater semantics.
- Use small coercion helpers for render-time values:
  - `getConfigValue(value, fallback)` for string/number input props
  - `getConfigBoolean(value, fallback)` for checkbox props
- Convert dynamic values at the boundary:
  - `Number(value)` before numeric formatting or comparisons
  - `trade.timestamp ? new Date(trade.timestamp).toLocaleString() : '-'`
- Avoid impure render fallbacks such as `Date.now()`.
- Avoid `setState` directly inside `useEffect` when the same result can be derived from props or triggered by a user event.
- If `Object.values()` is iterating a record of unknown shape, cast it to `Record<string, T>` first and then filter with a type predicate.

## Verification sequence
1. Run targeted tests for the shared utility or stats helper.
2. Run `npm run build` for the frontend.
3. Run lint and keep any remaining findings limited to non-blocking warnings where possible.

## Signs the pattern is needed
- TS errors in multiple sibling dashboard panels after a shared prop/type change.
- React lint errors about `Date.now()` in render or `setState` inside `useEffect`.
- A build succeeds only after the config boundary is narrowed rather than widened.
