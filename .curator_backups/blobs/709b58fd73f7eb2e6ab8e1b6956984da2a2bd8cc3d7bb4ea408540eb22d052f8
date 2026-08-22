# Transformer runtime package activation failure

Session note for the trade repo’s containerized ML build/verify path.

## Failure pattern

A trained transformer package completed training and packaging, then failed during activation/reload with:
- `cannot create std::vector larger than max_size()`
- `No usable ONNX models found in <package dir>`
- `Trained package '<name>' created but could not be activated; keeping current active model`

The key clue was that the ONNX artifact itself was valid, but the packaged runtime copy still failed to load.

## What mattered

- The packaged runtime needed both `transformer.onnx` and `transformer_config.json`.
- The runtime contract depended on the config metadata (`lookback`, `n_features`, `input_layout`) matching the loader’s expectations.
- A CI smoke test that only exercised the lower-level ONNX export path missed the config/metadata sidecar entirely.
- The smoke test needed to call the higher-level packaging helper used in production so the generated config file existed.

## Useful verification steps

1. Capture the tmux pane from the last launch marker, not from the top of the session.
2. Confirm training actually finished and the failure happened during package activation/reload.
3. Inspect the packaged directory contents, not just the source export.
4. If activation fails, compare the packaged config/metadata against the loader’s expectations before blaming the ONNX graph.
5. After a bad package is identified, remove or quarantine the invalid trained-model directory so later reloads do not keep rediscovering it.

## CI linkage lesson

When the smoke test started calling `ModelTrainer::export_transformer_artifact(...)`, the test target also had to link the implementation files it now depended on:
- `src/ml/ModelTrainer.cpp`
- `src/ml/DataCollector.cpp`
- `src/ml/Metrics.cpp`

A link-time failure here is a test-target wiring problem, not an app-model bug.

## GitHub Actions verification lesson

For the merge-to-`dev` verification loop:
- verify the workflow run by `headSha`, not just by branch name
- if a normal PR merge path fails because the branches diverged, merge via the GitHub API and then verify the `dev` run on the merge commit
- do not report success until the top-level run is complete and every required job is green

## Related skill pointer

See `containerized-build-verification` for the general CI/build verification workflow and `systematic-debugging` for the broader root-cause method.
