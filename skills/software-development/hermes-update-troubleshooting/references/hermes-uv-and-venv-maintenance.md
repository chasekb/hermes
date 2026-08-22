# Hermes uv and venv maintenance

## What `hermes update` owns

The update pipeline calls the managed-uv maintenance path during dependency refresh. Hermes's authoritative uv is `$HERMES_HOME/bin/uv`, not necessarily the first `uv` resolved from the interactive shell's `PATH`. The managed path is refreshed on a bounded cadence and then used to install/update Hermes runtime dependencies.

A source checkout can therefore be healthy while a shell-level `uv` is stale. Diagnose these separately:

```bash
command -v uv
uv --version
$HERMES_HOME/bin/uv --version
```

For repository operations, prefer the managed binary explicitly:

```bash
$HERMES_HOME/bin/uv sync --locked --python "$HERMES_HOME/hermes-agent/venv/bin/python"
```

## Runtime versus development environment

The normal Hermes update is intentionally runtime-oriented. The repository declares pytest and related tooling in the optional `dev` extra, so a normal application update may leave pytest absent while all production imports and `hermes doctor` pass.

Install development tooling into the same venv used by Hermes:

```bash
$HERMES_HOME/bin/uv pip install \
  --python "$HERMES_HOME/hermes-agent/venv/bin/python" \
  -e '.[dev]'
```

This keeps pytest, pytest-asyncio, ruff, ty, and debugpy aligned with the repository's pinned metadata instead of mixing a system pytest with Hermes's venv.

## Recommended operating model

- Normal user update: `hermes update`.
- Development update: `hermes update`, then the locked runtime sync and `-e '.[dev]'` install above.
- Future product improvement: add an explicit opt-in `hermes update --dev` mode that installs the dev extra and runs an import/pytest smoke check. Do not add dev dependencies to every normal install by default.
- If the managed uv and PATH uv differ, either use `$HERMES_HOME/bin/uv` explicitly or put `$HERMES_HOME/bin` before other uv locations in the shell PATH. Do not silently rewrite shell startup files during repository maintenance.

## Verification

```bash
$HERMES_HOME/bin/uv --version
"$HERMES_HOME/hermes-agent/venv/bin/python" -c 'import sys; print(sys.executable)'
"$HERMES_HOME/hermes-agent/venv/bin/python" -m pytest --version
"$HERMES_HOME/hermes-agent/venv/bin/python" -m pytest tests/hermes_cli/test_commands.py tests/hermes_cli/test_scan_venv_blockers.py -q -o addopts=''
hermes doctor
```

The targeted smoke test should prove that collection reaches actual tests. A full-suite failure after that must be classified separately from missing-tooling or wrong-interpreter errors.

## Pitfalls

- Do not use an old PATH uv against a newer `pyproject.toml` or `uv.lock` and conclude that the repository update is broken.
- Do not install pytest globally when the requested verification is for the Hermes checkout.
- Do not claim the full suite is healthy merely because pytest is installed; report real test failures separately.
- Do not make the optional dev extra part of the default production update without an explicit product decision.
