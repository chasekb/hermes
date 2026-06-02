# CPU hotspot triage on macOS + Podman

Use this when the machine is "slow" or `top` shows a runaway CPU process.

## First-pass checklist

1. Identify the top consumer from the host:
   - `ps -Ao pid,ppid,%cpu,%mem,command | sort -k3 -nr | head -n 15`
   - `top -l 1 -o cpu -stats pid,command,cpu,mem | head -n 25`
2. If the top process is `com.apple.Virtualization.VirtualMachine` or another Apple Virtualization framework binary, suspect Podman’s VM rather than a single app process.
3. Correlate the VM with Podman state:
   - `podman machine list`
   - `podman stats --no-stream`
   - `podman ps --format '{{.Names}}\t{{.Image}}\t{{.Status}}'`
4. Check container logs for maintenance work:
   - PostgreSQL checkpoints / WAL churn
   - reindexing / migrations
   - database health loops
5. If container CLIs inside the container are minimal, prefer host-side `podman logs` and `podman stats` over in-container process inspection.

## Common interpretation

- Very high CPU in the VM with low container CPU often means the VM is servicing disk I/O, checkpoints, or other host-backed storage work.
- A healthy-looking container may still be driving host CPU indirectly through logs, sync work, or storage churn.
- On macOS, the VM PID often hides the underlying workload; the fix usually comes from finding the noisy container or the disk-heavy maintenance job.
- If the VM is hot but container CPU looks low, inspect inside the Podman machine for emulated builds:
  - `podman machine ssh <name> 'ps -eo pid,ppid,pcpu,pmem,args --sort=-pcpu | head -n 25'`
  - Look for `qemu-x86_64-static`, `cc1plus`, `buildah`, `cmake`, `ninja`, or `podman-compose` jobs.
  - In that case, the spike is often a cross-arch compile workload (for example, vcpkg/protobuf) rather than a runtime service.
