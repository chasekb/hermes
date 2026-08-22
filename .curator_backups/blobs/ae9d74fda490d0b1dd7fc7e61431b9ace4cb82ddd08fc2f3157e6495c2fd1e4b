---
name: subscription-provider-billing
description: "Verify CLI provider subscription versus API billing."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [provider-auth, billing, subscriptions, api-keys, oauth, claude-code, anthropic]
    related_skills: [llm-provider-routing, hermes-agent]
    created_by: agent
---

# Subscription Provider Billing

Use this skill when configuring a Hermes provider or external model CLI where the user requires usage to draw from a subscription account rather than from metered API billing.

## Core rule

A successful model request does not prove the billing route. Verify authentication mode, provider endpoint, environment-variable precedence, and the runtime credential resolver separately.

## Claude Code / Anthropic workflow

1. Run `claude auth status --json`.
2. Require `loggedIn: true`, `authMethod: "oauth_token"`, and `apiProvider: "firstParty"` for Claude-account subscription routing.
3. Check the shell environment and Hermes `.env` without printing values. `CLAUDE_CODE_OAUTH_TOKEN` should be present; `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, and `ANTHROPIC_TOKEN` should be unset.
4. Confirm the runtime resolves the OAuth credential, preferably with a non-secret boolean/type probe such as Hermes's `resolve_anthropic_token()` plus `_is_oauth_token()`.
5. Remember that Claude Code documentation says an API key overrides Pro/Max/Team/Enterprise subscription authentication, including in print mode. Remove or unset stale API-key variables before testing.
6. Treat first-party OAuth as proof of Claude-account subscription routing, not proof of the exact Pro versus Max tier. Verify that tier in the Claude account billing/settings UI when required.
7. Do not interpret CLI `total_cost_usd` telemetry as proof of API billing; it may be an estimated usage value even for subscription sessions.

## Hermes configuration guidance

- Keep the provider as native `anthropic` when using Hermes's Anthropic adapter with `CLAUDE_CODE_OAUTH_TOKEN`.
- Do not add an Anthropic API key to `config.yaml` or `.env` when subscription billing is required.
- After changing auth or provider configuration, restart Hermes so credential resolution and prompt/provider state are rebuilt.
- Verify the exact path used by the target workload, not only standalone `claude`.

## Verification checklist

- [ ] Claude CLI reports first-party OAuth authentication.
- [ ] No API-key environment variable overrides exist in the shell or Hermes `.env`.
- [ ] Hermes resolves an OAuth credential without exposing its value.
- [ ] The selected model is available through the authenticated first-party route.
- [ ] Exact Pro/Max tier is confirmed separately if the user requires it.

## Pitfalls

- `CLAUDE_CODE_OAUTH_TOKEN` and `ANTHROPIC_API_KEY` are not interchangeable billing modes.
- `authMethod: oauth_token` identifies OAuth/subscription routing but does not identify Pro versus Max.
- A printed token prefix, account identifier, or estimated cost must never be logged as a secret or treated as billing proof.
- A direct Claude CLI smoke test validates the CLI path; Hermes still needs its own resolver/environment check.

See `references/claude-subscription-billing.md` for the evidence pattern and commands used to validate this route.
