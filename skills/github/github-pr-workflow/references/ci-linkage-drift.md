# CI linkage-drift note

This note captures a real GitHub Actions failure pattern: the workflow itself was healthy, but one matrix job failed because a target compiled a source file that used additional libraries without linking them.

Observed pattern
- A shared implementation file was added to a test target.
- The test target linked only `onnxruntime::onnxruntime`.
- The source file used Torch JIT / ONNX export APIs, so the linker reported many `undefined reference` errors from `torch::jit` / `c10` symbols.
- The production target had a broader link set than the test target, so the test target drifted out of sync.

Debugging takeaway
- When CI fails with linker errors, inspect the exact CMake target that owns the failing binary or test.
- Compare the target’s link libraries against the transitive APIs used by every source file in that target.
- Shared source files are a common place for dependency drift: the code compiles everywhere, but the smaller target’s link line is incomplete.

Fix pattern
- Align the test target’s link libraries with the shared source’s actual dependencies.
- Re-run the same GitHub Actions workflow and verify the exact run id / headSha until the backend jobs complete successfully.

Related verification rule
- Do not report success until the workflow is `completed` and every required job is `success`.
- For matrix builds, a single green job is not enough.
