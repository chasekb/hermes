# tmux pane + remote container port-conflict notes

Session pattern:
- A tmux pane showed an SSH shell to a Synology DiskStation.
- The visible failure was not in the shell itself; it was a containerized DNS stack on the remote host.
- The useful clue came from capturing the live pane, not from the top of its scrollback.

Observed failure window:
- Pi-hole started logging: `dnsmasq: failed to create listening socket for port 53: Address in use`
- `docker ps` on the remote host showed a `gluetun` container exposing `53/tcp` and `53/udp`.
- `docker exec gluetun netstat -ltnp` showed `:::53` owned by `gluetun-entrypoint` inside the shared namespace.
- `docker exec pihole netstat -ltnp` showed Pi-hole also trying to bind `:53`, confirming the conflict.
- `docker inspect gluetun` showed the compose stack publishing 53 on the host and sharing the gluetun network namespace.

Useful commands:
- `tmux ls`
- `tmux list-panes -a -F '#{session_name}:#{window_index}.#{pane_index} #{pane_title} #{pane_current_command}'`
- `tmux capture-pane -t <session>:<window>.<pane> -p -S -80`
- `docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'`
- `docker inspect <container> --format '{{json .HostConfig.PortBindings}}'`
- `docker exec <container> sh -lc 'netstat -ltnp; ps -ef'`

Fix direction that emerged:
- Remove the host 53 bindings from the gluetun compose stack, then restart the stack so Pi-hole can own DNS port 53 as intended.
- Re-capture the pane after the change to confirm the bind error disappears.
