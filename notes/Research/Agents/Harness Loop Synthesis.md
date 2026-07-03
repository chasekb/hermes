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
- LangGraph now lets the loop choose between automatic idle refresh and strict heartbeat-only refresh, which makes progress provenance part of harness design, not just runtime design.
- OpenTelemetry's Agent Framework reference scenario widens the first-party telemetry baseline again, making function-call payload capture and usage-detail reporting part of the shared harness/loop contract.
- Benchmark reproduction is now explicitly about control surfaces as much as model capability: long-horizon search harnesses rely on programmatic tool calling, compaction prompts, and task budgets, while strict JSON-schema validation keeps handoff boundaries honest.

## Hermes-specific gap themes to track
- Need for an explicit trace/eval harness around agent behavior.
- Need for stronger loop termination and escalation policies.
- Need for durable, checklist-driven activity tracking.
- Need to compare runtime surfaces against research-backed best practices.
- Need to align Hermes tracing and eval conventions with the dedicated OpenTelemetry GenAI semantic-conventions repo.
- Need to align Hermes eval criteria with trajectory-first harnesses and boundary-aware loop telemetry.
- Need harnesses that preserve run state, retry metadata, and timeout provenance across resumptions.
- Need trace schemas that preserve agent identity consistently across both internal agent-invocation spans and tool-execution spans.
- Need trace schemas that preserve per-push timeout provenance for dynamic fan-out paths.
- Need harnesses that preserve overwrite intent across serialized state updates and checkpoint after overwrite application so replay starts from the same post-overwrite state.
- Need loop/harness documentation that preserves question and answer-format instructions through compaction on long-running research tasks.
- Need schema validation at handoff boundaries so control-flow coercion cannot hide behind apparently successful runs.

## Maintenance log
- 2026-06-12: split from the combined research notebook.
- 2026-06-16: the overlap is now more explicit: harnesses expose approvals, environment controls, and eval surfaces, while loop runtimes expose checkpoints, thread IDs, retries, and event-loop resumption.
- 2026-06-18: the synthesis now has a clearer split between trace-first harness evaluation and durability-oriented loop orchestration, with Temporal highlighting the workflow engine as the place to preserve control flow across crashes and pauses.
- 2026-06-19: ownership boundaries are now part of the control surface: OpenAI distinguishes delegated ownership (`handoffs`) from bounded specialist calls (`agent.asTool()`), while LangGraph separates retries, terminal error handling, human interrupts, and cooperative drain into distinct primitives; that means loop topology directly affects trace volume and approval surface area.
- 2026-06-20: OpenTelemetry's new agent/tool duration metrics and ADK's trajectory-first evaluation criteria tighten the overlap between loop boundaries, telemetry, and harness scoring.
- 2026-06-21: OpenAI's results and guardrails docs now make resumable approval state explicit even across nested multi-agent paths, and LangGraph's heartbeat-based idle timeouts connect progress signals to termination behavior.
- 2026-06-22: resumable `RunState`, attempt-aware retries, and per-send timeout overrides make execution-state provenance part of the harness/loop overlap, so Hermes needs to preserve more than final outputs when comparing agent runs.
- 2026-06-24: the latest LangGraph fault-tolerance docs sharpen the overlap further by separating `run_timeout` from heartbeat-only idle refresh and exposing `node_attempt` plus structured timeout context; Hermes harnesses should capture that provenance if they want fair comparisons of long-running runs.
- 2026-06-25: OpenAI's results/state guide now broadens the harness contract to include replay-ready histories, server-managed continuation IDs, resumable approval snapshots, and richer diagnostics; LangGraph now makes the idle-clock boundary more explicit with default auto-refresh signals versus strict heartbeat-only mode, so Hermes trace capture needs to preserve both continuation state and progress provenance.
- 2026-06-26: OpenTelemetry's GenAI repo now aligns agent identity across `invoke_agent.internal` and `execute_tool` surfaces, which sharpens the overlap between harness scoring and loop ownership correlation.
- 2026-06-27: OpenAI's eval guide now explicitly routes code-first SDK workflows through built-in tracing before graders, and LangGraph now exposes per-push `Send` timeout overrides for dynamic fan-out, so Hermes needs to preserve both high-signal traces and fan-out timeout provenance when comparing runs.
- 2026-06-29: OpenTelemetry's GenAI reference repo added native Agent Framework coverage and mock Responses payloads for function calls and usage details; Hermes should keep that telemetry shape in mind when comparing harness traces and loop ownership.
- 2026-06-30: LangGraph's overwrite fixes sharpen the harness/loop contract around serialized state updates and sparse replay, so Hermes traces and checkpoints need to preserve overwrite intent and post-overwrite snapshot timing.
- 2026-07-02: Anthropic's agentic-search cookbook and OpenAI Agents SDK strict-schema fix sharpen the overlap around long-horizon reproduction: harnesses need compaction-aware instructions and task budgets, while loops need strict validation at handoff boundaries.
