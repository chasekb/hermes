# Open Hermes backlog display recipe

When asked to show the open Hermes project backlog:

1. Read the live backlog JSON from `~/.hermes/backlog/backlog.json`.
2. Treat that file as the source of truth, even if the chat history contains an older summary.
3. Filter items where `status != "closed"`.
4. Present a concise list with:
   - id
   - priority
   - status
   - title
5. If the file was recently patched, reset, or re-written, re-read it before reporting so the output reflects the current live state.
6. Keep the response short unless the user explicitly asks for more detail.

Useful when the backlog has been through patch churn or restoration and the previous conversational summary may be stale.
