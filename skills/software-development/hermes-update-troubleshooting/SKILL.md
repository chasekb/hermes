---
name: hermes-update-troubleshooting
description: "Troubleshoot Hermes update failures."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, update, troubleshooting, git, authentication, verification]
    related_skills: [hermes-agent, software-development-workflows, systematic-debugging, github-auth]
    created_by: agent
---

# Hermes Update Troubleshooting

Use this class-level workflow when `hermes update` fails, reports unexpected output, or appears to update successfully but leaves the runtime or verification path unhealthy.

## When to Use

Use when `hermes update` fails, a tmux pane shows update errors, Git transport/authentication blocks an update, or an update needs post-install verification.

## Core principle

Separate the operation into four independently verifiable boundaries: capture the exact failure, verify repository transport/authentication, run the update without discarding local work, and verify the installed runtime and test interpreter. Do not jump directly to reinstalling or changing application source code.

## Workflow

### 1. Capture the exact failure

- Capture the requested tmux pane or terminal output before interpreting it.
- Locate the last `hermes update` invocation and inspect the following output first.
- Preserve the complete capture outside the chat if it is large; report the exact failing command and first meaningful error line.
- Treat plugin-hook context and update output as separate evidence streams.

### 2. Inspect both Git checkouts

Hermes installations can involve both the Hermes home/repository where the command is run and the installed `hermes-agent` source checkout used by the entry point. For each checkout, inspect `git remote -v`, branch/status, and remote reachability; do not assume they share a remote or authentication mode.

For GitHub SSH authentication failures:

1. Check `gh auth status` without printing tokens.
2. If GitHub CLI is authenticated, run `gh auth setup-git`.
3. Prefer authenticated HTTPS GitHub remotes when SSH keys are unavailable.
4. Verify each affected checkout with `git ls-remote origin HEAD`.
5. Retry `hermes update --check` before the full update.

If `gh` is not authenticated, stop at the auth boundary and ask the user to authenticate. Never guess credentials or put tokens into remote URLs.

### 3. Run the update safely

- Check for local changes before choosing backup/stash options.
- Preserve user-authored changes; do not reset, clean, or delete them for convenience.
- Use supported Hermes CLI flags rather than manually pulling and reinstalling.
- If the checkout is dirty, inspect status and diff after Hermes stashes/restores changes.
- Use `--no-backup` only when explicitly accepted and a safe recovery path is understood.
- Treat dependency sync, UI build, skill sync, and gateway restart as separate success signals.

### 4. Repair and verify gateway service lifecycle

When the update warning or pane shows gateway startup/restart trouble, treat the service manager as a separate boundary from the Python process:

1. Inspect `hermes gateway status`, `launchctl print gui/$(id -u)/ai.hermes.gateway` on macOS, or the corresponding systemd unit, plus the newest `logs/gateway.log` and `logs/gateway.error.log` lines.
2. Compare the service's complete `ProgramArguments`/`ExecStart` with the current CLI parser. A generated supervisor-only flag that the live entry point rejects causes an immediate crash loop even when foreground `hermes gateway run` works.
3. Refresh the definition with `hermes gateway install` (use `--force` only when the normal repair path does not rewrite it), then explicitly run `hermes gateway start`.
4. Verify both the manager state and the child process; a successful start command is insufficient if launchd/systemd reports a nonzero last exit or the logs show an argparse error.
5. If a platform is being retried without usable credentials, either configure its secret or set that platform's `enabled: false` in `config.yaml` before restarting; do not leave a known-unconfigured adapter in a retry loop.

Do not delete update markers or declare the fleet current until a newly started gateway has stamped current runtime identity and the service manager reports it healthy.

### 5. Verify with the right interpreter

Run `hermes update --check`, `hermes doctor`, and the repository's targeted tests using its managed interpreter or test runner. Do not infer a product regression from `python -m pytest` until confirming that `python` points at the intended environment and pytest is installed there. Distinguish missing test tooling, missing runtime dependencies, and real source/test failures after collection succeeds. Record the exact interpreter path and command when verification is blocked.

### 5. Keep uv, the runtime venv, and dev tooling distinct

Hermes updates its own managed uv at `$HERMES_HOME/bin/uv`; this may differ from the first `uv` found on the shell PATH. Use the managed binary for repository operations. The normal update synchronizes runtime dependencies but does not necessarily install the optional `[dev]` extra, so pytest may be absent even when Hermes itself is healthy. For development verification, install the declared extra into the actual Hermes venv rather than using an unrelated system interpreter:

```bash
$HERMES_HOME/bin/uv sync --locked --python "$HERMES_HOME/hermes-agent/venv/bin/python"
$HERMES_HOME/bin/uv pip install --python "$HERMES_HOME/hermes-agent/venv/bin/python" -e '.[dev]'
```

Use this as a deliberate development step (or a future opt-in `hermes update --dev` workflow), not as an unconditional production-install default. See `references/hermes-uv-and-venv-maintenance.md` for the validated rationale and checks.

## Failure classification

- `Permission denied (publickey)` → GitHub SSH transport/auth boundary.
- `Authentication failed` or `could not read Username` → HTTPS credential boundary.
- Network/DNS errors → connectivity boundary.
- Build/dependency errors after fetch → update installation boundary.
- Gateway restart errors → service lifecycle boundary.
- Test import/collection errors → test environment boundary until proven otherwise.

## Verification checklist

- [ ] Exact pane/terminal output captured.
- [ ] Failure isolated to a specific boundary.
- [ ] Both relevant checkout remotes inspected.
- [ ] Git access verified with `git ls-remote`.
- [ ] Update completed without discarding user changes.
- [ ] Post-update status/diff inspected.
- [ ] `hermes update --check` is current.
- [ ] `hermes doctor` passes or warnings are classified.
- [ ] Tests used the intended interpreter, or the blocker is explicit.

## Pitfalls

- Do not modify application source code to fix Git authentication.
- Do not assume `origin` in one checkout controls the other.
- Do not expose tokens from `gh auth status`, credential helpers, `.env`, or remote URLs.
- Do not call tests broken until dependency presence and interpreter selection are checked.
- Do not overwrite or discard a dirty working tree merely to make update output clean.

## Support files

- `references/hermes-update-auth-and-verification.md` — concise command sequence, evidence fields, and boundary classification for update incidents.
