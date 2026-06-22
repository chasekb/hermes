# Constituent-vs-Proxy Universe Checks

Use this when a backlog item or Kanban task asks for an index universe, stock universe, or market symbols list.

## Rule

Require the actual constituent symbols, not the ETF or wrapper ticker that tracks the basket.

Examples:
- Good: Russell 3000 constituent tickers from a constituent CSV / holdings export
- Good: a live holdings download for IWV, filtered to equity rows, when that is the best public machine-readable route to current Russell 3000 constituents
- Bad: IWV / VTI / SPY / other ETF wrappers used as a proxy for the universe

## Acceptance checks

- The source produces >3000 constituent tickers for Russell 3000-style requests.
- Known large-cap constituents are present in the result set.
- Wrapper ETFs are absent unless the request explicitly asks for ETFs.
- The backlog item or task text names the canonical source, not just the thematic universe.

## Recommendation-writing note

When drafting a backlog recommendation, include both:
- execution criteria: what must be built / wired / parsed / tested
- closeout criteria: what evidence proves the right universe was used and the proxy was not

This prevents a superficially correct implementation that returns the fund symbol instead of the underlying stock constituents.