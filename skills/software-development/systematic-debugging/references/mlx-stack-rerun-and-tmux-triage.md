# MLX stack rerun and tmux triage

Session-derived debugging notes for the mlx-stack repo.

## tmux / shell-context sanity check

When a tmux pane shows stale activation state or a CLI command is unexpectedly missing:

1. Inspect the active shell context first:
   - `echo VIRTUAL_ENV=$VIRTUAL_ENV`
   - `which python`
   - `which ai-dev`
2. If the shell is stale, reset it cleanly:
   - `deactivate`
   - `source .venv/bin/activate`
   - `hash -r`
3. Prefer explicit repo interpreter paths during verification:
   - `.venv/bin/python -c 'import mlx.core as mx; print(mx.__name__)'`
   - `.venv/bin/ai-dev --help`

## repeatable model-pull behavior

`ai-dev pull-models` should be rerunnable against already-populated local model directories.

- Existing populated output directories should be skipped, not treated as a hard failure.
- Empty output directories can be cleaned up and reused.
- Existing files at the output path are still a real collision and should fail loudly.
- Add a regression test that exercises the rerun path so local artifact commands remain idempotent.

## verification pattern

For local-stack troubleshooting, verify the three layers together:

- CLI invocation: the command exists in the repo venv
- artifact state: the expected output directory is present and in the intended shape
- live service state: the stack status command reflects the current process/endpoint health
