---
name: llm-provider-routing
description: "Class-level workflow for LLM provider routing, auth handoffs, model identity checks, and OpenAI-compatible local proxy debugging."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [llm-providers, provider-routing, auth, oauth, api-key, openai-compatible, local-llm, litellm, model-catalogs, debugging]
    related_skills: [hermes-agent, claude-code, codex, opencode, local-llm-routing, serving-llms-vllm, llama-cpp]
    created_by: agent
---

# LLM Provider Routing

Use this umbrella when the task involves proving or changing which LLM provider, credential source, model alias, endpoint, or OpenAI-compatible backend an agent/runtime is actually using.

This absorbs two narrower lanes: provider-auth handoffs and OpenAI-compatible local inference proxy debugging.

## Decide the lane first

1. **Auth handoff** — switching between API keys, OAuth/setup-token credentials, CLI-managed auth, or clearing stale credential precedence.
2. **Model/catalog routing** — resolving whether a model alias exists in a provider catalog, static fallback, live account discovery, or local integration route.
3. **OpenAI-compatible local proxy** — a public `/v1` alias is forwarded through LiteLLM or another router to a backend such as `mlx_lm.server`, vLLM, llama.cpp, Ollama, or a custom service.
4. **Mixed provider migration** — separate credentials, model identity, endpoint mapping, and smoke tests; do not change all at once.

## Core principle

Separate four contracts that are often conflated:

- **Credential source**: environment variable, keychain/OAuth store, CLI setup token, config file, or secret manager.
- **Public client alias**: the name clients call (`default`, `fast`, `local-mlx`, curated provider slug).
- **Provider/catalog identity**: the canonical model id and account-specific limits exposed by the provider.
- **Backend serving id/path**: the id/path the actual serving backend accepts (`models/local-mlx`, a HF repo id, a GGUF path, or an artifact path).

A routing fix is complete only when each boundary is verified independently and a tiny generation request succeeds on the exact path the user will use.

## Lane A: auth handoffs

Use when moving between credential modes or making one credential source supersede another.

1. Identify the canonical auth source for the target provider or CLI.
2. Prefer refreshable or managed credentials over static environment tokens when supported.
3. Clear or unset older auth variables that have higher precedence than the new source.
4. Persist the selected credential only in the documented secret store or env file.
5. Run a tiny smoke test that exercises the exact runtime/provider path.
6. Confirm the provider/auth method from output, debug logs, or error details—not just that the command exits cleanly.

### Claude Code CLI inside Hermes

- Treat Claude Code CLI auth as a separate CLI transport/delegation lane, not Anthropic API auth.
- Verify installed CLI/help before designing adapters. Baseline: `claude setup-token` and `CLAUDE_CODE_OAUTH_TOKEN`.
- For headless execution, prefer `claude -p` with structured output, trusted cwd, no session persistence, explicit permission/tool allowlists, bounded time/output/concurrency, and process-group cancellation.
- Never use `--bare` for this path; it skips OAuth/keychain reads and expects API-key-style auth.
- Build a sanitized child environment; reject or clear shadowing `ANTHROPIC_API_KEY`/`ANTHROPIC_AUTH_TOKEN`; never put tokens in argv; redact logs and artifacts.

## Lane B: model identity and catalog routing

1. Query the static configured catalog and the live provider catalog separately.
2. Compare canonical slug, context window, max output, modalities, tools, reasoning controls, pricing, moderation, request limits, and rate limits where available.
3. Treat local manifests, cached metadata, and live/account-specific discovery as separate evidence classes.
4. Do not silently substitute a model name because it looks similar; prove alias-to-canonical routing.
5. If no benchmark or smoke test is available, state uncertainty and recommend workload-based evaluation rather than inventing a ranking.

## Lane C: OpenAI-compatible local inference proxy debugging

Use when a local LLM stack exposes an OpenAI-compatible API through a proxy/router.

1. Capture the exact error surface.
   - Classify 401/403 auth, 404 model lookup, 429 cooldown/no deployment, 5xx backend failure, timeout, or malformed response.
2. Probe each layer separately.
   - GET backend `/v1/models` if available.
   - GET proxy `/v1/models` with auth.
   - POST a tiny direct backend chat/completion using the backend-advertised id.
   - POST the same tiny request through the proxy using the public alias.
3. Compare model id/path at each boundary.
   - If direct backend succeeds with an artifact path but proxy fails with a public alias, mapping is wrong.
   - If logs show a local alias being treated as a Hugging Face repo, the backend probably received the alias instead of its accepted id/path.
   - If the proxy returns “no deployments available,” check whether an earlier 404/5xx put the deployment into cooldown.
4. Patch the source of truth, not just generated runtime config.
   - Update config defaults, generated runtime config when checked in, and tests asserting rendered backend mapping.
5. Restart the config-consuming process and rerun the exact red probe.

## Tiny probe discipline

Use minimal prompts and small token limits while debugging routing. You are testing connectivity and mapping, not generation quality.

Common probes:
- GET backend `/v1/models`
- GET proxy `/v1/models` with auth header
- POST backend `/v1/chat/completions` or `/v1/completions` with `max_tokens <= 3`
- POST proxy using the public alias and `max_tokens <= 3`

## Pitfalls

- Environment variables often beat credential files; a stale env token can hide valid OAuth or setup-token credentials.
- Browser OAuth and CLI-issued setup tokens are different flows.
- A successful login flow is not enough if runtime precedence still selects an older token.
- `/v1/models` ids are not necessarily interchangeable between proxy and backend.
- Do not forward a friendly alias to a backend that expects a path or upstream model id.
- Do not claim health from `/v1/models` alone; verify one tiny generation request.
- Do not hard-code one-machine absolute paths in reusable defaults when relative artifact paths work.

## Support files

- `references/provider-auth-handoffs.md` — preserved auth handoff and Claude Code details.
- `references/openai-compatible-local-inference.md` — preserved local proxy routing workflow and LiteLLM/MLX pattern.
