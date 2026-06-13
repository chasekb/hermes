---
name: mixture-of-agents
description: "Use Hermes's MoA toolset effectively for hard multi-model reasoning tasks."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [moa, multi-model, openrouter, aggregation, reasoning, reliability]
    related_skills: [hermes-agent, subagent-driven-development]
---

# Mixture of Agents (MoA)

Use this skill when you want Hermes's `moa` toolset to solve a hard problem by combining several model outputs and then synthesizing them into one answer.

## Best fit

Use MoA for:
- complex math
- algorithm design
- multi-step reasoning
- deep code analysis
- tradeoff-heavy research synthesis
- questions where independent perspectives reduce blind spots

Do not use MoA for:
- simple lookups
- short factual questions
- low-latency tasks
- problems that already have an obvious answer

## What the tool actually does

Current Hermes MoA behavior is a fixed two-stage pipeline:
1. reference models generate responses in parallel
2. an aggregator model synthesizes the best parts into one final answer

Implementation detail: both stages currently route through the OpenRouter client, so the configured model IDs must be valid OpenRouter slugs for the account in use. The aggregator can be the same model as one of the references, but using a distinct synthesis model is usually better when you want maximal diversity.

The default tool schema only accepts `user_prompt`.
If you need custom reference models or a different aggregator, patch the implementation in `tools/mixture_of_agents_tool.py` or call the Python function directly.

## Required setup

- `OPENROUTER_API_KEY` must be available
- The selected models must be valid for your OpenRouter account
- At least one reference model must return usable content

## Good prompt shape

Ask MoA for:
- multiple candidate approaches
- explicit tradeoffs
- a final recommendation
- concise synthesis of disagreements

Example:

```text
Compare three ways to design a Hermes skill for toolset audits. Have each model propose a different approach, then synthesize a recommended design with risks and a final decision.
```

## Failure mode: all reference models fail

If MoA returns an error like:

- `Insufficient successful reference models (0/4)`

then the issue is usually one of these:
- every reference model call failed
- the selected model IDs are stale or unavailable
- the account cannot access one or more models
- the models returned empty reasoning-only output repeatedly

Recovery steps:
1. verify the OpenRouter key is loaded
2. try a smaller set of known-good models
3. prefer direct model IDs over router aliases
4. re-run with a narrower prompt
5. inspect the MoA debug log if debugging is enabled

## Tuning notes

Current defaults in the implementation are easy to miss:
- reference models are hardcoded in source
- the aggregator model is hardcoded in source
- the runtime tool schema currently only accepts `user_prompt`
- empty-content reference responses are retried before failing

When validating a model-set change, prefer a two-step check:
1. run the MoA test file with dev deps
2. run a mocked invocation to confirm the exact reference list and aggregator wiring before trying live calls

## Learning from MoA runs

If the question is not just "did MoA answer this once?" but "is MoA improving outcomes over time?", pair MoA usage with hook-based telemetry and durable review memory.

Record compact run metadata such as:
- model set used
- synthesis success or failure
- retry count
- latency bucket
- outcome / verdict
- short evidence pointer

Avoid using raw transcripts as the durable record; keep them as transient debugging context only.

## Support files

- `references/model-selection.md` — how to choose current-good OpenRouter models for MoA
- `references/failure-modes.md` — common MoA failures and how to recover

## Practical rule

If MoA is failing on all references, do not keep retrying the same prompt blindly. Change the model set or simplify the prompt first.
