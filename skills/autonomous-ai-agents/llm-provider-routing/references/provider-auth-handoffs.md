# Provider Auth Handoffs (absorbed note)

Preserved details from the former `provider-auth-handoffs` skill.

## Standard workflow
1. Identify the canonical auth source for the target provider or CLI.
2. Prefer refreshable or managed credentials over static env tokens when supported.
3. Clear or unset older auth variables that have higher precedence than the new source.
4. Persist the chosen credential in the documented secret store or env file.
5. Run a tiny smoke test to confirm the runtime selected the intended path.
6. If a login flow prints a token in terminal output, treat that as sensitive source-of-truth material and store it only where the provider documents.

## Claude Code CLI inside Hermes
- Do not pass a Claude Code OAuth token into Hermes's Anthropic Messages API adapter and call that equivalent to Claude Code.
- Verify live CLI help before designing adapters. Baseline: `claude setup-token` followed by `CLAUDE_CODE_OAUTH_TOKEN`.
- Use `claude -p` with structured `json` or `stream-json` output, trusted cwd, `--no-session-persistence`, allowlists, time/output/concurrency bounds, and process-group cancellation.
- Never use `--bare` for OAuth/keychain auth.
- Sanitize child environments and redact logs/backlog artifacts.
- Start with fake-CLI fixture tests for success, malformed output, missing auth/CLI, nonzero exit, timeout/cancel, output overflow, and no Anthropic SDK/API call. Add a real smoke test only when valid Claude Code auth already exists.

## Model identity note
Provider handoffs are not complete until the selected model is checked against provider-specific catalog and endpoint. Report static catalog entries, cached metadata, and live/account-specific discovery separately.
