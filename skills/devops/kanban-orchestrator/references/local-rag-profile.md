# Default local RAG profile for Hermes

This reference turns the note-layer workflow into a reusable local retrieval profile/runbook.

## Goal
Use selective local retrieval sources without turning the vault into transparent memory, and without inventing hidden fallback paths.

## Canonical sources and roles
- Obsidian project index note: entry point and navigation map.
- Obsidian decision log and session summaries: the current state of the project.
- Workflow registry and backlog: process, intake, and status truth.
- MCP-backed structured sources: repositories, databases, fetch/search tools, and other external data.
- Hermes skills: repeatable procedures and reusable workflows.
- Hermes built-in memory: stable user/environment facts only.

## Routing rules
1. Questions about a project's current state -> project index note plus the latest session summary.
2. Questions about a decision -> decision log first.
3. Questions about structured local data -> an MCP source or repo tool, not the vault.
4. Questions about a reusable procedure -> an existing skill first.
5. Questions about a new capability surface -> run the public skill / MCP / workflow survey gate before creating anything.
6. If the needed source is not linked or registered, stop and report it rather than inventing a hidden retrieval route.

## Minimal profile shape
The exact implementation can be either a dedicated profile clone or an explicit `hermes -p <profile>` wrapper, but the behavior should stay the same.

```yaml
profile_name: local-rag
purpose: selective local retrieval
load_skills:
  - note-taking/obsidian
  - mcp/native-mcp
  - devops/kanban-orchestrator
  - software-development/subagent-driven-development
retrieval_sources:
  - obsidian-index
  - obsidian-decision-log
  - obsidian-session-summary
  - workflow-registry
  - mcp-structured-sources
behavior:
  start_from: project_index
  expand_hop_limit: 1
  fallback: stop-and-report
  no_full_vault_load: true
  no_hidden_retrieval: true
```

## Profile operator checklist
- Confirm the index note exists for the project.
- Confirm the linked notes are the only notes needed for the task.
- Confirm the relevant MCP sources are configured and reachable.
- Confirm the survey gate has already been used if a new retrieval source is being proposed.
- Confirm the workflow stays local and explicit.

## Smoke test
A minimal smoke test looks like this:
1. Create or identify an index note and one decision note.
2. Ask Hermes to continue the task from the index note.
3. Hermes should answer using only the index note, the decision note, and stable memory if needed.
4. Hermes should explicitly say when it needs a different linked note.
5. Hermes should not request the whole vault or invent an undocumented fallback.

## Limits
- No full-vault loading.
- No transparent memory.
- No hidden retrieval paths.
- No automatic promotion of notes into memory.
- No new retrieval source without the survey gate.
