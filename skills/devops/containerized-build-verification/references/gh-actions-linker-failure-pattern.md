# GitHub Actions link-time failure pattern

This note captures a recurring CI-debugging pattern from the trade repo.

## Symptom

A GitHub Actions Docker build failed in the C++ backend job with link-time errors during a smoke-test target build:

- `undefined reference to trade::ml::update_execution_cohort(...)`
- `undefined reference to trade::ml::finalize_execution_cohorts(...)`
- `undefined reference to trade::ml::summarize_execution_cohorts(...)`
- C++ compile error from a call site still constructing a service whose constructor had been made private

## Root cause shape

The code change was valid in the production source, but the CI test target was missing the implementation translation unit that defined the new helpers.

In this case:

- `src/ml/ExecutionCohorts.cpp` was linked into the main app target
- `test_transformer_onnx_export` did not include `src/ml/ExecutionCohorts.cpp`
- `PredictController` still used `TradingStatsService()` instead of the singleton accessor

## Fix pattern

1. Inspect the failing job’s exact link errors with `gh run view <run_id> --job <job_id>` or `gh api repos/<owner>/<repo>/actions/jobs/<job_id>/logs`.
2. Trace each undefined symbol back to its defining `.cpp` file.
3. Check the failing test/executable target’s source list in `CMakeLists.txt`.
4. Add the missing implementation file(s) to the test target, not just the app target.
5. Update any call sites that still use an old construction pattern after an API becomes singleton-based.
6. Re-run the same GitHub Actions run until every required job is green.

## Verification checklist

- The specific workflow run matches the pushed `headSha`
- The same run transitions to `status=completed` and `conclusion=success`
- Every required job in the matrix reports `success`
- The final report includes the run URL and verified SHA
