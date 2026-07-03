# Research backlog closeout via durable notes

Use this pattern when a Hermes project backlog item is research-oriented and the implementation result is primarily a durable note, matrix, or routing policy rather than code.

## Closeout steps
1. Create the durable project note that contains the survey, matrix, or routing decision.
2. Index the note from the Hermes project MOC so future retrieval starts from the project entrypoint.
3. Update the project decision log to point at the new note.
4. Mark the backlog item closed only after the durable artifact and the index link both exist.
5. Re-read the backlog JSON after editing and verify the item count/status mix.

## Evidence to keep
- note path(s)
- project index path
- decision-log path
- backlog item id(s)
- final open/closed counts

## Pitfall
Do not close a research backlog item just because the content was drafted. The closeout is incomplete until the project index and backlog record both reflect the new durable artifact.