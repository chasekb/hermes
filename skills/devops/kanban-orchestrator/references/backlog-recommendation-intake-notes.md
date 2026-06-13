# Backlog recommendation intake notes

Use this when turning a user feature request into one or more durable project backlog recommendations.

## Observed intake shape
- `kind`: `recommendation`
- `project_id`: the project scope you want to target (for this repo, `transform`)
- Required fields: `title`, `summary`, `details`, `priority`, `tags`
- Dedupe rule: identical `title` within the same `project_id` should be treated as a duplicate unless the prior item is already closed

## Recommended recommendation body structure
Put the implementation guidance into `details` with two explicit sections:

### Execution checklist
Use bullet points that can be translated into tests or implementation steps.
Good checks usually include:
- locate the current code path or dispatch path
- implement the smallest runnable slice
- add tests for behavior, order, or failure cases
- update docs/help text if the user-facing surface changed

### Closeout criteria
Use bullet points that a reviewer can verify after the change.
Good checks usually include:
- the new behavior exists in the live path
- existing standalone behavior still works
- tests prove the new behavior and protect the old one
- docs or saved usage examples match the implemented behavior

## Good practice
- Keep each recommendation focused on a single outcome.
- Prefer one recommendation per independent lane.
- If the request spans multiple lanes, create separate recommendations rather than burying unrelated work inside one item.
- After intake, re-read the backlog status so you can verify the item count and confirm the items landed in the intended project scope.
