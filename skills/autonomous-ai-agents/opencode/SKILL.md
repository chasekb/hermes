---
name: opencode
description: "Delegate coding to OpenCode CLI (setup, auth, feature work, PR review)."
version: 1.3.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Coding-Agent, OpenCode, Autonomous, Refactoring, Code-Review, CLI]
    related_skills: [claude-code, codex, hermes-agent, coding-agent-tools]
---

# OpenCode CLI

Use OpenCode as an autonomous coding worker orchestrated by Hermes terminal/process tools.

## When to use
- The user explicitly asks for OpenCode
- You want an external coding agent to implement, refactor, or review code
- You need long-running coding sessions with progress checks
- You want to run parallel tasks in isolated workdirs or worktrees

## Core commands
- `opencode run '...'` for one-shot tasks
- `opencode` for interactive TUI sessions
- `opencode providers list` to inspect configured credentials
- `opencode providers login` to add credentials
- `opencode agent list` and `opencode agent create` for agent definitions
- `opencode models [provider]` to inspect available models
- `opencode debug config` and `opencode debug info` for troubleshooting
- `opencode.jsonc` is the persistent config file under `~/.config/opencode/`
- `opencode models opencode` is the quickest way to refresh the current free-model shortlist before pinning one

## Prerequisites
- OpenCode installed on the host
- A git repository for code tasks is strongly preferred
- Use `pty=true` for interactive TUI or login flows
- Use `opencode run` when a one-shot check is enough

## Authentication patterns
- OpenCode provider auth is managed through `opencode providers login`
- `opencode providers list` is the quickest way to confirm what is already configured
- If the provider named `opencode` asks for an API key, that is the OpenCode-specific auth path, not a model-provider fallback
- If a login flow points to `https://opencode.ai/auth`, follow that flow and paste the resulting key/token into the CLI prompt
- If the auth flow redirects into GitHub/Google, complete the browser sign-in there and then return to the CLI prompt
- Do not assume a different provider credential proves OpenCode-specific access

See `references/authentication.md` for the login-flow checklist and smoke-test notes.

## One-shot workflow
1. Verify the binary and credentials with `opencode --help` / `opencode providers list`.
2. Prefer `opencode run` for bounded tasks.
3. Attach files with `-f` when context matters.
4. Force a model with `--model provider/model` only when necessary.
5. For persistence, set the root-level `model` key in `~/.config/opencode/opencode.jsonc`.
6. When choosing a free default, refresh with `opencode models opencode` and then pin the current best `provider/model` in config.
7. Verify the diff and tests yourself before telling the user it worked.

## Interactive workflow
1. Start `opencode` in a repo with `pty=true`.
2. If running in the background, monitor with `process(action="poll"|"log")`.
3. Answer prompts with `process(action="submit")`.
4. Exit with Ctrl+C or `process(action="kill")`.

## Pitfalls
- Interactive `opencode` sessions need a PTY.
- `opencode run` is the preferred automation path for small tasks.
- PATH mismatches can point Hermes at a different OpenCode binary than the shell uses.
- Verify provider auth with `opencode providers list` before blaming the model or prompt.
- Keep each OpenCode session scoped to one repo or worktree.
- If you want a stable default model, pin it in `~/.config/opencode/opencode.jsonc` instead of relying on the last CLI flag.
- The OpenCode auth flow may start in a browser and hand back to the CLI; that round trip is expected.

## Verification
A minimal smoke test is:
- `opencode run 'Respond with exactly: OPENCODE_SMOKE_OK'`
- Success means the command exits cleanly and returns the exact marker

## PR review workflow
- Use a temporary clone or a dedicated worktree for review tasks
- Prefer `opencode run` for brief diffs and `opencode pr <number>` for GitHub PR checkout/review flows

## Rules
1. Prefer `opencode run` for one-shot automation.
2. Use PTY-backed interactive sessions only when iteration is needed.
3. Always scope OpenCode work to a single repo/workdir.
4. Verify provider state before launching long tasks.
5. Report concrete outcomes: files changed, tests run, remaining risks.
