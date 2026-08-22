# Trade backlog materialization pattern

Use this when a repo-local backlog recommendation should become a live Hermes backlog item.

## Pattern
1. Read the live backlog JSON and identify the project-scoped items for `project_id=trade`.
2. Promote each recommendation into a discrete live backlog item with:
   - stable id
   - title and summary
   - `project_id=trade`
   - `scope` set to the repo path
   - exact `links` to the source code / evidence docs
   - `execution_criteria` and `closeout_criteria`
   - notes that keep the item focused on one investigation lane
3. Verify the new items are present in the live backlog and the counts/status mix make sense.
4. If the repo contains a duplicate recommendation doc that is only serving as staging or note-taking, remove it after the live backlog items are verified.
5. Report the live backlog ids and the cleanup result together so the durable source of truth is clear.

## Guardrails
- Do not rely on a chat summary when the backlog JSON is available.
- Keep the live Hermes backlog separate from repo-local docs until the live items are confirmed.
- Preserve the execution/closeout criteria in the live item; do not collapse them into a vague summary.
