---
project_id: hermes
note_type: gap-analysis
updated_at: 2026-06-12T00:00:00Z
---
# Harness and Loop Engineering Gap Analysis

Compare the researched harness and loop engineering best practices against the current Hermes runtime, note, and backlog surfaces.

## Hermes surfaces reviewed
- /Users/bernardchase/.hermes/config.yaml
- /Users/bernardchase/.hermes/agent-hooks/hook_router.py
- /Users/bernardchase/.hermes/backlog/backlog.json
- /Users/bernardchase/.hermes/notes/Projects/hermes/Index.md
- /Users/bernardchase/.hermes/notes/Projects/hermes/Session Summary.md
- /Users/bernardchase/.hermes/notes/Projects/hermes/Decision Log.md
- /Users/bernardchase/.hermes/notes/Projects/hermes/Open Questions.md
- /Users/bernardchase/.hermes/notes/Research/Agents/Harness Engineering.md
- /Users/bernardchase/.hermes/notes/Research/Agents/Loop Engineering.md
- /Users/bernardchase/.hermes/notes/Research/Agents/Harness Loop Synthesis.md

## Gap matrix

| Area | Hermes surface(s) | Status | Evidence | Follow-up |
| --- | --- | --- | --- | --- |
| Trace visibility | hook router, decision memory, event log | partial | `hook_router.py` records note telemetry and MoA lifecycle hooks; the review ledger is durable but not yet a full eval harness. | Keep the event log and add a dedicated trace/eval harness for agent trajectories. |
| Reproducibility / fixture-backed verification | config, backlog, notes | partial | `config.yaml` has checkpointing disabled and no fixture-backed harness surfaced in the inspected files. | Add a fixture-backed verification path before treating workflow claims as regressions-tested. |
| Bounded loop termination | config, hook router | partial | `max_turns` exists, and tool-loop warnings exist, but hard-stop loop guardrails are disabled and semantic termination is not explicit. | Define semantic termination criteria and escalation thresholds, then tighten hard-stop behavior where appropriate. |
| Retry vs bug separation | config, hook router | partial | `api_max_retries` and tool-loop guardrails exist, but there is no documented error-class policy in the inspected runtime surfaces. | Distinguish transient failures from logic bugs in the runtime policy and review path. |
| Approval / escalation thresholds | config, hook router | partial | pre-approval notifications exist, but no threshold matrix or escalation policy was visible in the inspected files. | Add a simple approval/escalation matrix for high-risk or repetitive actions. |
| Durable checkpoints / resumability | config | missing | `checkpoints.enabled` is false. | Enable durable checkpoints for workflows that need pause/resume semantics. |
| Checklist-driven activity tracking | project notes, backlog | covered | The new Hermes activity-tracking checklist note provides a stable operational template and backlog linkage. | Keep using the checklist in future action summaries and closeouts. |
| Evaluation / CI gating | backlog, notes | missing | No dedicated eval harness or trajectory regression gate was visible in the inspected Hermes surfaces. | Add a minimal CI or fixture-backed eval gate for agent behavior before large workflow changes. |

## Current decisions
- Keep selective note retrieval and centralized hook routing.
- Improve loop termination, approvals, and checkpointing before scaling longer-running workflows.
- Use the activity checklist as the canonical operational tracker.
- Defer heavier eval infrastructure until the trace shape and checkpoint story are clearer.

## Closeout summary
- The analysis is source-backed and tied to concrete Hermes files.
- Remaining gaps are documented as follow-up work rather than assumed to be implemented.
- This note is the durable record for the current gap-analysis recommendation.
