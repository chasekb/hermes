---
project_id: hermes
note_type: operator-guide
updated_at: 2026-08-26T00:00:00Z
status: tested
---
# Claude Code CLI delegation operator guide

This is a local, single-user, opt-in delegation lane. It launches the installed
Claude Code executable; it does not route through Hermes's Anthropic SDK/API
provider and it is not a multi-user Claude.ai credential broker.

## Installation and compatibility check

Install Claude Code using Anthropic's supported installer or Homebrew, then
check the executable and the version before enabling the lane:

```text
claude --version
claude -p --help
claude setup-token --help
```

The tested release is Claude Code **2.1.246**. CLI flags are version-sensitive;
the compatibility contract currently requires `-p` with an empty prompt value,
`--output-format stream-json`, `--verbose`, `--include-partial-messages`,
`--no-session-persistence`, `--permission-mode dontAsk`, `--allowedTools`, and
`--max-turns`. If the installed CLI rejects that contract, stop and upgrade or
reassess the adapter. Do not use `--bare`: it bypasses the managed OAuth/keychain
credential path.

## Two opt-in gates

Both settings are required; defaults remain safe and unchanged:

```yaml
delegation:
  backend: claude-code-cli
  claude_code:
    enabled: true
    cwd_roots: ["/absolute/path/to/trusted/project"]
```

`delegation.backend: claude-code-cli` selects the backend and
`delegation.claude_code.enabled: true` enables it. A non-empty `cwd_roots`
allowlist is also required. Prompts are piped on stdin, never placed in argv.
The child has an explicit tool allowlist and bounded turns, bytes, concurrency,
and wall-clock time. Existing security controls reject duplicate or unsafe CLI
flags and strip API/cloud-provider overrides from the child environment.

## Authentication and account policy

Authentication is either Claude Code's managed credential store/keychain or an
already-created `CLAUDE_CODE_OAUTH_TOKEN` from `claude setup-token`. An API-key
helper or API-key environment variable is not accepted for this lane. If both
sources are present, `CLAUDE_CODE_OAUTH_TOKEN` is the selected source (after
rejecting API-key helper configuration); the child environment also removes
API-key variables so they cannot take precedence inside Claude Code.

The setup-token flow requires an eligible Claude Pro, Max, Team, or Enterprise
account and is inference-only. Eligibility and automated-use/account policy
remain the operator's responsibility; this adapter does not expand plan
entitlements or make a policy determination.

## Results, usage, and failures

Only a terminal `result` event can produce a completed result. Partial assistant
events are progress only; a clean exit without a terminal result is a
`protocol_error`. Nonzero exit, malformed output, timeout, cancellation, input
or output limits, missing executable, and unavailable authentication are
reported as failures without exposing prompt, token, or raw stderr content.

Claude Code usage and cost fields are `reported` only when a trusted source is
available. Values emitted by the CLI are labeled **unverified**; missing values
are **unavailable**. Do not treat either as billing truth or as evidence that
usage was zero.

## Rollback

Disable the lane and restore the default backend, then restart the affected
Hermes process:

```yaml
delegation:
  backend: hermes
  claude_code:
    enabled: false
```

Rollback requires no credential migration or deletion. If compatibility or
security validation fails, leave both gates disabled, restore `backend: hermes`,
and retain the existing Hermes/Copilot paths. Never print, persist, or paste a
credential while diagnosing this integration.

## References

- [[Claude Code CLI Auth Handoff for Hermes]] — source review and protocol notes.
- [[Claude Code CLI Authenticated Delegation Plan]] — implementation and closeout evidence.
- https://code.claude.com/docs/en/authentication
- https://code.claude.com/docs/en/headless