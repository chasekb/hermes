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

The fix was to replace a hand-written transformer ONNX writer with a real libtorch ONNX export path and to guard overlapping training requests with a `409 Conflict` response when a job is already running.

That combination matters because:
- the exporter fix ensures the artifact is valid
- the conflict guard reduces concurrent background-training overlap that can muddy the logs and confuse diagnosis

## Related verification pattern

When a build log looks successful but the output artifact is rejected later:
- inspect the artifact itself, not just the progress/status endpoint
- capture the log window from the last explicit launch marker
- compare the runtime rejection against the generated file size and format
- if the output is in a bind-mounted data directory, verify that the build actually wrote to the intended host path
