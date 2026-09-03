# Reboot-recovery evidence recipe

Use this as a compact, read-only evidence pass before restarting a Hermes pane.

## Host and tmux

```bash
date --iso-8601=seconds
who -b
last -x reboot shutdown | head -20
journalctl --list-boots --no-pager | head -10
tmux list-panes -a -F '#S:#I.#P cmd=#{pane_current_command} title=#{pane_title} path=#{pane_current_path} pid=#{pane_pid}'
tmux capture-pane -t <pane> -p -S -120
```

For a remote host, run these through the user-authorized Tailscale/SSH path and
record the host timezone. A restricted non-interactive PATH can make `hermes`
look unavailable even though the tmux shell has it.

## Session metadata query

The canonical database is `$HERMES_HOME/state.db`. The `sessions` table contains
session identity and lifecycle metadata; `messages` contains the conversation.
A useful read-only query shape is:

```python
import sqlite3
con = sqlite3.connect('/home/<user>/.hermes/state.db')
rows = con.execute('''
  select id, title, source, started_at, ended_at, end_reason,
         message_count, tool_call_count, cwd, git_branch, last_activity_at
  from sessions
  order by coalesce(last_activity_at, started_at) desc
''')
```

Convert epoch fields with the host timezone before comparing to `last` or
journal timestamps. Filter the reboot-adjacent window, then read the last
several user/assistant messages for each candidate. Search message content for
the actual project/workflow terms; titles can be generic or misleading.

## Safe resume and verification

1. Confirm the selected pane is idle or safely closable.
2. Send `/exit` and wait for the shell prompt.
3. Resume the exact session ID using the pane's Hermes executable, for example:
   `/home/<user>/.hermes/hermes-agent/venv/bin/hermes --resume <SESSION_ID>`
4. Verify the child process, start time, pane title/footer, session ID, and
   workflow-specific historical state.

Do not submit a new prompt merely because the resumed TUI displays a draft
suggestion. For quantitative/trading workflows, verify that read-only and
human-approval gates remain visible and that no live-execution action was
introduced by recovery.
