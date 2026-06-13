# tmux + Python package stack triage

Use this note when a local compose/Podman stack is being debugged from a tmux pane and one service is a Python package entrypoint.

## What to verify first

1. Do not trust shell activation state alone.
   - Check the active interpreter and PATH resolution explicitly.
   - Prefer invoking the repo venv interpreter directly when debugging:
     - `./.venv/bin/python ...`
     - `./.venv/bin/ai-dev ...`

2. Isolate the first real failure in the pane.
   - Capture a short log window around the first explicit error.
   - Ignore later noise until the earliest blocker is explained.

3. Distinguish a port conflict from a broken service.
   - If a service on the expected host port answers with the wrong API or a different server signature, confirm the port owner before changing code.
   - Use a free port if the repo’s default collides, then update config, runtime defaults, tests, and docs together.

4. Distinguish package-root import failures from application bugs.
   - If a compose service launches a Python module from inside a subdirectory and fails with `ModuleNotFoundError` for an in-repo package, the container likely does not have the repo root on `PYTHONPATH`.
   - Prefer mounting the repository root and running the entrypoint as a module, e.g. `python -m package.module`, so package imports resolve the same way they do locally.

## Common fixes that proved durable

- Re-source the intended virtual environment and rehash the shell if tmux kept a stale command path.
- Verify container health with a direct HTTP endpoint after `up`, not just with compose logs.
- When a host-side model/API service is expected to be reachable from containers, validate the rendered base URL and the live endpoint together.

## Verification pattern

- After any fix, rerun the exact compose/CLI command that failed.
- Confirm service health with a real endpoint response.
- Confirm the repo status is consistent with the updated runtime contract before declaring the stack healthy.
