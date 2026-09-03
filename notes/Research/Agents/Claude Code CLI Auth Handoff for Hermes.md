---
project_id: hermes
note_type: research-report
updated_at: 2026-08-25T20:00:00Z
status: implementation-gated-policy-reviewed
---
# Claude Code CLI authentication handoff for Hermes

## Question

Can Hermes add a bounded method to invoke the Claude Code CLI using a Claude Code OAuth/setup token, without routing the lane through Hermes's Anthropic Messages API adapter or an Anthropic API key?

## Verified evidence

- Claude Code's official authentication documentation says `claude setup-token` creates a one-year OAuth token for scripts/CI, prints it once, and expects it in `CLAUDE_CODE_OAUTH_TOKEN`. The token requires a Pro, Max, Team, or Enterprise plan and is inference-only. Source: https://code.claude.com/docs/en/authentication
- The same documentation lists authentication precedence and warns that `ANTHROPIC_API_KEY` takes precedence over `CLAUDE_CODE_OAUTH_TOKEN`; the Hermes child environment must therefore clear or reject API-key variables for this lane. Source: https://code.claude.com/docs/en/authentication
- Official headless-mode documentation supports `claude -p`, structured `json` or newline-delimited `stream-json`, `--allowedTools`, `--permission-mode`, `--no-session-persistence`, and `--max-turns`. Source: https://code.claude.com/docs/en/headless
- Official documentation explicitly says `--bare` skips OAuth and keychain reads and requires `ANTHROPIC_API_KEY` or `apiKeyHelper`; the proposed lane must not use `--bare`. Source: https://code.claude.com/docs/en/headless
- The earlier handoff recorded Claude Code `2.1.206`; the current tested version is Claude Code `2.1.246` (`claude --version`). `claude -p --help` exposes the required print, structured-output, permission, directory, budget/turn, and session flags; `claude setup-token --help` confirms the setup-token flow. Flag availability is version-sensitive and must be probed or pinned by the implementer.

## Hermes current state

- Hermes already resolves `CLAUDE_CODE_OAUTH_TOKEN` and Claude Code credential files in `agent/anthropic_adapter.py`, but that code constructs an Anthropic Messages API client. This is credential reuse, not a Claude Code CLI transport.
- Hermes already has a subprocess/structured-protocol precedent in `agent/copilot_acp_client.py`; it resolves a child command, builds a sanitized child environment, streams JSON-RPC, bounds timeouts, and converts process output into Hermes-compatible results.
- Provider profiles are declarative and discovered through `providers/__init__.py` and `providers/base.py`. A CLI transport may need a dedicated runtime branch or a provider plugin, but must remain distinct from `api_mode=anthropic_messages`.
- Existing CLI orchestration guidance is in `skills/autonomous-ai-agents/claude-code/SKILL.md`; this research note adds the separate OAuth policy gate and external-process implementation contract.

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

## Policy gate and account decision (2026-08-25)

The approved design is **local, single-user, opt-in execution only**. The operator must use an unmodified, locally installed Claude Code binary and an account-owned credential: either the Claude Code-managed subscription credential store or a token already created by `claude setup-token` and supplied as `CLAUDE_CODE_OAUTH_TOKEN`. The setup-token path is documented for CI/scripts, creates a one-year OAuth token, requires Claude Pro, Max, Team, or Enterprise, and is inference-only: it can make model requests but cannot establish Remote Control sessions or fetch claude.ai connectors.[1]

The child environment must fail closed against credential shadowing. Before launch, remove/reject `ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_API_KEY`, `apiKeyHelper`-equivalent configuration, cloud-provider selectors, federation/profile selectors, and endpoint overrides for this lane. Current Claude Code precedence places bearer/API-key/helper sources above `CLAUDE_CODE_OAUTH_TOKEN`, and `-p` always uses `ANTHROPIC_API_KEY` when present; clearing those variables is therefore required, not merely preferred.[1][5] Within the allowed sources, `CLAUDE_CODE_OAUTH_TOKEN` wins over the stored `/login` subscription credential. If neither allowed source is present, Hermes returns `auth_unavailable` without spawning the child. The token is never placed in argv, config, logs, telemetry, prompts, or error strings.

