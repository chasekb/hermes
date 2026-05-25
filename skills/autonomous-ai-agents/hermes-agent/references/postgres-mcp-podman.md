# Postgres MCP wired to running Podman databases

Use this pattern when the machine already has Postgres containers running under Podman and you want Hermes MCP to attach to them without hardcoding secrets in `config.yaml`.

## Pattern

1. Discover the running containers and host ports:
   - `podman ps --format '{{.Names}}\t{{.Ports}}'`
   - `podman inspect <container> --format '{{range .Config.Env}}{{println .}}{{end}}'`
2. Prefer a `bash -lc` wrapper in `mcp_servers.<name>.command/args`.
3. In the wrapper:
   - `set -a`
   - `source <project>/.env`
   - export `DB_HOST=localhost`
   - export the correct `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`
   - set `DB_SSL_MODE=disable`
   - set `DB_READ_ONLY=true` when the server should be query-only
   - `exec npx -y mcp-postgres@latest`
4. Keep credentials out of the Hermes config file; source them at runtime from the project `.env`.
5. Test each configured server with `hermes mcp test <name>`.

## Useful mapping example

- `db-postgres` → `localhost:5433`
- `trade_db_1` → `localhost:5432`
- `cohida-db-prod` → `localhost:5435`

## Pitfalls

- `mcp-postgres@latest` can fail immediately with a generic `Connection closed` if the password is wrong or the host/port is off by one.
- Do not assume a single `postgres` MCP server is enough when multiple containers are running; create one MCP entry per database target so tool names and connection settings stay clear.
- If a container is reachable only from the host port mapping, point MCP at `localhost:<mapped-port>`, not the container DNS name.
