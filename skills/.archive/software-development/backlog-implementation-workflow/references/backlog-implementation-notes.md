# Backlog implementation notes

Reusable lessons from implementing backlog items in the trade project.

- Start from the authoritative backlog/review document and preserve its item order.
- Split work by layer: metrics/cohort logic, sizing policy, and API/cache wiring should each get their own code change and verification.
- Execution-regime cohorts were most useful when bucketed by spread, order-book imbalance, liquidity tier, volatility, and session/time-of-day.
- If a sizing policy depends on recent results, pass live metrics plus cohort metrics through the shared metrics object and persist it so downstream consumers can use it.
- Add focused tests for the new behavior and then a broader build pass; do not mark the backlog item complete until you have a real successful verification result.
- For long-running builds, background the process and wait for completion instead of stopping at early compile output.
