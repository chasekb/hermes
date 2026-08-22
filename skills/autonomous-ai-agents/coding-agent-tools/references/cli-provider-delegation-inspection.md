# CLI-Backed Provider / Delegation Inspection

Use this reference before proposing a Hermes integration for Claude Code, Codex, Copilot, or another coding-agent CLI.

## Inspection checklist

1. **Provider abstraction**
   - Locate the provider registry/profile type.
   - Record provider aliases, auth type, transport/API mode, base URL, and model catalog hooks.
2. **Runtime routing**
   - Trace explicit provider → config → environment → auto resolution.
   - Identify the authoritative runtime resolver and any legacy helper with different precedence.
3. **Auth boundaries**
   - Record API-key, OAuth, credential-file, and CLI-managed sources separately.
   - Never read credentials into an audit report; report only source names and precedence.
4. **Subprocess lane**
   - Find command/args precedence, executable lookup, inherited environment, cwd, stdin/stdout/stderr, timeout, cancellation, and termination escalation.
   - Check whether output is a stable inference protocol or an autonomous-agent protocol.
5. **Delegation integration**
   - Inspect child construction, provider/model overrides, role/depth limits, concurrency, timeout, result schema, memory hooks, and cost/observability rollup.
6. **Config and tests**
   - Inspect defaults plus the live config example.
   - If tests are unavailable in the checkout, say so and propose fake-executable tests rather than inferring support from filenames.

## Architecture decision rule

Prefer a **delegation backend** when the external CLI owns tools, permissions, sessions, and workspace execution. A first-class Hermes provider is appropriate only when the CLI exposes a stable request/response protocol that can be represented by the existing client abstraction. Otherwise, a provider implementation grows into a second agent runtime: prompt serialization, tool-call parsing, session lifecycle, cancellation, permission handling, model selection, and client construction all become required surfaces.

For a delegation backend, preserve the existing child result contract (`task_index`, `status`, `summary`, `duration_seconds`, `error`) and make the backend explicit in config. Keep the current Hermes child-agent path as the default and isolate the external subprocess adapter behind one module.

## Hermes-specific comparison pattern

The existing Copilot ACP implementation is the reference external-process path:

- Registry: `hermes_cli/auth.py::PROVIDER_REGISTRY["copilot-acp"]`
- Profile: `plugins/model-providers/copilot-acp/__init__.py`
- Runtime branch: `hermes_cli/runtime_provider.py::resolve_runtime_provider`
- Client: `agent/copilot_acp_client.py::CopilotACPClient`
- Client construction: `agent/agent_runtime_helpers.py::create_openai_client`
- Child transport overrides: `tools/delegate_tool.py::_build_child_agent`

Claude Code currently belongs to the native Anthropic auth path rather than a distinct CLI provider:

- Provider entry: `hermes_cli/auth.py::PROVIDER_REGISTRY["anthropic"]`
- Runtime token resolver: `agent/anthropic_adapter.py::resolve_anthropic_token`
- Precedence: `ANTHROPIC_TOKEN` → `CLAUDE_CODE_OAUTH_TOKEN` → Claude Code credential files → `ANTHROPIC_API_KEY`

Do not conflate that auth integration with delegation through the `claude` executable. The former is API transport; the latter is an external autonomous runtime.

## Deterministic verification

Use a fake CLI executable for unit tests. Verify command and argument precedence, prompt delivery, stdout summary capture, stderr isolation, nonzero exit handling, timeout termination, cwd propagation, environment inheritance without secret logging, batch ordering, and preservation of the existing Hermes delegation path. Live CLI smoke tests should be short, bounded, and run only in a temporary workspace.
