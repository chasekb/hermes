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
