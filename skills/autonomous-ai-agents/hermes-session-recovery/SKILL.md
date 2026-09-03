---
name: hermes-session-recovery
description: "Use after host restarts to safely resume Hermes workflows."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, sessions, tmux, reboot-recovery, remote-operations, workflow-resume]
    category: autonomous-ai-agents
---

# Hermes Session Recovery

## When to Use

Use this skill after a host reboot, SSH interruption, stale terminal, or tmux
reconnect may have disrupted a Hermes workflow and the correct session/pane must
be identified and resumed safely.

Use this skill when a machine reboot, host outage, SSH interruption, or stale
terminal may have disrupted one or more Hermes workflows. The goal is to
identify the affected workflow from evidence, preserve unfinished work, and
resume only the correct Hermes session in the correct tmux pane.

This is a recovery workflow, not a generic session-cleanup workflow. Do not
archive, delete, rename, or prune sessions while recovering them unless the
user explicitly asks for that separate mutation.

## Core procedure

1. Establish the target host and access path.
   - Inspect the local tmux layout first.
   - If the workflow is remote, use the user-authorized SSH/Tailscale path.
   - Treat non-interactive SSH shells as having a different PATH from an
     interactive tmux shell; prefer absolute Hermes executable paths when the
     command is not found.

2. Determine the actual reboot boundary.
   - On Linux, use `date --iso-8601=seconds`, `who -b`, `last -x reboot shutdown`,
     and, when available, `journalctl --list-boots --no-pager`.
   - Record the timezone explicitly. Hermes SQLite timestamps are epoch values;
     render them in the host's local timezone before comparing them with
     `last` or journal output.
   - Do not infer the reboot time from tmux pane age alone.

3. Inventory live tmux panes without changing state.
   - Capture pane IDs, current commands, titles, working directories, and pane
     PIDs with a format such as:
     `tmux list-panes -a -F '#S:#I.#P cmd=#{pane_current_command} title=#{pane_title} path=#{pane_current_path} pid=#{pane_pid}'`
   - Capture the likely Hermes panes, plus nearby project panes, before sending
     keys.
   - Map a pane PID to its child process; the tmux `pane_pid` is often the shell,
     not the Hermes Python child.

4. Review Hermes sessions around the reboot.
   - Use `hermes sessions list` when available; otherwise query the canonical
     `$HERMES_HOME/state.db` read-only with Python `sqlite3`.
   - The useful `sessions` fields are `id`, `title`, `source`, `started_at`,
     `ended_at`, `end_reason`, `message_count`, `tool_call_count`, `cwd`,
     `git_branch`, and `last_activity_at`.
   - Filter sessions whose activity overlaps the pre-reboot window, then inspect
     their recent user/assistant messages. A title alone is not enough to
     identify the impacted workflow.
   - Search message content for the domain workflow terms, project name, board
     name, or explicit task identifiers. This distinguishes a quantitative,
     trading, deployment, or coding workflow from unrelated Hermes activity.

5. Choose a resume candidate conservatively.
   - Prefer the exact session whose recent conversation created or advanced the
     affected workflow.
   - Check whether its final state was idle, completed, blocked, or actively
     executing a side effect.
   - Never kill or resume over an actively running worker merely because its
     title looks relevant. If state is ambiguous, report the candidate and ask
     before interrupting it.
   - Preserve safety boundaries from the recovered conversation. For example,
     a quantitative-trader workflow may be research/read-only and explicitly
     gated; resuming it must not activate live trading or account mutation.

6. Restart only an idle or safely closable Hermes pane.
   - Send `/exit` and wait until the pane returns to its shell.
   - Resume the exact session ID, preferably with the absolute executable when
     using a non-interactive remote shell:
     `/home/<user>/.hermes/hermes-agent/venv/bin/hermes --resume <SESSION_ID>`
   - Do not send a new task automatically just because the resumed prompt shows
     a historical draft or suggested input. A prompt line is not proof that a
     new request has been submitted.

7. Verify the recovery.
   - Confirm the pane's current command is the Hermes process, identify its child
     PID and start time, and capture the pane footer/title.
   - Confirm the resumed session ID and workflow-specific historical state are
     visible.
   - Report the reboot boundary, candidate sessions reviewed, selected session,
     pane, and verification result. Mention blockers or safety gates rather than
     claiming the workflow is complete.

## Remote and PATH pitfalls

- Tailscale SSH may print an authentication-check URL even while executing the
  command. Do not treat that banner as proof that the remote command failed;
  inspect the command's actual output and exit status.
- A remote non-interactive shell may lack the interactive PATH containing
  `hermes`. Use the venv path under `$HERMES_HOME/hermes-agent/venv/bin/hermes`
  or source the same shell initialization used by the tmux pane.
- `hostname` may be unavailable in a restricted PATH; `date`, `who -b`, `last`,
  and journal output can still establish the reboot boundary.
- Use local-time conversion with the host timezone when comparing SQLite epoch
  values to `last` output. Mixing UTC-rendered SQLite times with CDT/PDT reboot
  times can make a session appear to span or miss the reboot incorrectly.

## Workflow-specific safety

For trading or quantitative workflows:

- Treat “quantitative-trader” profile creation and workflow migration as a
  gated design/research task unless the recovered session explicitly documents
  a separate approved live-execution gate.
- Preserve read-only database boundaries, human approval requirements, and
  fail-closed behavior found in the session history.
- Do not start data collection, order submission, account mutation, or live
  execution as part of recovery unless the user explicitly requests that exact
  action and the required gates are already satisfied.

## Supporting reference

See `references/reboot-recovery-evidence.md` for the compact evidence recipe,
SQLite query shape, and tmux verification checklist used for this recovery
class.

## Verification checklist

- [ ] Reboot time and timezone established from host evidence.
- [ ] Relevant tmux panes captured before mutation.
- [ ] Candidate sessions selected from state metadata and recent messages.
- [ ] Workflow-specific session identity verified, not guessed from title.
- [ ] Only an idle/safely closable pane was restarted.
- [ ] Exact session ID resumed.
- [ ] Pane process and recovered workflow state verified afterward.
- [ ] No live-trading or other side effect was introduced during recovery.
