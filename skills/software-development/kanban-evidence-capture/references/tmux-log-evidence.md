# Tmux and runtime-log evidence recipe

## Capture

Capture full scrollback to a safe temporary path:

```sh
tmux capture-pane -p -t <session>:<window>.<pane> -S - > /tmp/<project>-<pane>.log
```

Record line count and byte size. Keep the source path out of the repository unless the user explicitly requests a checked-in report.

## Condense without losing provenance

Use a small parser to report:

- total lines and bytes;
- counts of open/completed trades, generated signals, HOLDs, blockers, warm-up/rejected inference, and provider failures;
- unique blocker/error codes;
- first and last timestamps;
- sequence-to-timestamp gaps and representative lines for startup, model load, worker start, and failures.

Do not infer root cause from counts alone. Pair each finding with source code paths or an explicit follow-up investigation card.

## Attach and verify

Attach the complete artifact to one relevant Kanban task. Verify the task record or attachment listing contains the expected stored filename, `text/plain` content type, and exact byte size. Task descriptions should contain only condensed evidence and the pane provenance.

## Trading diagnosis dimensions

For a zero-trade ML order-book session, preserve separate counters for selected symbols, quote successes/failures, transformer readiness/warm-up, generated signals/HOLDs, gate blockers, executable intents, fills, and persisted trades. For perceived slow refresh, timestamp worker ticks, quote completion, signal generation, event delivery, cache update, and UI render separately. For a large-universe widget, verify that summaries remain compact while search/filter/detail access preserves every failure category and selected symbol.
