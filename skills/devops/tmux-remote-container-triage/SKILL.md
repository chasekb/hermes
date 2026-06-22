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
   - Avoid broad restarts until you know which component owns the failure.
7. Re-capture and verify.
   - Re-open the same pane and confirm the error is gone.
   - Re-run the port/healthcheck inspection after the change.

## Pitfalls

- Capturing from the top of scrollback and narrating stale boot noise instead of the live failure window.
- Assuming the last line in the pane is the root cause.
- Forgetting that multiple containers can share a network namespace and therefore compete for the same apparent port.
- Editing the wrong stack because the pane is SSHed into a remote host that runs its own compose project.
- Treating a healthcheck loop as the root cause when it is often a symptom of a lower-level port, DNS, or network binding issue.
- Making an invasive change before proving which service owns the port.

## Verification

A good triage result should answer all of these:

- Which tmux pane/session/window contained the live failure?
- What was the first meaningful error in the live window?
- Which process/container owned the conflicting resource?
- What exact config change is the smallest fix?
- How do you know the change worked?

## Support files

- `references/tmux-pane-port-conflict-synology.md` — session-style notes and a concrete Synology/Docker port-53 conflict example.
