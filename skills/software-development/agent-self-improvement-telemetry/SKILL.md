---
name: agent-self-improvement-telemetry
description: "Inspect, interpret, and act on an agent's self-improvement loop: skill curator, skill-usage telemetry, memory, and usage analytics."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [self-improvement, telemetry, curator, skills, metrics, analytics, memory]
---

# Agent Self-Improvement Telemetry

Use this skill when you need to understand or update an agent's learning loop: skill curation, skill-usage metrics, memory, and the analytics that influence maintenance decisions.

This skill is intentionally broad. It is not about one session or one error string; it is the umbrella for observing how the agent improves itself over time.

## What to inspect first

1. Curator status
   - whether the curator is enabled
   - last run / run count
   - interval and idle gates
   - stale/archive thresholds
2. Skill-usage telemetry
   - per-skill use/view/patch counters
   - derived activity count
   - last activity timestamps
   - state and pinning
3. Usage analytics
   - sessions, messages, tool calls, tokens, active time
   - top tools, top skills, activity patterns
4. Memory status
   - whether built-in memory is active
   - whether an external provider is configured

See `references/self-improvement-metrics.md` for a compact field guide and a current-session snapshot pattern.
See `references/decision-memory-loop.md` for the durable record format that backlog and review workflows consume.
See `references/skill-lifecycle-and-curation.md` for the keep / merge / archive rule and the overlap example used by the curator.

## Core metrics and how they are used

Curator decisions are driven by these fields:
- `use_count` — active use of a skill
- `view_count` — inspection / reading of a skill
- `patch_count` — edits to a skill
- `last_used_at`, `last_viewed_at`, `last_patched_at`
- `last_activity_at` — derived latest of the activity timestamps
- `state` — active, stale, archived
- `pinned` — skip any auto-transition or review action
- `created_by` — curator only acts on agent-created skills

Derived metric:
- `activity_count = use_count + view_count + patch_count`

Decision rules:
- Do not treat low counters alone as a reason to delete or consolidate; content overlap matters more than raw usage.
- Prefer `last_activity_at` over `use_count` when deciding whether a skill is stale.
- Pinned skills are off-limits to auto-transition and review.
- The curator should only operate on agent-created skills; bundled and hub-installed skills are not candidates.

## Workflow

1. Inspect current state.
2. Separate durable telemetry from transient session noise.
3. Decide whether you are updating:
   - the skill library itself
   - the curator configuration
   - the telemetry interpretation rules
4. If you discover a reusable pattern, patch the umbrella skill and add a short reference note.

## Decision-memory loop

The durable decision-memory store lives at `~/.hermes/backlog/decision-memory.json`.
Write compact, redacted records there when a workflow, skill, or hook change finishes so the next weekly or stale review can turn the observed outcome into a recommendation.

Use the store for decision support, not raw logging:
- capture the expected outcome and the observed outcome
- record the recommendation for the next review pass
- keep secrets, tokens, and raw transcripts out of the durable record
- prefer one short evidence pointer over a long transcript dump

## Lifecycle rule of thumb

Use the curator the same way you would review backlog items: durable criteria first, telemetry second, age last.

- Discover a skill only when it owns a distinct workflow surface.
- Promote it only after repeatable use or repeated inspection shows it is reusable.
- Maintain it when `last_activity_at` and the counters still show real use.
- Retire it when it is stale and a canonical skill already covers the same action surface.
- Keep pinned or non-agent skills out of curator transitions.

If two skills overlap, keep the one that owns the action surface and archive the one that only restates it.

## Pitfalls

- Do not confuse session analytics with skill-usage telemetry. They answer different questions.
- Do not use `use_count == 0` as proof a skill is worthless.
- Do not forget pinning: pinned skills remain out of the curator's hands.
- Do not encode one-off numeric snapshots into the main SKILL.md; put those in a reference file.

## Verification

Useful checks when reviewing the system:
- `hermes curator status`
- `hermes skills list`
- `hermes insights`
- `hermes sessions stats`
- `hermes memory status`

Use the outputs to decide whether the learning loop is healthy, idle, or in need of cleanup.
