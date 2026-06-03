# MCP Health Checks and Failure Triage

Use this when the Hermes UI or logs suggest that MCP servers are failing.

## Fast triage

1. List configured servers:
   - `hermes mcp list`
2. Test a specific server:
   - `hermes mcp test <server>`
3. If one server fails, inspect its wrapper and environment variables in `~/.hermes/config.yaml` and `~/.hermes/.env`.
4. Reload or restart after changing config or env:
   - `/reload-mcp` in-session
   - restart Hermes for startup-time config changes

## Important pattern

A single unhealthy MCP server can make the UI look like "all MCP servers failed" even when most servers are healthy. Always verify servers individually before assuming a global outage.

## Log clues

Look for:
- `MCP server '<name>' is unreachable after 5 consecutive failures`
- `Failed to connect to MCP server '<name>'`
- startup registration lines such as `registered N tool(s)`

## Example: Brave Search

If Brave Search returns `SUBSCRIPTION_TOKEN_INVALID` or repeated failures:
- confirm the server has a valid `BRAVE_API_KEY` in the runtime environment
- re-test the server after fixing the key

Do not treat the presence of one failed server as proof that all MCP connections are broken.