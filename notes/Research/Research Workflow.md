---
project_id: hermes
note_type: research-workflow
updated_at: 2026-06-12T00:00:00Z
---
# Research Workflow

Automated workflow for daily research updates.

## Purpose
Keep Hermes research current without overwriting prior findings.

## Daily routine
1. Read [[Research Index]].
2. Open the active research hub and topic pages.
3. Search for new primary-source material.
4. Append only new findings.
5. Update source registry and maintenance log entries.
6. Verify that prior content was not rewritten.

## Rules
- Append-only edits only.
- No fabricated claims.
- No duplicate source entries unless a source has a new relevant angle.
- If nothing substantive changed, record that explicitly in the session summary.
- Keep the update focused on harness engineering and loop engineering unless a new adjacent topic is clearly relevant.

## Automation
- Daily schedule is maintained by a Hermes cron job.
- The job runs in the Hermes workdir and updates the research notes directly.

## Daily log
- 2026-06-12: workflow established; future daily entries append below.
- 2026-06-12: added the Skill Curation research note and the reusable workflow skill-ification rubric.
- 2026-06-16: reviewed refreshed LangChain, Google ADK, and OpenTelemetry sources; appended notes on harness capability grouping, per-node fault tolerance, checkpointed interrupts, and deterministic loop/event-loop models.
- 2026-06-18: reviewed current OpenAI eval guidance, LangChain fault-tolerance/interrupt docs, and Temporal's Agents SDK integration; appended source-backed notes on trace-first evaluation sequencing, retry-vs-error-handler precedence, durable execution, and workflow/activity separation.
- 2026-06-19: reviewed current OpenAI orchestration and LangGraph fault-tolerance updates; appended source-backed notes on handoffs vs agents-as-tools, over-splitting costs, checkpointed failure provenance, interrupt bypass behavior, and cooperative drain/shutdown.
- 2026-06-20: reviewed OpenTelemetry GenAI semantic-conventions updates and Google ADK conformance evaluation docs; appended source-backed notes on agent/tool duration metrics, requested reasoning level telemetry, and trajectory-vs-final-response evaluation criteria.
- 2026-06-21: reviewed refreshed OpenAI results/guardrails docs and LangGraph fault-tolerance updates; appended source-backed notes on result-surface selection, nested approval interruptions, and heartbeat-based idle timeouts.
- 2026-06-22: reviewed LangGraph fault-tolerance updates and the OpenAI Agents SDK running-agents guide; appended source-backed notes on attempt-aware retries, structured timeout metadata, per-send timeout overrides, `RunState` resumption, and explicit streaming/turn-budget surfaces.
- 2026-06-23: reviewed current OpenAI, LangChain, Temporal, Anthropic, Google ADK, and OpenTelemetry sources; no substantive changes beyond prior notes, so no topic updates were needed.
- 2026-06-24: reviewed current OpenAI eval/orchestration/results docs, LangGraph fault-tolerance, and the Temporal Agents SDK integration; appended source-backed notes on heartbeat-only idle refresh, `runtime.heartbeat()` semantics, `execution_info.node_attempt`, and structured timeout provenance.
- 2026-06-25: reviewed refreshed LangGraph fault-tolerance and OpenAI results/state docs; appended source-backed notes on default auto-refresh progress signals, strict heartbeat-only idle refresh, `TimeoutPolicy` split timeouts, and richer result/diagnostics surfaces for replay and approvals.
- 2026-06-26: reviewed refreshed OpenTelemetry GenAI semantic-conventions changes; appended source-backed notes on cross-boundary agent identity and aligned invoke-agent/tool telemetry.
- 2026-06-27: reviewed refreshed OpenAI eval/observability docs and LangGraph fault-tolerance; appended source-backed notes on code-first SDK tracing before graders and `Send`-level dynamic timeout overrides for fan-out paths.
- 2026-06-28: reviewed current OpenAI, Anthropic, LangChain, Google ADK, OpenTelemetry, and Temporal sources; found no substantive changes beyond prior notes, so no topic updates were needed.
- 2026-06-29: reviewed current OpenTelemetry, OpenAI Agents SDK, LangGraph, Anthropic, Google ADK, and Temporal sources; OpenTelemetry's GenAI reference repo added native Agent Framework coverage with mock Responses function-call and usage-detail payloads, so I appended source-backed notes on the expanded telemetry surface.
- 2026-06-30: reviewed LangGraph 1.2.7 fixes for `Overwrite` JSON roundtrips and delta-channel snapshot timing; appended source-backed notes on preserving overwrite intent across serialized state updates and checkpointing after overwrite application.
- 2026-07-02: reviewed OpenAI Agents SDK strict-schema handoff validation and Anthropic's agentic-search benchmark reproduction cookbook; appended source-backed notes on strict validation at control boundaries plus programmatic tool calling, server-side compaction, and task budgets for long-horizon benchmark harnesses.
