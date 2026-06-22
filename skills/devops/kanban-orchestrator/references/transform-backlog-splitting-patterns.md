# Transform backlog splitting patterns

Session-derived guidance for the transform repo backlog.

## When to split into separate recommendations
- Split runtime/architecture changes from measurement or evaluation work.
- Treat process-model changes as implementation items.
- Treat caching questions as analysis/evaluation items unless the user explicitly asks for implementation.
- Keep each recommendation to one durable outcome so execution and closeout criteria stay testable.

## Example split used in this session
- CLI orchestration: one recommendation for adding a single command that runs all four transform modes.
- Parallelism model: one recommendation for replacing thread-based worker execution with process-based execution.
- PostgreSQL write pressure: one recommendation for evaluating whether extra caching or buffering is warranted.

## Scope and criteria reminders
- Scope each item to the transform repo path.
- Use execution criteria for code/path discovery, implementation steps, tests, and benchmarks.
- Use closeout criteria for reproducible evidence, doc updates, and preservation of legacy behavior.
- Keep architecture changes separate from validation-only investigations whenever the work can be independently closed.