This is not permission to route Hermes through the Anthropic SDK or Messages API. Hermes must launch the `claude` executable and parse its stdout; the external CLI may perform its own service call as Claude Code. The implementation must not import/call `anthropic`, `agent/anthropic_adapter.py`, or the native Hermes `anthropic_messages` provider for this backend, and must not fall back to `ANTHROPIC_API_KEY` or another direct API path.

The legal/compliance decision is conditional: a developer running Hermes locally for their own authorized account is the only first-slice target. Anthropic states that OAuth is for purchasers of Free/Pro/Max/Team/Enterprise subscription plans, while developers building products/services should use Console API keys or supported cloud credentials; it also prohibits third-party applications from offering Claude.ai login, routing Free/Pro/Max credentials on behalf of users, or collecting/storing/intermediating Claude.ai credentials.[4] Consequently, no shared token, credential pool, hosted/multi-user broker, resale, or end-user credential collection is allowed. Any product, hosted sandbox, or multi-user deployment requires a separate Anthropic commercial agreement and account-owner/legal approval before the feature can be enabled. The default remains disabled and the account/plan approval is an operational prerequisite, not something Hermes can infer.

## Delegated research synthesis

The three delegated lanes recorded in the prior handoff remain the evidence base, with the following implementation conclusions:

1. **Official-auth lane — high confidence for documented CLI behavior; medium confidence for account authorization.** It verified `claude setup-token`, the one-year `CLAUDE_CODE_OAUTH_TOKEN` script/CI surface, Pro/Max/Team/Enterprise scope, inference-only limitation, authentication precedence, non-interactive `-p`, structured output, and the OAuth-incompatible `--bare` mode.[1][2][3]

It also recorded token expiry and legal/compliance restrictions; account billing, organization policy, and whether a particular subscription permits this exact local automation remain operator/account-owner questions.[4][5]
2. **Hermes-runtime lane — high confidence from direct source inspection.** It traced `tools/delegate_tool.py::_build_child_agent`, `delegate_task`, `_resolve_delegation_credentials`, `hermes_cli/config_defaults.py::DEFAULT_CONFIG`, `hermes_cli/auth.py::ProviderConfig/PROVIDER_REGISTRY`, `hermes_cli/runtime_provider.py::resolve_runtime_provider`, `agent/copilot_acp_client.py::CopilotACPClient`, `agent/anthropic_adapter.py`, and the delegation tests. The recommendation is a backend branch/client behind delegation, not a first-class inference provider, because Claude Code owns tools, permissions, sessions, and workspace execution.
3. **Security/operations lane — high confidence for the control design; implementation-dependent until tested.** It recommended a local subprocess wrapper with child-only environment handling, stdin prompt delivery, separate stdout/stderr, trusted cwd validation, `stream-json` parsing, bounded output/concurrency, parent-owned deadline, process-tree cleanup, fake-CLI fixtures, and an opt-in live smoke test. Non-goals are API fallback, arbitrary cwd/MCP/plugin injection, unrestricted permissions, durable session orchestration, high-concurrency scheduling, multi-user brokering, and credential pooling.

## Exact Hermes seams inspected

