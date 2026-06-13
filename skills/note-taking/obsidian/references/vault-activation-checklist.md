# Obsidian vault activation checklist for Hermes

Use this when the Obsidian workflow exists in docs but there is no confirmed live vault path yet.

## Goal
Turn the documented note-layer workflow into an operational vault-backed workflow.

## Checklist
1. Resolve or create a concrete vault path.
   - Preferred source: `OBSIDIAN_VAULT_PATH`.
   - If absent, choose a real local vault directory and make it explicit.
2. Set the vault path in Hermes config or environment so file tools can use it as a concrete absolute path.
   - Route note lifecycle telemetry through `~/.hermes/agent-hooks/hook_router.py` so reads/writes are observable.
3. Create the minimal project note set:
   - Project index / MOC
   - Decision log
   - Session summary
   - Optional open-questions note
4. Seed the notes with wikilinks so the index can navigate to the other notes.
5. Verify the workflow end-to-end:
   - list notes under the vault
   - read the index note
   - follow one linked note
   - write a small session-summary update

## Operational meaning
- If no concrete vault path is available, treat the Obsidian docs as the workflow spec and the local-rag examples as shape references only.
- The captured reference notes under `~/.hermes/skills/devops/kanban-orchestrator/references/examples/local-rag/` are examples of the intended shape, not a substitute vault.
- Once a vault is configured, use the selective-retrieval policy from the context-layer docs.
