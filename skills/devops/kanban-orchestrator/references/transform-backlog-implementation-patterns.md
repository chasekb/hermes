# Transform backlog implementation patterns

Session-derived implementation notes for backlog items that turn pipeline metrics into code changes.

## Observed optimization patterns
- Cap worker fan-out to the actual workload size before calling `run_forked_tasks`; a global worker cap is often too blunt for symbol-sized batches.
- Replace per-symbol watermark lookups with a batched query that returns a map of `underlying_symbol -> latest_daily_timestamp`.
- Reuse the batched watermark map inside the child task closure instead of re-querying inside each worker.

## Verification pattern
- Run the available unit binaries directly when the full build toolchain is unavailable in the local environment.
- Use `git diff --check` to catch whitespace/patch issues after edits.
- Distinguish environment/setup gaps from code regressions; do not encode missing local tools as a durable workflow rule.

## When this applies
Use these steps when a transform backlog item is about reducing fetch/write overhead, improving hardware saturation, or trimming serialized work in the metrics/options pipeline.
