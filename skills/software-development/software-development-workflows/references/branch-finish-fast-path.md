# Branch finish fast path

Use this when the user explicitly asks you to "commit and push" the current work.

Procedure:
1. Verify the relevant tests or checks pass.
2. Inspect `git status` and stage only intended files.
3. Commit with a concise conventional commit message.
4. Push the current branch to `origin`.
5. Verify the pushed head SHA matches local `HEAD`.

Pitfalls:
- Do not stop to present a merge/PR choice menu when the user has already chosen commit+push.
- If generated artifacts are part of the deliverable, stage them explicitly instead of assuming they are disposable.
- Add ignore rules for ephemeral build caches and `__pycache__`-style artifacts before staging, rather than relying on cleanup after the fact.
