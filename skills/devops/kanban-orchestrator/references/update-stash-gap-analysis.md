# Update stash vs pre-update backup gap analysis

Session-derived notes for Hermes update recovery tasks.

## What the previous update stashed
The update preserved local git working-tree changes before pulling. The best evidence came from update logs and the recovery path, not from the stash object itself (which was no longer addressable later).

Paths implicated in the conflict/recovery flow:
- `agent/auxiliary_client.py`
- `agent/codex_runtime.py`
- `agent/conversation_loop.py`
- `tests/run_agent/test_run_agent_codex_responses.py`

A separate file was restored cleanly during the process:
- `tests/agent/test_auxiliary_client.py`

## Two different safety layers
Do not conflate these:
1. Git stash used to protect in-flight repo changes during `hermes update`.
2. Pre-update `HERMES_HOME` snapshot controlled by `updates.pre_update_backup` / `--backup`.

The snapshot captured unrelated runtime state, including:
- `state.db`
- `config.yaml`
- `.env`
- `auth.json`
- `cron/jobs.json`
- `processes.json`

## Recovery behavior observed
- Update logs explicitly said the stashed changes were preserved and the working tree was reset to clean state.
- Conflict restore is conservative: if reapplying the stash conflicts, Hermes preserves the stash, prints conflicted files, and resets to a clean worktree so Hermes remains runnable.
- Cleanup guidance points users back to `git stash list` / `git stash drop` for manual resolution.

## Gap analysis
Core wiring looks sound; the main gaps are discoverability and traceability:
- No dedicated Hermes command yet to surface the saved stash ref, conflicted files, and recommended recovery steps.
- Update docs and CLI docs do not clearly cross-link the stash-conflict runbook from the primary update flow.
- Once the stash ref is no longer reachable as a git object, the exact diff is hard to recover from the user-facing path.

## Rewiring candidates if the flow is improved later
- Add a small Hermes helper that prints recovery metadata after update failures.
- Print a one-line pointer to the stash recovery runbook from the conflict path.
- Cross-link update docs, CLI docs, and the recovery reference so operators can move from the log to the fix path without hunting.
