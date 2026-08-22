# Podman Compose provider routing on macOS

Session-derived pattern for local stack failures where `podman compose` delegates to an unexpected external provider.

## Symptom pattern

A CLI command that internally runs `podman compose ...` may print an external-provider banner such as:

```text
>>>> Executing external compose provider "/opt/homebrew/bin/docker-compose" ... <<<<
failed to connect to the docker API at unix:///.../podman/<machine>.sock: connect: no such file or directory
```

This usually means the failure is not in the compose YAML or app service. The failing boundary is provider selection/socket routing.

## Fast investigation steps

1. Capture the exact command output first; do not assume `podman compose` and `podman-compose` behave identically.
2. Check provider/tool split:
   - `command -v podman`
   - `command -v podman-compose`
   - `command -v docker-compose`
   - `podman compose version`
   - `podman-compose -f podman-compose.yml ps`
3. Check active Podman machine/socket state:
   - `podman machine list`
   - `podman system connection list`
   - `podman info --format '{{.Host.RemoteSocket.Path}}'`
4. If direct `podman-compose -f ...` succeeds but `podman compose -f ...` fails, fix command resolution to prefer direct `podman-compose` when present and keep `podman compose` as fallback.
5. Add focused regression tests that stub command discovery so both provider paths are covered.
6. If the compose file emits `version is obsolete`, remove the top-level `version` key from the canonical compose file and rely on the Compose spec.

## Verification loop

After the fix, run both code-level and runtime-level checks when available:

- Unit test for command selection.
- Template/runtime parity if templates mirror compose files.
- Full relevant test suite.
- `podman-compose -f podman-compose.yml config`.
- The user-facing CLI command that failed, e.g. `ai-dev up` and `ai-dev status`.

## Pitfall

Do not capture this as "Podman compose is broken" or "Docker Compose is unusable." The durable lesson is to identify which provider/socket boundary is failing and route to the provider that uses the active Podman connection.