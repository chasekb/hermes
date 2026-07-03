# Long-running compose build capture

Session note: when capturing a tmux pane from a launch marker, the useful window may still be an active `podman-compose build` with little or no recent output. Treat silence as inconclusive until the process tree and local images are checked.

## What worked

- Anchor the capture at the latest exact occurrence of the launch marker, not at the top of scrollback.
- Check the live process state before assuming a stall:
  - `ps -o pid,ppid,etime,pcpu,pmem,command -p <compose-pid>`
  - inspect child `podman build` / `podman-compose` PIDs if present
- Confirm completed services by inspecting local images:
  - `podman images --format '{{.Repository}}:{{.Tag}}\t{{.ID}}' | grep '<service>:<tag>'`
- Expect mixed progress in multi-service builds: one image can finish and tag successfully while another service is still compiling dependencies.

## Triage rule

If the compose process is still alive and child build output shows dependency installation progress, do not call the build hung. Continue from the current tail and identify the first real failure only when a command exits non-zero or the log shows an explicit error boundary.
