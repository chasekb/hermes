---
project_id: hermes
note_type: capability-survey
updated_at: 2026-07-03T09:37:26Z
---
# Capability Surface Survey

This note captures the reusable survey-first approach for new Hermes capability surfaces.

## Use case
Use this when evaluating whether a new skill, MCP integration, workflow, rule, hook, memory backend, or retrieval layer should be added instead of reusing an existing path.

## Survey lanes
- installed skills and linked references
- MCP servers and adapters
- workflows and registry entries
- hooks and runtime config surfaces
- existing notes / backlog items that already solve the problem
- memory or retrieval providers that may already cover the use case

## Reusable gate
- `skills/devops/kanban-orchestrator/references/public-skill-survey-gate.md`
- `skills/devops/kanban-orchestrator/references/workflow-registry.md`

## Current Hermes-relevant surfaces
- `skills/autonomous-ai-agents/hermes-agent/SKILL.md`
- `skills/autonomous-ai-agents/opencode/SKILL.md`
- `skills/autonomous-ai-agents/mixture-of-agents/SKILL.md`
- `skills/autonomous-ai-agents/multi-agent-evaluation-router/SKILL.md`
- `skills/software-development/software-development-workflows/SKILL.md`
- `skills/devops/kanban-orchestrator/SKILL.md`
- `plugins/memory/hindsight/README.md`
- `agent/memory_manager.py`
- `config.yaml`
- `agent/shell_hooks.py`
- `backlog/backlog.json`
- `backlog/decision-memory.json`
- `notes/Projects/hermes/Index.md`
- `notes/Projects/hermes/Decision Log.md`

## Gap matrix

| Area | Hermes surface(s) | Status | Evidence | Follow-up |
| --- | --- | --- | --- | --- |
| Long-term memory / entity graph | Hindsight plugin, `MemoryManager` | partial | Hindsight already provides knowledge graph, entity resolution, and multi-strategy retrieval; `MemoryManager` centralizes the built-in provider plus at most one external provider. | Keep Hindsight as the current substrate; avoid inventing a second memory surface unless a concrete consumer needs one. |
| Cross-surface retrieval / recall | Hindsight, notes, backlog | partial | The memory plugin can store and recall across a bank, but notes and backlog remain separate durable surfaces. | Keep the survey-first gate and record any gap as a separate backlog item rather than conflating it with memory storage. |
| Skills and workflow packaging | Skills, workflow docs | present | Hermes already has a reusable skill system and workflow-class skills for maintenance and orchestration. | Use skills for repeatable procedures; do not encode project-specific comparisons as new skills unless they recur. |
| Hooks and runtime config | `agent/shell_hooks.py`, `config.yaml` | partial | The runtime exposes hooks and config surfaces, but no dedicated knowledge-graph orchestration layer was visible. | Treat any new hook/rule as a follow-up item with its own survey and closeout criteria. |
| Notes / backlog continuity | Hermes notes, backlog JSON | present | The project index, decision log, and backlog provide durable note and review surfaces. | Use notes for the comparison artifact and backlog for any follow-up implementation items. |
| Dedicated Hermes knowledge-graph surface | none identified | missing | No first-class KG query/index surface was needed after reviewing the existing memory and notes stack. | Defer a new surface until a concrete workflow proves the current stack is insufficient. |

## Current decisions
- Treat Hindsight as the existing memory/graph substrate, not as a trigger to invent a new surface.
- Keep knowledge-graph work as a comparison artifact unless a concrete missing capability emerges.
- Defer any new surface to a separate backlog item with explicit execution and closeout criteria.

## Closeout summary
- The survey is source-backed and compares the current Hermes surfaces against the KG research question.
- The matrix records present, partial, and missing support instead of a vague brainstorm.
- No new Hermes surface was introduced as part of this backlog item.