---
name: multi-agent-evaluation-router
description: "Fan out prompts to Codex and multiple OpenCode free-model agents, score them with a reusable rubric, and persist routing signals."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [multi-agent, evaluation, opencode, codex, rubric, routing, persistence]
    related_skills: [hermes-agent, opencode, mixture-of-agents, coding-agent-tools]
---

# Multi-agent evaluation router

Use this skill when you need to compare candidate answers from Codex and several OpenCode models, then turn the results into a durable routing signal.

## When to use
- you want to compare multiple coding or reasoning agents on the same prompt
- you want independent reviewers instead of a single generator/judge loop
- you want to learn which OpenCode free models are good fits for a prompt class
- you want to persist compact evaluation metadata for later routing decisions

## When not to use
- there is only one obvious model to run
- the prompt is simple and does not need comparison
- the result is ephemeral and should not be stored

## Required lane shape
Use at least these lanes:
1. one Codex lane
2. two OpenCode lanes pinned to different free models
3. at least two independent reviewer passes

Keep generation and scoring separate. The generator lanes must not be the only reviewers.

## Workflow
1. Classify the prompt into a reusable prompt class.
2. Fan out the prompt to Codex and multiple OpenCode free-model lanes.
3. Capture each lane's output with provider, model, workdir/session, and prompt fingerprint.
4. Apply the shared rubric in independent reviewer lanes.
5. Reconcile reviewer disagreement with an explicit tie-break rule.
6. Persist a compact decision record with the prompt class, lane metadata, scores, and final recommendation.
7. Use the record later when deciding whether a prompt class should keep using OpenCode free models.

## Support files
- `references/routing-workflow.md`
- `references/rubric-template.md`
- `references/reviewer-lanes.md`
- `references/persistence.md`
- `scripts/record_eval.py`

## Maintenance
- Keep this skill class-level and put session-specific prompts, lane choices, sample outputs, and evidence into the linked `references/` files or `scripts/` helpers.
- If a new reusable lesson appears from a run, add it to a reference file instead of creating a separate one-off skill.
- The `scripts/record_eval.py` helper writes compact records into `backlog/decision-memory.json`; use it for replayable evaluation evidence.