| Area | Current symbol/path | Design implication |
|---|---|---|
| Child construction | `tools/delegate_tool.py:1606` `_build_child_agent`; `:1812-1848` validates/pins transport overrides | Add a separate external backend argument/client; do not reinterpret `override_provider` as Anthropic API routing. Preserve toolset intersection, leaf/orchestrator role, parent lineage, worktree option, and child identity. |
| Dispatch | `tools/delegate_tool.py:3625` `delegate_task`; `:3737-3797` resolves credentials, caps children, validates tasks; `:3878-3897` passes overrides | Add explicit backend selection before normal provider credential resolution. Empty/default backend must return the existing Hermes child path byte-for-byte. Model-supplied values cannot raise configured budgets. |
| Credential resolver | `tools/delegate_tool.py:4454` `_resolve_delegation_credentials`; `:4491-4535` direct endpoint and `:4549-4593` runtime-provider resolution | Do not send `claude-code-cli` through this API-key/provider resolver. Add a distinct result such as `{backend, command, args, auth_source, cwd}` with no secret value; reject API-key fallback. |
| Config defaults | `hermes_cli/config_defaults.py:1987-2049` `DEFAULT_CONFIG["delegation"]`; legacy mirror `cli.py:534-540` | Existing delegation is provider/model/base_url/api_key/api_mode plus iteration, timeout, concurrency, depth, and approval controls. Add the new nested CLI block without changing existing defaults or storing credentials. |
| Provider registry | `hermes_cli/auth.py:232-307` `ProviderConfig` and `PROVIDER_REGISTRY["copilot-acp"]` | `auth_type="external_process"` is the precedent, but Claude Code should remain a delegation backend because it is an autonomous CLI, not an OpenAI-compatible inference endpoint. |
| Runtime resolver | `hermes_cli/runtime_provider.py:106-155` URL/API-mode detection and `resolve_runtime_provider` | Explicitly bypass for the Claude CLI lane; otherwise `api.anthropic.com` and `/anthropic` resolve to `anthropic_messages`, which is forbidden for this backend. |
| Existing process precedent | `agent/copilot_acp_client.py:62-74` command/args resolution, `:156-165` child env, `:586-610` `Popen`, `:614-694` reader/timeout loop, `:742-780` event handling | Reuse the subprocess discipline, but use Claude's documented line-delimited JSON protocol rather than ACP JSON-RPC. Add process-group termination rather than relying on one-process kill. |
| Result contract | `tools/delegate_tool.py:2454-2468` `_run_single_child`; `:2860-2947` timeout entries; `:3111-3163` result/usage/cost shape; `:3252-3286` completion callback | Preserve `task_index`, `status`, `summary`, `api_calls`, `duration_seconds`, `model`, `exit_reason`, `truncated`, `tokens`, `tool_trace`, `cost_usd`, and `cost_status`; add backend-specific usage only as optional fields. |
| Event/durable delivery | `tools/delegate_tool.py:2700-2704` start/complete callbacks; `tools/async_delegation.py:147-166` durable schema and `:335-388` unknown-owner recovery | Emit lifecycle events compatible with existing callbacks and preserve `async_delegation` restart semantics. Never persist prompt, argv, stderr, or credentials. |
| Tests | `tests/tools/test_delegate.py`, `tests/tools/test_delegate_output_schema.py`, `tests/tools/test_async_delegation.py`, `tests/agent/test_codex_app_server_integration.py`, `tests/tools/test_local_setsid_descendant_sweep.py` | Add fake executable tests at the external-client boundary; retain existing delegation, provider/auth, ACP, credential-pool, timeout, and process-tree tests. |

## Implementation contract

### Configuration schema

Add this opt-in block under the existing `delegation` section. Names are a contract; credentials are deliberately absent:

```yaml
delegation:
  backend: hermes                 # default; existing behavior, never changed implicitly
  claude_code:
    enabled: false                # second gate; both backend and enabled are required
    command: claude                # executable name or absolute path; no shell
    args: []                       # non-security operator args, token-free
    cwd_roots: []                  # required absolute trusted project roots
    allowed_tools: [Read, Grep]    # explicit allowlist; no unrestricted default
    permission_mode: dontAsk       # version-checked safe default
    output_format: stream-json     # final `json` is the compatibility fallback
    max_turns: 20
    max_budget_usd: null
    timeout_seconds: 900
    input_max_bytes: 10485760       # never above Claude's documented 10 MiB stdin cap
    stdout_max_bytes: 8388608
    stderr_max_bytes: 65536
    max_concurrent: 1
    retry_limit: 0
    no_session_persistence: true
```

