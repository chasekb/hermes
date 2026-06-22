# Hermes Obsidian vault activation checklist

Use this checklist when bootstrapping or verifying the Hermes notes vault.

1. Confirm the canonical root is `~/.hermes/notes`.
2. Confirm the core note set exists:
   - `Projects/hermes/Index.md`
   - `Projects/hermes/Decision Log.md`
   - `Projects/hermes/Session Summary.md`
   - `Projects/hermes/Open Questions.md`
3. Confirm the index links the decision log and session summary.
4. Confirm `OBSIDIAN_VAULT_PATH` resolves to the Hermes vault root in a fresh shell.
5. Confirm note reads and writes succeed with concrete absolute paths.
6. Confirm the retrieval path stops after directly linked notes.
