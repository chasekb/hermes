# Transform pipeline metrics and hardware-utilization backlog notes

Session-derived guidance for transform backlog items about pipeline metrics, concurrency, and hardware saturation.

## Scope
Use this pattern when the user asks for a backlog recommendation that:
- analyzes pipeline run metrics
- identifies compute/fetch/write bottlenecks
- recommends code changes that better exploit available CPU or I/O hardware
- needs multi-agent analysis before implementation

## Canonical evidence sources
- Live backlog store: `~/.codex/MCP/backlog/backlog.json`
- Transform backlog wrapper: `./scripts/backlog`
- Metrics table: `priority_queue.pipeline_run_metrics`
- End-of-run summary: `print_pipeline_optimization_opportunities` in `src/cpp/Main.cpp`
- Ranking and summary helpers: `src/cpp/PipelineMetrics.cpp`
- Metric shape: `src/cpp/include/Types.hpp`

## Recommended review lanes
Use a small fan-out before writing the backlog item:
1. Codex lane for code-path inspection and optimization opportunities.
2. OpenCode lane for concurrency / worker-fan-out review.
3. OpenCode lane for fetch/write-path and batching review.
4. Synthesize the results into one backlog recommendation with explicit execution and closeout criteria.

Keep the lanes independent unless one lane truly depends on another lane's findings.

## Recommendation shape
Include all of these in the backlog body:
- exact source table or metric stream
- how metrics are grouped or ranked (`stage_label`, `source_table`, run id)
- what hardware resource is underused today
- the smallest code-level change that should improve saturation
- a failing test, benchmark, or fixture that proves the work is needed
- before/after evidence that will prove the optimization worked

## Checklist wording that worked well
Execution checklist:
- collect representative run metrics
- classify bottlenecks by stage and source table
- compare throughput against CPU count and worker limit
- confirm whether the bottleneck is compute, fetch, or write bound
- add a failing test or benchmark harness before changing behavior

Closeout criteria:
- code-referenced recommendation names the highest-impact optimization
- a reviewer can trace the recommendation back to live metrics and code paths
- before/after evidence shows the optimization improved throughput or saturation
- the pipeline still emits timing rows and the optimization summary

## Practical notes
- Prefer the repo wrapper for transform backlog intake so the `transform` project scope is selected automatically.
- When the user asks for project backlog/status, show both the live backlog snapshot and the current kanban board snapshot.
- Do not mark the recommendation closed until the validation path is reproducible from the documented source or fixture.