`backend: hermes` and `enabled: false` are both required defaults. `backend: claude-code-cli` selects the lane only when the second gate is true. `cwd_roots` must be non-empty for live execution; the parent/request cwd must resolve beneath one of those roots after symlink resolution, and a model/task may not supply or widen it. Worktree isolation may derive a child cwd only from a validated root. Reject root paths that are files, missing, outside the allowlist, or escape it through symlinks; do not accept arbitrary `--add-dir`, MCP, plugin, settings, or session paths from task text.

Command and argument precedence is deterministic: Hermes constructs `claude -p` plus mandatory safety/protocol flags; config `args` may add only an allowlisted, version-compatible flag set; per-task hints may select a model/effort only within configured ceilings. Reject duplicate/conflicting occurrences of `-p`, `--bare`, `--output-format`, `--verbose`, `--include-partial-messages`, `--no-session-persistence`, `--permission-mode`, `--allowedTools/--allowed-tools`, `--tools`, `--max-turns`, `--max-budget-usd`, `--resume/--continue`, `--cloud`, `--bg/--background`, and `--dangerously-skip-permissions` instead of relying on CLI last-flag-wins behavior. Hermes-generated safety flags are authoritative; no shell string parsing, `shell=True`, token-bearing argv, session resume, cloud dispatch, or background dispatch.

### Invocation and version-sensitive flags

The tested binary is Claude Code **2.1.246** (`claude --version`). Its help exposes `-p`, `--output-format {text,json,stream-json}`, `--verbose`, `--include-partial-messages`, `--no-session-persistence`, `--permission-mode`, `--allowedTools/--allowed-tools`, `--tools`, `--max-turns`, and `--max-budget-usd`; `claude setup-token --help` confirms the setup-token command. The current docs say `stream-json` partial output requires `--verbose` and `--include-partial-messages`, while the final line is a `result` event.[2][3]

The baseline argv is conceptually:

```text
[command, "-p", "", "--output-format", "stream-json", "--verbose",
 "--include-partial-messages", "--no-session-persistence",
 "--permission-mode", permission_mode, "--allowedTools", *allowed_tools,
 "--max-turns", str(max_turns), ...]
```

The prompt is delivered through stdin, bounded to `input_max_bytes`; the empty `-p` prompt is an implementation detail to keep user content out of argv. If the installed CLI rejects this form, fail closed and record a version-compatibility error; do not silently fall back to a different transport. `--bare` is explicitly prohibited because current Claude Code does not read OAuth credentials or the keychain in bare mode.[1][2] `--permission-mode manual` is the current compatibility alias for the interactive/default mode; use `dontAsk` with an explicit allowlist for unattended execution and record the tested flag set rather than assuming future aliases.[3]

### Output, result, and usage schema

Parse newline-delimited JSON one line at a time, enforcing the byte cap before decoding. Only a terminal `type: "result"` event can produce `summary`; partial text, assistant messages, and tool events are progress, never a final answer. Accept `subtype: success`, `error_max_turns`, `error_max_budget_usd`, and other documented/error subtypes without inventing success. Malformed lines are counted and retained only as redacted diagnostics; a missing terminal result is `protocol_error`.

The external client returns an internal record:

```json
{
  "backend": "claude-code-cli",
  "status": "completed|failed|timeout|cancelled|protocol_error|auth_unavailable",
  "summary": "terminal result text or null",
  "session_id": "optional, never resumed",
  "model": "optional",
  "exit_reason": "completed|error_max_turns|error_max_budget_usd|...",
  "usage": {
    "input_tokens": 0,
    "output_tokens": 0,
    "reasoning_tokens": null,
    "cache_read_tokens": null,
    "cache_creation_tokens": null,
    "source": "reported|unavailable|unverified"
  },
  "cost_usd": null,
  "cost_status": "reported|unavailable|unverified",
  "num_turns": null,
  "duration_seconds": 0.0,
  "malformed_event_count": 0
}
```

