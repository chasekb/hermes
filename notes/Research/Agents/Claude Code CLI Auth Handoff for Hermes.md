---
project_id: hermes
note_type: research-report
updated_at: 2026-07-10T08:03:57Z
status: implementation-gated
---
# Claude Code CLI authentication handoff for Hermes

## Question

Can Hermes add a bounded method to invoke the Claude Code CLI using a Claude Code OAuth/setup token, without routing the lane through Hermes's Anthropic Messages API adapter or an Anthropic API key?

## Verified evidence

- Claude Code's official authentication documentation says `claude setup-token` creates a one-year OAuth token for scripts/CI, prints it once, and expects it in `CLAUDE_CODE_OAUTH_TOKEN`. The token requires a Pro, Max, Team, or Enterprise plan and is inference-only. Source: https://code.claude.com/docs/en/authentication
- The same documentation lists authentication precedence and warns that `ANTHROPIC_API_KEY` takes precedence over `CLAUDE_CODE_OAUTH_TOKEN`; the Hermes child environment must therefore clear or reject API-key variables for this lane. Source: https://code.claude.com/docs/en/authentication
- Official headless-mode documentation supports `claude -p`, structured `json` or newline-delimited `stream-json`, `--allowedTools`, `--permission-mode`, `--no-session-persistence`, and `--max-turns`. Source: https://code.claude.com/docs/en/headless
- Official documentation explicitly says `--bare` skips OAuth and keychain reads and requires `ANTHROPIC_API_KEY` or `apiKeyHelper`; the proposed lane must not use `--bare`. Source: https://code.claude.com/docs/en/headless
- The installed CLI was verified locally as Claude Code `2.1.206`. `claude -p --help` exposes the required print, structured-output, permission, directory, timeout-related, and session flags; `claude setup-token --help` confirms the setup-token flow.

## Hermes current state

- Hermes already resolves `CLAUDE_CODE_OAUTH_TOKEN` and Claude Code credential files in `agent/anthropic_adapter.py`, but that code constructs an Anthropic Messages API client. This is credential reuse, not a Claude Code CLI transport.
- Hermes already has a subprocess/structured-protocol precedent in `agent/copilot_acp_client.py`; it resolves a child command, builds a sanitized child environment, streams JSON-RPC, bounds timeouts, and converts process output into Hermes-compatible results.
- Provider profiles are declarative and discovered through `providers/__init__.py` and `providers/base.py`. A CLI transport may need a dedicated runtime branch or a provider plugin, but must remain distinct from `api_mode=anthropic_messages`.
- Existing reference guidance is in `skills/autonomous-ai-agents/provider-auth-handoffs/references/claude-code-hermes.md`.

## Recommended boundary

Implement a separate, opt-in `claude-code-cli` delegation lane for bounded coding/research tasks. Do not replace Hermes's primary model provider in the first slice. Hermes should launch `claude -p` with an explicit trusted working directory, an explicit permission/tool allowlist, bounded output, cancellation, and no session persistence. The child should inherit the Claude Code credential source without Hermes printing, persisting, or passing the token as a command-line argument.

## Open gates

- Confirm the intended Claude subscription and account policy permits the planned automated use before enabling live execution.
- Decide whether the first transport returns final JSON only or supports `stream-json`; prefer stream parsing if Hermes needs cancellation/progress.
- Define whether Claude Code's native tools are the capability boundary or whether Hermes must translate tool calls; the first slice should avoid a broad tool-call translation layer.
- Run the delegated research synthesis and record its source URLs, implementation recommendation, and security caveats here before accepting the backlog item.

## Delegated multi-agent synthesis

Three independent research lanes completed on 2026-07-10:

1. Official-auth lane: confirmed `claude setup-token`, the one-year `CLAUDE_CODE_OAUTH_TOKEN` script/CI surface, headless `claude -p`, structured output, the `--bare` OAuth incompatibility, credential expiry risk, and the legal/compliance caveat. Sources: https://code.claude.com/docs/en/authentication, https://code.claude.com/docs/en/headless, https://code.claude.com/docs/en/cli-reference, https://code.claude.com/docs/en/legal-and-compliance. Confidence is high for documented behavior; account-specific billing and authorization remain to be confirmed.

2. Hermes-runtime lane: identified `tools/delegate_tool.py` (`_build_child_agent`, `delegate_task`, `_resolve_delegation_credentials`), `hermes_cli/auth.py` (`ProviderConfig`, provider registry, external-process credential resolution), `hermes_cli/runtime_provider.py` (provider resolution and the `copilot-acp` branch), `hermes_cli/config.py` (delegation defaults), `agent/copilot_acp_client.py` (subprocess precedent), and `agent/anthropic_adapter.py` (current Claude Code credential-to-Anthropic-API path). Recommendation: add a Claude Code delegation backend or generic external CLI client rather than a first-class inference provider.

3. Security/operations lane: recommended a local single-user subprocess wrapper with child-only environment handling, stdin prompt delivery, separate stdout/stderr, explicit cwd/tool permissions, `stream-json` parsing, parent-owned wall-clock timeout and process-tree cleanup, bounded concurrency, fake-CLI tests, and an opt-in live smoke test. Explicit non-goals are multi-user credential brokering, direct Anthropic API fallback, arbitrary cwd/MCP/plugin injection, unrestricted permissions, durable session orchestration, and high-concurrency scheduling. Sources: https://code.claude.com/docs/en/agent-sdk/hosting and https://code.claude.com/docs/en/agent-sdk/streaming-output.

## Decision after research

Keep `HERMES-BL-20009` proposed and implementation-gated. The smallest defensible slice is an opt-in external-process backend behind the existing delegation machinery, preserving the current Hermes backend as default. Do not make Claude Code OAuth a general Hermes provider or multi-user service without an explicit Anthropic policy/account decision.
