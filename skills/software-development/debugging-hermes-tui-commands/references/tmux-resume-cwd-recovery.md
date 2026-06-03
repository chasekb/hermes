# tmux resume cwd recovery

Use this when a Hermes TUI pane is still open but the current working directory is stale or missing, and launching `hermes` or `hermes --resume` errors before the UI can start.

Recovery recipe:
1. Inspect the pane context with `tmux list-panes -a -F '#S:#I.#P #{pane_current_path} #{pane_pid}'`.
2. If the pane path is missing, moved, or invalid, send a command that first changes into a live directory, then prints it:
   - `cd /Users/bernardchase/.hermes && pwd`
3. If the shell prompt has already captured a partial command, clear the line before sending the fix. In tmux, `C-u` is a fast way to wipe the current input line.
4. Re-run the Hermes command from the repaired cwd:
   - `hermes --resume <session_id>`
5. Re-capture the pane after the relaunch to confirm the session resumed normally.

Notes:
- Prefer an absolute path for the recovery `cd` target so the fix works even if the pane started in a deleted project directory.
- If a pane keeps re-opening in the wrong place, the launch wrapper or tmux session startup command may need to be updated, but the immediate recovery step is always the same: re-establish a valid cwd before restarting Hermes.
- Avoid trying to diagnose Hermes startup itself until the shell has a valid cwd again; many pre-UI failures are just shell state, not Hermes command bugs.