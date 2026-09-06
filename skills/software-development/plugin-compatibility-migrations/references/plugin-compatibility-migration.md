# Plugin Compatibility Migration Reference

## Command sequence

From the Hermes home containing the active plugin tree:

```bash
tmux capture-pane -t <session:window.pane> -p -S -200
hermes plugins compat
```

From the canonical Hermes source checkout:

```bash
<venv>/bin/python - <<'PY'
import importlib
for name in [
    "<canonical replacement module>",
    "<touched plugin module>",
]:
    importlib.import_module(name)
    print(name, "OK")
PY

<venv>/bin/python scripts/check_compat_pointers.py
<venv>/bin/python -m compileall -q <touched plugin files>
hermes plugins compat
```

Use the actual interpreter and `PYTHONPATH` that Hermes uses. Do not run the smoke test from a parent directory whose stale package shadows the checkout.

## Source-root decision table

| Observation | Action |
|---|---|
| Replacement module exists in the runtime checkout and imports successfully | Update the plugin to the canonical module. |
| Replacement exists only in a nested checkout | Re-run with that checkout's virtualenv/source path; do not add a shim. |
| Replacement is absent from the runtime checkout | Stop and resolve the version/source mismatch before editing plugin code. |
| Static report is clean but plugin import fails | Treat it as an integration failure; inspect package roots, discovery order, and interpreter selection. |
| Plugin imports successfully but report still lists a hit | Search dynamic imports, attribute access, and duplicate plugin copies; then re-run discovery. |

## Scope rule

Patch only the reported external plugin references. Leave unrelated user-home state, credentials, generated reports, gateway processes, and working-tree changes untouched unless the user explicitly asks for them.
