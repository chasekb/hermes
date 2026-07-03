# Capability Surface Survey Gate

Use this when a request might introduce or significantly extend a Hermes capability surface such as a new skill, MCP integration, workflow, rule, hook, memory backend, or retrieval layer.

## Trigger
- User asks for a new capability surface, integration, or workflow enhancement.
- The work mentions knowledge graphs, memory/entity resolution, provenance, retrieval, or cross-surface orchestration.
- The request could be solved by an existing Hermes surface instead of inventing a new one.

## Survey lanes
- Installed skills and linked references
- MCP servers and adapters
- Workflow registry entries
- Hooks and runtime config surfaces
- Existing notes / backlog items that already address the problem
- Relevant memory or retrieval providers that may already cover the use case

## Output shape
- What exists already
- What exists partially
- What is missing
- Which gaps are safe to defer
- Which gaps deserve separate backlog items

## Pattern from this session
For knowledge-graph research, explicitly compare Hermes surfaces such as:
- memory provider / retrieval layer
- skills
- rules/config
- hooks
- workflow registry
- notes and backlog artifacts

## Rule
Before inventing a new Hermes surface, survey the existing ones first and record the result in a durable note or backlog item.