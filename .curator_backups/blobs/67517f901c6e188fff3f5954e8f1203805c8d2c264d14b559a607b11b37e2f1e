# Remote CI session reference

Validated workflow for Hermes homes with a nested runtime repository:

1. Inspect root and nested repository status independently.
2. Commit and push the root Hermes-home changes.
3. Commit and push nested runtime changes to an authorized fork or branch when upstream rejects the credential.
4. Use the repository-supported build path. Hermes rejects wheel/sdist builds; `uv sync --locked --python 3.11 --extra dev` is the supported remote environment build path.
5. Verify the exact GitHub Actions run by `headSha`, final conclusion, job conclusions, and URL.
6. If the workflow is queued too long, poll `gh run view`; a watcher timeout is not proof of failure.
7. Separate package/environment build failures from focused Kanban policy-test failures. Fix the first concrete job error before rerunning.