Map it into the existing parent result contract (`task_index`, `status`, `summary`, `api_calls`, `duration_seconds`, `model`, `exit_reason`, `truncated`, `tokens`, `tool_trace`, `cost_usd`, `cost_status`). Claude's JSON cost and per-model usage are client-side estimates, not billing truth; preserve them only when reported and label them `reported`/`unverified` rather than claiming actual spend.[2] If usage is absent, return zero/`null` plus `source: unavailable`, not a fabricated count. Never include raw stdout/stderr, prompt text, environment values, or token-looking strings in the result.

### Event schema

Normalize process and stream activity to the existing progress callback names (`subagent.start`, `subagent.complete`) and, for the external lane, a versioned metadata event:

```json
{
  "schema_version": 1,
  "type": "delegation_event",
  "event": "spawn_requested|process_started|system_init|partial|tool_use|api_retry|result|timeout|cancelled|process_exit|completed",
  "delegation_id": "opaque id",
  "subagent_id": "opaque id",
  "task_index": 0,
  "seq": 1,
  "status": "running|completed|failed|...",
  "model": "optional",
  "duration_seconds": 0.0,
  "usage": {"source": "reported|unavailable|unverified"},
  "bytes": {"stdin": 0, "stdout": 0, "stderr": 0}
}
```

`system/init` records capability/model/tool metadata; `system/api_retry` records attempt, max retries, delay, status/category; partial/tool events carry only bounded, redacted previews; `result` is the sole terminal summary source. Do not persist full event payloads to `state.db` or live logs. Durable async records retain routing/status/result only, consistent with `tools/async_delegation.py`; process paths are reduced to basename and cwd is represented by an allowlisted root identifier or hash.

### Limits, timeout, and cancellation

The first slice is intentionally conservative: one Claude child at a time (`max_concurrent: 1`), zero automatic retries, 20 agentic turns, optional $ budget, 15-minute parent wall clock, 10 MiB stdin ceiling matching the documented Claude Code pipe limit, 8 MiB stdout, 64 KiB stderr, and a 5-second post-result drain/cleanup grace. The configured values may be lower but not higher than hard safety ceilings without a separately reviewed change.[2]

Launch with `start_new_session=True` (or the platform equivalent), separate stdin/stdout/stderr pipes, and a child-only sanitized environment. On parent stop/cancel or deadline: close stdin, send SIGINT for graceful turn termination, wait up to 2 seconds, send SIGTERM to the whole process group, wait up to 3 seconds, then SIGKILL and reap descendants. Claude documents exit 143 and process-tree termination on SIGTERM; map this to `cancelled` when parent-requested and `timeout` when the Hermes deadline fired.[2] A timeout must return within the deadline plus the bounded grace, never wait on an abandoned thread, and must leave no orphaned Claude process. Do not retry after timeout/cancellation by default.

### Rollback and verification

Rollback is a configuration change first: set `delegation.backend: hermes` and `delegation.claude_code.enabled: false`, then restart only the affected Hermes process if necessary. No existing provider/auth schema or credential-pool entry is migrated. If the client is found unsafe, remove its dedicated module and its backend branch, delete only the new config keys, and retain the existing Hermes and Copilot ACP paths. Verification must include fake-CLI tests for auth shadowing, command/arg rejection, trusted cwd/symlink escape, stdin/stdout/stderr caps, JSON and stream fixtures (`system/init`, partial, tool, retry, result), malformed/nonzero output, timeout/cancel process-tree cleanup, concurrency, usage-unavailable reporting, and an assertion that the client never imports/calls the Anthropic SDK/API adapter. A live sentinel smoke test is optional and must run only with pre-existing valid Claude Code auth, in a temporary trusted workspace, without invoking `claude setup-token` or printing/copying the token.

## Sources

[1] https://code.claude.com/docs/en/authentication
[2] https://code.claude.com/docs/en/headless
[3] https://code.claude.com/docs/en/cli-reference
[4] https://code.claude.com/docs/en/legal-and-compliance
[5] https://code.claude.com/docs/en/env-vars
