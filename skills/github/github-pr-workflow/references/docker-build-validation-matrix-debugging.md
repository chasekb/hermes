# Docker Build Validation: matrix backend debugging notes

This note captures a real matrix-build verification session on `trade` where the workflow was the source of truth.

## What happened

- Workflow: `Docker Build Validation`
- Verification method: GitHub Actions only; no local build was treated as proof.
- Required check: every matrix job had to finish, not just the first green job.

### Failure progression

1. Initial failure was a backend link error in `TransformerOnnxExport.cpp`.
   - Missing Torch/Python link deps on `test_transformer_onnx_export` caused undefined references.
   - Fix: link `${TORCH_LIBRARIES}` and `Python3::Python` for the test target.

2. After link fixes, the backend still failed inside the CI-only smoke test.
   - `ctest -R transformer_onnx_export` failed during ONNX export.
   - The failure moved from link-time to runtime export compatibility, proving the target was now compiling but the smoke path was still wrong.

3. The smoke test went through several export shapes.
   - Hand-built ATen graphs can fail in `torch::jit::export_onnx`.
   - A traced real model path was closer to the actual production export surface than a synthetic operator graph.

## Practical takeaways

- Treat the exact GitHub Actions run as the canonical evidence.
- Match both branch and `headSha` before trusting a run.
- Read failed job logs from the same run id; do not infer root cause from an older run.
- For matrix workflows, require all required jobs to reach terminal success before reporting success.
- When the failure shifts from linker errors to runtime export errors, the fix likely needs to move from dependency wiring to export-path correctness.

## Useful commands

```bash
gh run list --branch <branch> --limit 10 --json databaseId,status,conclusion,workflowName,headSha,displayTitle,url,createdAt
gh run view <RUN_ID> --json status,conclusion,jobs,url,workflowName,headSha,displayTitle
gh run view <RUN_ID> --log-failed
```
