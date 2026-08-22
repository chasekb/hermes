# Remote-only CI build verification

Use this when a Kanban-backed repository must not build locally.

1. Do not run package or container builds locally; inspect metadata and workflow configuration only.
2. Ensure GitHub Actions contains an actual build/package job, not only lint or repository-integrity checks.
3. Commit all requested changes and push the exact commit.
4. If an HTTPS OAuth push rejects workflow-file changes for missing `workflow` scope, switch the repository's authenticated remote to SSH and retry.
5. Dispatch or identify the workflow run for the pushed ref, then verify the exact head SHA, run URL, overall conclusion, and every build job conclusion.
6. Report validation-only success separately from actual build success; never use an older or integrity-only run as build proof.
