# Publishing an Existing Local Workspace Publicly

This note captures a safe workflow for turning an already-populated local directory into a public GitHub repository without leaking local state.

## Recommended sequence

1. Inventory the workspace before adding files.
2. Create a default-deny `.gitignore` first.
3. Allow only explicitly approved top-level files and directories.
4. Explicitly exclude runtime state, caches, logs, sessions, profiles, secrets, and nested working copies.
5. Validate ignore behavior with `git check-ignore` and `git add -n` before staging.
6. Commit locally, then create the GitHub repo and push.

## Practical notes

- Root-anchor allow rules when the repository contains many top-level siblings.
- Prefer explicit allowlists for public snapshots instead of broad globbing.
- Treat nested checkouts and local agent state as non-public by default.
- Verify that a representative file from an intended included subtree is not ignored.
- Verify that known runtime artifacts are ignored before publishing.

## Verification commands

```bash
git check-ignore -v <path>
git add -n .
git status --short --branch
```

## Common exclusions for Hermes workspace snapshots

- state databases and WAL/SHM sidecars
- profiles, sessions, caches, logs, and memories
- nested agent checkout directories
- generated hub/usage/manifest state inside skill trees
