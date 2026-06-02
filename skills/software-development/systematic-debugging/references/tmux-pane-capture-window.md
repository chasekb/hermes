# tmux pane capture window

Use this when a user asks for logs/screen output "since" a specific marker in a tmux pane.

Workflow
1. Identify the exact pane and anchor marker the user named.
2. Capture only the suffix starting at the last occurrence of that marker (or the last known-good command if the marker is a launch command).
3. Keep the window small enough to read end-to-end; do not mix in earlier boot noise if the failure happened later.
4. Preserve the exact command line, timestamps if available, and the first error line that changes the state of the pane.
5. If the marker appears multiple times, prefer the latest occurrence unless the user explicitly asks for the first.

Practical notes
- When the marker is a launch command like `TAG=dev podman-compose up --no-build`, treat it as the anchor for the next failure window.
- If the pane is long-lived, capture the span from the anchor to the current tail before interpreting errors.
- If the log output is truncated or interleaved, re-capture a smaller suffix rather than guessing from memory.
- Pair the captured window with nearby shell context: the exact command, cwd, and any env vars visible in the pane.
- Common mistake: reasoning from the top of the pane or from a previous run's output. The useful evidence is the suffix after the last anchor, not the entire scrollback.
