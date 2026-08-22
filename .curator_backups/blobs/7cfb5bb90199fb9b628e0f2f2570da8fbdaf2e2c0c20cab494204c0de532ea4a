# tmux port-conflict and stack-restart note

Session pattern:
- A tmux-attached compose stack failed because a VPN gateway container (`gluetun`) was publishing host port 53 while a child DNS service (`pihole`) also needed DNS on 53.
- The earliest real error in the captured pane was `dnsmasq: failed to create listening socket for port 53: Address in use`.
- The gateway container was healthy enough to expose its own DNS (`[::]:53`) once the conflicting host bind was removed.

What worked:
1. Capture the live tmux pane first and anchor on the first explicit error.
2. Inspect the active compose file inside the host directory that actually owns the container, not the first directory you happen to be in.
3. Remove the conflicting host 53 bindings from the gateway compose file.
4. Reintroduce internal DNS routing explicitly when needed, e.g. `DNS_ADDRESS=127.0.0.1` so the VPN container points at its in-network DNS listener.
5. Restart with `docker-compose up -d` and verify with `docker-compose ps` plus `docker-compose logs` until the service becomes healthy.

Useful verification commands:
- `docker-compose ps`
- `docker-compose logs --tail 50 <service>`
- `docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'`

Pitfall:
- A compose stack can look “up” but still be functionally broken if the healthcheck depends on DNS reaching itself. After removing a port conflict, re-check health transitions rather than stopping at container start.
