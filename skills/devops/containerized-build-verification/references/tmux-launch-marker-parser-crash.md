# tmux launch-marker parser crash triage

Session note:
- When a containerized service exits in a tmux pane, anchor the capture on the last exact launch command or sentinel (for example `podman-compose up`) and read forward from there.
- In the market repo, the pane showed the last line before exit 139 as `S&P 500 page fetched (... bytes). Parsing...`.
- That pointed to the HTML parsing path, not the fetch layer or container wiring.

Useful pattern:
1. Capture the pane from the last launch marker, not from the top of scrollback.
2. Identify the first explicit application log line before the crash.
3. Reproduce the suspect parsing path with a tiny standalone harness against a real captured input file.
4. Confirm the harness on the live input before editing container config.
5. After the code change, rerun the exact harness and recheck the tmux pane to prove the crash window is gone.

This is especially helpful for parser bugs that surface only after a successful network fetch, because the container logs can make the fetch look healthy while the actual fault is in the next step.