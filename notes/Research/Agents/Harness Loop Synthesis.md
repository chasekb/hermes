---
project_id: hermes
note_type: research-synthesis
updated_at: 2026-06-12T00:00:00Z
---
# Harness Loop Synthesis

## Cross-cutting synthesis
- Harnesses measure and constrain loops.
- Loops produce the traces that harnesses evaluate.
- Good loop design makes harnesses more legible and replayable.
- Good harness design surfaces failures in retries, termination, and control flow.

## Shared best practices
- Start with traces.
- Prefer deterministic checks where possible.
- Keep environments reproducible.
- Make control flow explicit.
- Calibrate automated judges with human review.
- Treat evals and runtime telemetry as durable artifacts.

## Shared do not dos
- Do not rely on final answers alone.
- Do not use drifting environments.
- Do not leave termination implicit.
- Do not trust judges or retries without calibration.
- Do not mix inspection, execution, and closeout without evidence.

## Emerging trends
- Trajectory-first evaluation.
- OpenTelemetry-style observability.
- Durable checkpointed execution.
- Graph-based orchestration.
- More human review and approval gates.

## Hermes-specific gap themes to track
- Need for an explicit trace/eval harness around agent behavior.
- Need for stronger loop termination and escalation policies.
- Need for durable, checklist-driven activity tracking.
- Need to compare runtime surfaces against research-backed best practices.

## Maintenance log
- 2026-06-12: split from the combined research notebook.
