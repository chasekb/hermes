---
name: tmux-remote-container-triage
description: Debug remote hosts, SSH shells, and containerized services by capturing tmux panes, locating the live failure window, and tracing the owning process or port binding before making the smallest safe fix.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [tmux, ssh, docker, containers, remote-debugging, port-conflicts, logs]
---

# tmux Remote Container Triage

Use this skill when a problem is happening in a remote SSH shell, inside tmux, or in a containerized service on another machine, and you need to capture the live failure window before diagnosing the cause.

## When to use

- The user points to a tmux pane, SSH shell, or remote terminal session.
- The live problem is a container or service startup failure, healthcheck loop, or port conflict.
- The issue is noisy and the useful clue is buried in scrollback.
- You need to identify which process, container, or compose service owns a port.
- The fix is likely in a compose file, service config, or port mapping rather than in application code.

## Core workflow

1. Identify the exact tmux target first.
   - Run `tmux ls` and `tmux list-panes -a` before capturing.
   - Confirm the session, window, and pane you are about to inspect.
2. Capture the live window from the relevant pane.
   - Prefer `tmux capture-pane -t <session>:<window>.<pane> -p -S -N`.
   - Anchor on the last clear marker, not on early boot noise.
3. Read the log for the error boundary.
   - Look for the first repeated failure, the port claim, the DNS/healthcheck failure, or the stack trace root cause.
4. Determine the scope of ownership.
   - If it is a host port conflict, inspect the host container bindings.
   - If it is namespace-shared, inspect the container that owns the shared network namespace.
   - If it is an SSH shell, confirm whether the remote host or a container on that host is the real owner.
5. Verify with process/port inspection.
   - `docker ps --format ...`
   - `docker inspect <container>`
   - `docker exec <container> ... netstat|ss|ps`
6. Make the smallest safe fix.
   - Remove or change the conflicting port mapping.
   - Adjust service upstreams or internal DNS settings when the conflict is actually a dependency wiring issue.
   - If the live stack uses pulled images rather than bind mounts, rebuild or republish the image before expecting source edits to appear.
   - Avoid broad restarts until you know which component owns the failure.
7. Re-capture and verify.
   - Re-open the same pane and confirm the error is gone.
   - Re-run the port/healthcheck inspection after the change.
   - For frontend/backend stacks, smoke-test the exact API routes the UI is calling before calling the fix done.

## Pitfalls

- Capturing from the top of scrollback and narrating stale boot noise instead of the live failure window.
- Assuming the last line in the pane is the root cause.
- For long-running compose builds, treating a quiet pane as a hang before checking the active process tree and completed local images.
- Forgetting that multiple containers can share a network namespace and therefore compete for the same apparent port.
- Editing the wrong stack because the pane is SSHed into a remote host that runs its own compose project.
- Treat a healthcheck loop as the root cause when it is often a symptom of a lower-level port, DNS, or network binding issue.
- Assuming a container failure is always caused by the local checkout; if the service is running a pulled dev image, source edits will not appear until the image is rebuilt/published and re-pulled.
- In image-backed compose stacks, confirm the resolved `image:` values from `podman-compose config` before debugging app code. If the defaults point at a registry or `localhost/...`, `up --no-build` may try to pull instead of reusing a local build.
- In image-backed compose stacks, check whether the repo is bind-mounted before trying to validate a source edit from the live pane.
- When a frontend is proxying to a backend and the pane shows `ECONNRESET` / `socket hang up`, inspect the backend route contract next; missing compatibility endpoints can look like transport failures.
- Making an invasive change before proving which service owns the port.

## Reference files

- `references/trade-compose-dev-image-fallback.md` — trade-repo notes on live tmux pane capture, image-backed compose stacks, and the asset-fallback path.
- `references/trade-compose-local-image-tags.md` — capture of the stale `localhost/...` image-tag failure and the local-tag/build-context fix used to make `podman-compose up --no-build` work again.
- `references/long-running-compose-build-capture.md` — the long-running Podman/compose capture pattern when the pane is still actively building but temporarily quiet.

## Verification

A good triage result should answer all of these:

- Which tmux pane/session/window contained the live failure?
- What was the first meaningful error in the live window?
- Which process/container owned the conflicting resource?
- What exact config change is the smallest fix?
- How do you know the change worked?

## Support files

- `references/tmux-pane-port-conflict-synology.md` — session-style notes and a concrete Synology/Docker port-53 conflict example.
- `references/trade-compose-frontend-contracts.md` — trade-repo notes on image-backed compose stacks, frontend API compatibility routes, and when source edits require a rebuild.
