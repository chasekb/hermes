# Transformer ONNX Artifact Validation

This note captures a real failure mode seen in the trade repo during containerized ML training.

## Symptom

The training job completed and packaged `data/onnx/transformer.onnx`, but model activation failed because the artifact/package contract was inconsistent.

Observed failure pattern:
- packaged artifact existed but was tiny (around 200 bytes)
- loader reported an ONNX Runtime parse/load failure such as `cannot create std::vector larger than max_size()`
- the training pipeline logged that the package was created, then the loader refused to activate it

## What to verify

Before trusting a “training completed” status in a containerized pipeline, verify all three layers:

1. The training job reached the packaging step.
2. The produced artifact is non-empty and plausibly sized.
3. The artifact can actually be loaded by the runtime that will consume it.

## Practical checks

- Check the on-disk size of the exported model file.
- If the file is suspiciously small, treat that as a serialization bug rather than a training-data problem.
- Verify the export path writes a real model proto, not a hand-written placeholder blob.
- Re-run the exact container build or training job after the exporter is fixed, then confirm the new artifact is larger and reloads cleanly.

## Trade-repo lesson

The trade-repo lesson is more specific: a trained transformer package can reach 100% completion and still fail activation after packaging if the runtime package's contract does not match what the loader expects.

Observed failure pattern from tmux capture:
- the log was captured from the last `TAG=dev podman-compose up --no-build` marker in the pane, which isolated the relevant session from older noise
- training progressed to completion
- packaging copied both `transformer.onnx` and `transformer_config.json` into `/app/data/trained_models/...`
- activation then failed with `Skipping transformer model ... because it could not be loaded: cannot create std::vector larger than max_size()`
- the backend followed with `No usable ONNX models found ...` and left the current active model unchanged
- the packaged artifact itself was valid enough to pass ONNX checker, so the failure was in runtime loading / shape discovery, not obvious graph corruption
- the mismatch that mattered was the runtime config contract: `input_layout` / feature-dimension expectations must match between exporter, packaged config, and loader

What fixed the class of issue:
- prefer packaged `transformer_config.json` metadata first for dimensions/layout
- treat ONNX Runtime shape discovery as fallback-only
- keep a valid model loaded even if one candidate fails
- remove invalid/stale trained-package directories after activation failure so later reloads do not rediscover broken state
- make the smoke/regression test call the same production packaging helper that writes the config sidecar; in the trade repo, the fix was to use the trainer-level artifact writer instead of the ONNX-only export helper so the test exercised the real package shape

That combination matters because:
- artifact existence is not enough; the runtime input contract must match
- axis order / shape mismatches can hide behind a successful file write and only surface when onnxruntime loads or executes the model
- metadata lookup can fail independently of model validity, so the loader should not collapse a valid artifact into a fatal load failure just because shape discovery was unavailable
- a loadable artifact should still be validated with a real consumer input before declaring success

## Related verification pattern

When a build log looks successful but the output artifact is rejected later:
- inspect the artifact itself, not just the progress/status endpoint
- capture the log window from the last explicit launch marker (or the last launch command in tmux)
- compare the runtime rejection against the generated file size, layout, and metadata
- if the output is in a bind-mounted data directory, verify that the build actually wrote to the intended host path
- if the post-train activation fails, delete or quarantine the invalid package directory before rerunning so stale artifacts do not mask the fix

## CI linkage pitfall discovered in the trade repo

A later follow-up in the same debugging thread surfaced a different failure mode: the smoke test was updated to call `ModelTrainer::export_transformer_artifact(...)`, but the CI build then failed at link time because the `test_transformer_onnx_export` target did not link the trainer implementation or its `libpqxx` dependency.

Observed CI failure signature:
- `undefined reference to trade::ml::ModelTrainer::ModelTrainer(...)`
- `undefined reference to trade::ml::ModelTrainer::export_transformer_artifact(...)`
- `undefined reference to pqxx::internal::demangle_type_name(...)`

Fix pattern:
- add the implementation source file to the test target (`src/ml/ModelTrainer.cpp` in this case)
- link the transitive library needed by that implementation (`libpqxx::pqxx` here)
- re-run the same workflow run or a fresh push-run and verify the exact `headSha` before declaring success
