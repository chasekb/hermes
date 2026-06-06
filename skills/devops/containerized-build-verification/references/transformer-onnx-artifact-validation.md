# Transformer ONNX Artifact Validation

This note captures a real failure mode seen in the trade repo during containerized ML training.

## Symptom

The training job completed and packaged `data/onnx/transformer.onnx`, but model activation failed because the artifact was malformed.

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

The trade-repo lesson is more specific: the artifact can exist, parse, and still be unusable if the consumer feeds a different tensor contract. In the successful verification pass, the ONNX smoke test failed because the exported model expected `[1, 60, 10]` while the test supplied `[1, 10, 60]`.

That combination matters because:
- artifact existence is not enough; the runtime input contract must match
- axis order / shape mismatches can hide behind a successful file write and only surface when onnxruntime loads or executes the model
- a loadable artifact should still be validated with a real consumer input before declaring success

## Related verification pattern

When a build log looks successful but the output artifact is rejected later:
- inspect the artifact itself, not just the progress/status endpoint
- capture the log window from the last explicit launch marker
- compare the runtime rejection against the generated file size and format
- if the output is in a bind-mounted data directory, verify that the build actually wrote to the intended host path
