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
- Durable execution is increasingly layered either inside the framework or in an external workflow engine such as Temporal's Agents SDK integration.
- Boundary-aware telemetry is converging with trajectory-aware evaluation: OpenTelemetry is adding agent-invocation and tool-execution duration metrics plus requested reasoning-level attributes, while ADK is separating tool-trajectory scoring from final-response quality.
- Result surfaces are becoming control-plane artifacts too: OpenAI now separates final output, replay history, continuation IDs, and resumable approval state, which means harnesses and loops have to agree on more than just the final answer.
- Progress signaling is part of the same boundary story: LangGraph's heartbeat-based idle timeouts make loop liveness visible to the runtime and the harness at the same time.

## Hermes-specific gap themes to track
- Need for an explicit trace/eval harness around agent behavior.
- Need for stronger loop termination and escalation policies.
- Need for durable, checklist-driven activity tracking.
- Need to compare runtime surfaces against research-backed best practices.
- Need to align Hermes tracing and eval conventions with the dedicated OpenTelemetry GenAI semantic-conventions repo.
- Need to align Hermes eval criteria with trajectory-first harnesses and boundary-aware loop telemetry.

## Maintenance log
- 2026-06-12: split from the combined research notebook.
- 2026-06-16: the overlap is now more explicit: harnesses expose approvals, environment controls, and eval surfaces, while loop runtimes expose checkpoints, thread IDs, retries, and event-loop resumption.
- 2026-06-18: the synthesis now has a clearer split between trace-first harness evaluation and durability-oriented loop orchestration, with Temporal highlighting the workflow engine as the place to preserve control flow across crashes and pauses.
- 2026-06-19: ownership boundaries are now part of the control surface: OpenAI distinguishes delegated ownership (`handoffs`) from bounded specialist calls (`agent.asTool()`), while LangGraph separates retries, terminal error handling, human interrupts, and cooperative drain into distinct primitives; that means loop topology directly affects trace volume and approval surface area.
- 2026-06-20: OpenTelemetry's new agent/tool duration metrics and ADK's trajectory-first evaluation criteria tighten the overlap between loop boundaries, telemetry, and harness scoring.
- 2026-06-21: OpenAI's results and guardrails docs now make resumable approval state explicit even across nested multi-agent paths, and LangGraph's heartbeat-based idle timeouts connect progress signals to termination behavior.
