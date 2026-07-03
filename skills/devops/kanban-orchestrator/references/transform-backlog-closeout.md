# Transform backlog closeout recipe

Use when a transform repo task or recommendation has been implemented and needs live backlog closeout.

## Closeout sequence
1. Run the repo wrapper from the transform checkout:
   - `./scripts/backlog status`
2. Close the live recommendation by id:
   - `./scripts/backlog complete REC-...`
3. Re-run `./scripts/backlog status` and confirm:
   - `open_recommendations: 0`
   - `open_tasks: 0`
4. Preserve the backlog file as the source of truth; do not infer completion from chat state alone.

## Notes
- The wrapper defaults to the `transform` project scope via `CODEX_BACKLOG_PROJECT=transform`.
- The complete command accepts the recommendation id directly; do not add placeholder flags unless the wrapper help explicitly documents them.
- Keep local build artifacts separate from backlog state; cleanups should only remove temporary verification output when explicitly approved.
