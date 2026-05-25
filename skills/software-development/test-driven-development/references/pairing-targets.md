# Pairing-target expansion pattern

Use this when a pipeline grows a sibling target that should behave like an existing one (for example: `main_1d -> metrics_1d` and `main_1m -> metrics_1m`).

## Pattern
1. Extract target construction into a helper that returns an explicit list of source/derived table pairs.
2. Add a focused test for the helper that asserts all expected pairs are present.
3. Wire the production loop to iterate over the helper output instead of hard-coding a single table pair.
4. Keep any downstream side effects that are specific to one lane gated to the lane that owns them.

## Verification
- Run the smallest focused test for the helper first.
- Then run a syntax check or build of the affected translation unit(s) to catch integration errors early.
- Prefer verifying the exact edited code path before running the whole suite.
