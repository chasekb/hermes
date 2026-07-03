# Remote build monitoring session notes

This repo’s GitHub Actions verification flow surfaced a few practical points:

- Always verify the exact push run by `headSha`, URL, and final `conclusion`.
- Do not treat a sibling pull_request run on the same SHA as proof for the push that initiated the build.
- `gh run watch --exit-status` can keep streaming for a long time on backend-heavy matrices; if it times out, continue with `gh run view --json status,conclusion,headSha,url,updatedAt` against the exact run id.
- For long backend matrices, it’s normal for frontend legs and manifest publish jobs to finish well before the backend jobs do.
- If duplicate runs on the same SHA are clogging the queue, cancel only the stale duplicates that are blocking the intended verification path.