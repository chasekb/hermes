# ONNX model activation/load triage

Session note: trade repo transformer packaging/activation failure after `TAG=dev podman-compose up --no-build`.

Observed failure window:
- training completed packaging and then reloaded models
- backend logged: `Skipping transformer model ... because it could not be loaded: cannot create std::vector larger than max_size()`
- followed by: `No usable ONNX models found in ...`
- package was created, but activation failed and the current model stayed active

What mattered:
- The checked-in `data/onnx/transformer.onnx` passed ONNX checker.
- The runtime failure happened in the copied packaged artifact under `data/trained_models/<package>/transformer.onnx`, not necessarily the source file.
- A valid ONNX file can still fail activation if the loader's metadata/layout assumptions disagree with the packaged config.

Triage pattern:
1. Compare the packaged `transformer.onnx` and `transformer_config.json` against the checked-in source artifact.
2. Verify tensor layout metadata (`input_layout`, channels-first/last) matches what the loader and inference path expect.
3. Treat `cannot create std::vector larger than max_size()` during ONNX session load as a load-path/shape-metadata problem first, not automatically as ONNX corruption.
4. When packaging succeeds but activation fails, inspect the reload path and package metadata before changing training code.
5. If remote CI is the only reliable verification path, use GitHub Actions as the source of truth and record the exact workflow run URL plus head SHA.

Useful log anchor:
- capture tmux output starting from the last `TAG=dev podman-compose up --no-build` marker or the packaging/reload marker, then read forward to the first failure. Avoid reasoning from earlier boot noise.
