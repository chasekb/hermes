# Kanban gap-analysis reference

## Minimal card bodies

Storage audit: verify the exact live endpoint and collection/database; capture schema/config, total and distinct counts, identifier/date ranges, payload samples, query limitations, timestamp, and read-only evidence.

Source audit: enumerate canonical URLs exactly as constructed; map query parameters, sets, date windows, pagination/resumption, retries, rate limits, fields, and identifier/date semantics to workflows; avoid unbounded harvests.

Reconciliation: consume both handoffs; define join and normalization rules; calculate missing/extra/duplicate/ambiguous buckets; distinguish source/query/parser/persistence/measurement causes; include a negative control and reproducible evidence.

Specification: rank gaps by impact and confidence; name exact files/symbols/tests; define fixtures, rollback, and live-data safety; turn unresolved decisions into blockers.

Implementation/review: implement only approved scope; run targeted tests/build/smoke checks; verify residual gaps and report exact evidence.

## Failure/retry pattern

A compound CLI command can commit earlier task creates before a later invalid parent causes failure. Always re-list and show the board after any failed create sequence. Use only IDs confirmed by readback and retry the missing child with an idempotency key. Never infer task persistence from a copied or mistyped ID.
