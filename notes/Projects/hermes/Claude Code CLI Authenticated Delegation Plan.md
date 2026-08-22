---
project_id: hermes
note_type: plan
updated_at: 2026-07-10T08:03:57Z
status: proposed
---
# Plan: Claude Code CLI transport using Claude Code OAuth auth

## Goal

Add a bounded Hermes delegation method that invokes the installed Claude Code CLI using Claude Code authentication, without calling Hermes's Anthropic SDK/API path.

## Phase 1 — Contract and safety gate

- Confirm the Claude plan/account and automated-use policy.
- Define the child-process contract: prompt/input, cwd, model hint, permission mode, allowed tools, output format, timeout, cancellation, and error categories.
- Make auth precedence explicit: accept the Claude Code credential store or `CLAUDE_CODE_OAUTH_TOKEN`; reject or clear `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, and unrelated API-key variables for this lane.
- Prohibit `--bare`, token command-line arguments, token logging, and raw stderr propagation.

## Phase 2 — Minimal transport

- Extend `tools/delegate_tool.py` through its existing `_build_child_agent()`, `delegate_task()`, and `_resolve_delegation_credentials()` seams with an opt-in external CLI backend; add `agent/external_cli_client.py` or a narrowly scoped `agent/claude_code_client.py` adjacent to the existing `agent/copilot_acp_client.py` precedent.
- Invoke `claude -p` with structured output, explicit permission/tool restrictions, `--no-session-persistence`, and a trusted cwd.
- Parse final JSON and newline-delimited `stream-json` events, including system initialization, retry, partial, tool, and terminal-result events; never treat partial events as final text.
- Bound stdin/prompt size, stdout/stderr bytes, wall-clock time, concurrent children, and process-group teardown. Keep the documented piped-stdin limit as an explicit guardrail.
- Return a Hermes-native result/error object with redacted diagnostics and provenance fields.

## Phase 3 — Hermes integration

- Expose the lane as an opt-in delegation backend without changing the default Hermes backend or `model.provider` behavior.
- Add config through `hermes_cli/config.py` and the delegation block for command path, timeout, output cap, max concurrency, allowed tools, and default permission mode; keep credentials out of config.
- Add CLI/diagnostic visibility that reports configured auth source class, never token material.
- Document installation, `claude setup-token`, environment precedence, and the no-API-key guarantee.
- Document that this is a local single-user adapter and not a multi-user Claude.ai credential broker; record the applicable account/plan and legal/compliance decision.

## Phase 4 — Verification

- Use a fake `claude` executable for deterministic unit tests.
- Test success, malformed JSON, nonzero exit, timeout, cancellation, output overflow, missing CLI, missing OAuth token, API-key shadowing, and token redaction.
- Run a live sentinel smoke test only when the user already has a valid Claude Code auth source; do not automate token creation or print the token.
- Compare the new lane against the existing Anthropic adapter to prove no Anthropic SDK/API call occurs.
- Run existing auth-precedence, `copilot-acp`, delegation, and credential-pool regression tests; record the tested Claude Code version and known version-sensitive flags.

## Closeout evidence

- Unit and integration tests pass with the fake CLI.
- A real opt-in smoke test returns a sentinel result through `claude -p` using Claude Code auth and records no credential material.
- `claude --version`, auth-source diagnostics, exact command construction, timeout/cancellation behavior, and output parsing are documented.
- Security review confirms no token in argv, logs, telemetry, error strings, or backlog artifacts.
- Existing Hermes provider and delegation tests pass; default provider behavior is unchanged.
- Research note and Hermes project index link to the implementation, test, and policy evidence.
