# Local runtime tmux port conflicts

Session note for debugging host-served MLX and similar local services inside a repo.

When a service endpoint appears reachable but the expected app is not actually serving there:

1. Probe the live port directly instead of trusting the status banner.
2. Check which process/container owns the port (`podman ps`, `lsof -iTCP:<port> -sTCP:LISTEN`).
3. If the port is occupied by another stack, move the app to a free port rather than fighting the existing service.
4. Update every derived artifact in one change set:
   - source config (`.ai-dev/config.json`)
   - generated config (`litellm_config.yaml`)
   - runtime entrypoint (`mlx/entrypoint.sh`)
   - container metadata (`mlx/Dockerfile`)
   - tests that assert the endpoint/port
   - user docs that mention the default port
5. Re-run the stack and verify both:
   - the managed status command reports the new endpoint
   - the endpoint actually returns JSON from `/v1/models`

Example from this repo: 8081 was already owned by another stack, so the host MLX defaults were moved to 8082 and verified end-to-end.