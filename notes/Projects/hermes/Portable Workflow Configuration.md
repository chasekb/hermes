# Portable Workflow Configuration

The tracked workflow configuration is host-neutral and resolves local paths at runtime:

- `HERMES_HOME` points to the active Hermes profile home. It supplies the shell-hook router, filesystem MCP root, and SQLite state path.
- `HERMES_PROJECT_ROOT` points to the local project workspace containing the `db/`, `trade/`, and `cohida/` environment files used by the PostgreSQL MCP wrappers.
- Keep those `.env` files local and untracked. They are sourced only by the wrapper process; credentials do not belong in `config.yaml`.

Shell hooks expand `${HERMES_HOME}` without invoking a shell. An unset variable remains unresolved and therefore cannot redirect execution to another local path. PostgreSQL wrappers use `${HERMES_PROJECT_ROOT:?HERMES_PROJECT_ROOT must be set}` so a missing project root aborts before the MCP server starts. Each PostgreSQL wrapper continues to export `DB_READ_ONLY=true`.

For a machine-specific setup, export the two variables from the profile or service environment rather than editing the tracked configuration. The focused static contract tests in `tests/test_portable_config_paths.py` cover path substitution, missing project-root behavior, and read-only database intent.
