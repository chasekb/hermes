# MoA failure modes and recovery

This file collects the common MoA failure shapes and the quickest recovery steps.

## 1) No successful references

Example shape:
- `Insufficient successful reference models (0/4)`

Likely causes:
- every reference model call failed
- the selected model IDs are stale or unavailable
- the account cannot access one or more models
- the models repeatedly returned empty or unusable output

Recovery steps:
1. verify `OPENROUTER_API_KEY` is present
2. reduce the reference set to 2-3 known-good models
3. prefer direct model IDs over broad aliases
4. simplify the prompt so the references can answer directly

## 2) Aggregator failure

If the references succeed but aggregation fails:
- inspect the aggregator model slug first
- verify the aggregator is a valid OpenRouter model for the account
- keep the aggregator temperature conservative

## 3) Empty-content retries

The implementation retries empty content once for both layers.
If you still see empty output after retries, treat it as a model-selection or prompt-shape issue rather than a transient glitch.

## 4) Validation recipe

Before changing defaults in source:
1. run the MoA test file with dev dependencies
2. mock the reference runner and aggregator runner to assert the exact model IDs
3. only then run the live MoA path

## 5) Good triage question

When MoA fails, ask:
- did at least one reference return usable content?
- is the aggregator slug valid for this account?
- did the prompt ask for something the selected models can actually do?
