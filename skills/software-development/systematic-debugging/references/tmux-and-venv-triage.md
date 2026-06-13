# tmux capture + project venv triage

Use when debugging a long-lived tmux pane and the repo has a local `.venv`.

Captured pattern
- If the tmux command path contains shell metacharacters (for example `(` or `)`), invoke the capture from a simple parent cwd and `cd` into the target path inside the command string.
- Capture the failure window from the last useful launch marker rather than the full scrollback.

Python/uv venv mismatch pattern
- After `source .venv/bin/activate`, verify which interpreter is actually active with `which python`.
- If `python` still resolves to a shim outside the repo venv, use `.venv/bin/python` explicitly for imports, test runs, and one-shot checks.
- For editable installs into the repo venv, prefer:
  - `uv pip install --python .venv/bin/python -e '.[mlx-host]'`
- Verify with:
  - `.venv/bin/python -c 'import mlx.core as mx; print(mx.__name__)'`

Why this matters
- tmux captures often include older boot noise; anchoring to the current pane suffix prevents chasing stale errors.
- The active shell can lie about the interpreter after activation; explicitly targeting the repo interpreter avoids debugging the wrong environment.