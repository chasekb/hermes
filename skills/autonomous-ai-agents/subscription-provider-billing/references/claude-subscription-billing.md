# Claude subscription billing verification

Validated evidence pattern for Claude Code subscription routing:

- `claude auth status --json` should report `loggedIn: true`, `authMethod: "oauth_token"`, and `apiProvider: "firstParty"`.
- Check only presence, never values, for `CLAUDE_CODE_OAUTH_TOKEN`, `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, and `ANTHROPIC_TOKEN`.
- For subscription billing, the OAuth token should be present and the API-key variables should be unset. Anthropic documents that `ANTHROPIC_API_KEY` overrides subscription auth, including in print mode.
- Hermes can verify its own route with `resolve_anthropic_token()` and `_is_oauth_token()` while redacting the token.
- OAuth/first-party status proves Claude-account subscription routing, but not whether the account tier is Pro or Max. Confirm the exact tier in Claude account billing settings.
- A CLI `total_cost_usd` field is usage telemetry, not proof that the request was billed to an Anthropic API Console balance.
