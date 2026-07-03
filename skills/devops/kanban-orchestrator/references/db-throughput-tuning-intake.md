# DB Throughput Tuning Intake Notes

Use this when a backlog recommendation asks to improve database write throughput in a compose/Podman/Docker environment without regressing reads.

## Intake shape
- Scope the work to the exact database service, compose file, and host configuration in play.
- Treat the throughput target as a hypothesis to validate, not a guaranteed outcome.
- Prefer the smallest safe change set first; do not jump straight to aggressive Postgres tuning.

## Execution checklist
- Inventory host hardware and runtime limits that can bottleneck Postgres: CPU cores, RAM, storage type, filesystem, cgroup limits, shared memory, and container runtime constraints.
- Establish a baseline with the current compose settings using the same workload shape for reads and writes.
- Change one bottleneck-oriented setting group at a time so the effect is attributable.
- Benchmark the candidate config under a mixed read/write load, not write-only traffic.
- Compare write throughput, read latency, and error rate against baseline.
- If the target is not reachable without read harm, record the best safe compromise and the limiting resource.

## Closeout criteria
- A reviewer can reproduce the baseline and final comparison from documented commands or fixtures.
- The final compose file either contains the validated tuning or documents why no safe tuning was applied.
- Write throughput improved materially relative to baseline, or the ceiling is explicitly documented.
- Read throughput and p95 latency stayed within the agreed guardrail, or any regression is called out as a follow-on item.

## Pitfalls
- Do not validate with write-only benchmarks and assume read performance is unaffected.
- Do not claim a doubling target was achieved unless the same mixed workload and dataset were used for both measurements.
- Do not broaden the scope to code refactors until the bottleneck is understood and measured.
