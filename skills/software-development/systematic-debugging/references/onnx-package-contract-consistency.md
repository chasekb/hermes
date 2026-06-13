# ONNX package contract consistency

Session note: trade repo transformer training/activation fix.

Root cause pattern
- The exporter wrote a runtime package with a config/metadata contract that the loader did not fully honor.
- The model file itself could be valid while the packaged copy still failed at activation time because the loader interpreted layout/shape metadata differently.

Rules of thumb
1. Treat the runtime package as the source of truth for activation debugging, not just the checked-in source artifact.
2. Keep exporter, loader, and package metadata in one contract: the config written at export time must match what the loader expects to parse at startup.
3. If the loader supports only one canonical runtime layout, normalize unknown/stale config values to that canonical form and warn loudly.
4. Add a regression check that the export path writes the canonical config value used by the loader.
5. If packaging succeeds but activation fails, inspect the copied package dir first: model file, config file, metadata, and package cleanup behavior.

Observed failure signature
- backend logged `Skipping transformer model ... because it could not be loaded: cannot create std::vector larger than max_size()`
- followed by `No usable ONNX models found in ...`
- activation failed even though packaging completed

Useful verification target
- A smoke/regression test should validate both: ONNX session load succeeds and the packaged config contains the canonical `input_layout` value.
- If the smoke test is meant to validate the runtime package, it must call the same production packaging helper that writes the config sidecar; a model-only export helper can produce a false failure by omitting the metadata file entirely. In the trade-repo case, the test needed to use the trainer-level artifact writer rather than the lower-level ONNX-only helper.
