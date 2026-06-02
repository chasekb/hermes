# Self-improvement metrics and decision map

This reference captures the concrete telemetry fields and the current-session pattern for Hermes-style self-improvement.

## Metrics maintained

Skill-usage sidecar fields:
- `use_count`
- `view_count`
- `patch_count`
- `last_used_at`
- `last_viewed_at`
- `last_patched_at`
- `created_at`
- `state` (`active`, `stale`, `archived`)
- `pinned`
- `created_by`

Derived field:
- `activity_count = use_count + view_count + patch_count`

Curator gates:
- `interval_hours` (default 7 days)
- `min_idle_hours` (default 2 hours)
- `stale_after_days` (default 30)
- `archive_after_days` (default 90)

Usage analytics commonly consulted alongside curator state:
- sessions
- messages
- tool calls
- input tokens
- output tokens
- total tokens
- active time
- average session length
- average messages per session
- top tools
- top skills
- activity patterns

Memory status is also relevant when deciding whether the agent is learning from durable user facts versus transient session context.

## How the metrics are used

- `last_activity_at` is the best signal for skill freshness.
- `activity_count` is useful for ranking and reporting, but not for declaring a skill valuable on its own.
- `pinned=yes` means the skill is exempt from curator transitions and review.
- `created_by: agent` is the boundary for curator-managed skills.
- Session analytics inform whether the system is being used heavily, which tools dominate, and which skills are most active.

## Current-session snapshot pattern

When the user asks about the current state, inspect:
- `hermes curator status`
- `hermes skills list`
- `hermes insights`
- `hermes sessions stats`
- `hermes memory status`

Then summarize:
1. Whether the curator is enabled and whether it has run yet.
2. Whether there are any agent-created skills to maintain.
3. Which telemetry fields are being maintained and what they mean.
4. Which metrics are actually used in decisions versus simply reported.

## Example interpretation rules

- A skill with `use_count=0` and `view_count>0` may still be important if it is frequently inspected.
- A skill with a low `activity_count` can still be a good keeper if its content is broadly reusable.
- A stale skill that becomes active again should reactivate rather than remain stale.
- The curator should prefer content overlap analysis over pure counter thresholds when considering consolidation.

## Session-specific note

In the reviewed session, the curator was enabled but had not yet completed a real review pass; no agent-created skills were present for maintenance; built-in memory was active; and the observable usage telemetry showed a single tracked local skill entry (`hermes-orchestrator-layout`) with both use and view activity present.
