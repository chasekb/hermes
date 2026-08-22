# Cleanup boundaries

This reference records the workspace-cleanup policy that emerged from a trade repo session.

Core rule
- Remove only local build artifacts by default.
- Never delete a database data directory unless the user explicitly approves deletion of a database data directory and you perform a follow-up verification afterward.

Treat as protected unless explicitly approved
- Database data directories mounted or bind-mounted for runtime state
- Persistent cache/state directories that are used as application data stores

Treat as cleanup candidates
- Build directories (for example: build/, cmake-build-*/)
- Compiler artifacts, object files, temporary packaging files, test logs, coverage outputs
- Generated model/package temp files that are clearly transient and not runtime data

Verification after an approved data-directory deletion
1. Confirm the user explicitly approved deleting a database data directory.
2. Delete only the approved path(s).
3. Verify the deletion by checking the path no longer exists and reviewing git status / workspace state.
4. Report exactly what was deleted.

Example from the trade repo
- docker-compose.yml bind-mounts ./data/databases/postgres to /var/lib/postgresql/data
- docker-compose.yml bind-mounts ./data/cache/redis to /data
- In that repo, deleting ./data/databases/postgres or ./data/cache/redis removes live database/cache state, not just temporary build output.
