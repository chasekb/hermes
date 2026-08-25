# archbtw Hermes machine configuration

This directory records the sanitized, declarative configuration for the `archbtw` machine.

It is intentionally not a copy of `/home/kahlil/.hermes`. Runtime state, credentials, profile
`.env` files, databases, caches, logs, session data, and generated artifacts remain local and
must not be committed.

## Lifecycle contract

- One user-level `hermes-gateway.service` is the gateway supervisor and profile multiplexer.
- No per-profile gateway services are installed or enabled.
- `engineering` is the Kanban orchestrator.
- Kanban workers are dispatched through the default gateway to named specialist profiles.
- Existing interactive CLI sessions are not terminated automatically during gateway maintenance.
- Gateway changes are applied through the external user service manager, never from inside a
  gateway worker.

## Applying the overlay

Review `config-overlay.yaml` against the installed Hermes schema before applying it. The overlay
contains only the values intentionally tuned on this machine; it is not a standalone config file.

The profile routing descriptions are recorded in `profiles.yaml` and should be synchronized with
local profile metadata without copying profile credentials.

## Verification contract

After applying changes, verify:

- `hermes config check` and `hermes doctor` pass.
- `systemctl --user is-enabled hermes-gateway.service` returns success.
- `systemctl --user is-active hermes-gateway.service` returns success.
- The service has `Restart=always` and the configured five-second restart delay.
- No `hermes-gateway-<profile>.service` units are installed.
- Kanban workers have known profile assignees and no duplicate gateway services are created.
