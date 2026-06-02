---
name: workspace-cleanup
description: "Safe cleanup of local build artifacts with explicit protection for persistent data directories."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [cleanup, build-artifacts, safety, workspace, data-protection]
---

# Workspace Cleanup

Use this skill whenever the user asks to remove local artifacts, clean a working tree, free disk space, or prepare a repo for a fresh build.

Primary goal: remove transient build outputs without destroying persistent application state.

Reference note: see `references/cleanup-boundaries.md` for the concrete policy and the trade-repo example that motivated it.

## Default cleanup policy

- Prefer deleting only clearly transient files: build directories, compiler outputs, temp packaging files, logs, coverage artifacts, generated caches that are not runtime state.
- Treat database data directories, mounted volumes, and persistent cache/state directories as protected.
- If a path might contain live data, do not delete it unless the user explicitly approves that deletion.
- If the user approves deleting a database data directory, perform a follow-up verification after deletion and report the result.

## Cleanup workflow

1. Inspect the workspace and identify candidate paths.
2. Classify each path as either:
   - transient build artifact, or
   - persistent data/state directory.
3. Remove only the transient build artifacts by default.
4. If a persistent data directory is involved, ask for explicit approval before deletion.
5. After any approved persistent-data deletion, verify that the target path is gone and confirm the scope of deletion.

## What counts as a build artifact

Usually safe to remove:
- build/
- cmake-build-*/
- .cache/ entries that are only compiler/test intermediates
- temporary model packaging files ending in .tmp, .temp, or similar transient suffixes
- compiler object files and generated binaries
- logs and reports that are reproducible

## What is protected

Do not remove by default:
- database directories under data/ when they are bind-mounted into containers
- Redis/Postgres/MySQL runtime directories
- application state directories that store live or user-generated data
- anything whose purpose is ambiguous and may be persistent

## Pitfalls

- A directory named data/ is not automatically a safe cleanup target.
- Compose bind mounts often make local directories part of runtime state; inspect compose files before deleting them.
- If a cleanup request is broad, narrow it to the smallest set of transient files that satisfies the request.
- Never describe a database data deletion as a routine cleanup step.

## Verification

After cleanup, confirm:
- the intended build artifacts are gone
- the workspace still contains required source files
- protected data directories were not deleted unless explicitly approved
- git status only shows expected source changes or intentional deletions
