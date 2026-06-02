# Skill lifecycle and curator rules

This note is the short version of the Hermes skill lifecycle so the curator, backlog review, and skill authors all use the same decision rules.

## Lifecycle

1. Discover
   - A skill enters as a draft or a newly added skill with a clear owner and purpose.
   - It should solve one distinct workflow, not a vague category name.
2. Promote
   - Promote when the skill has a unique action surface, a repeatable use case, and no stronger overlap with an existing skill.
   - Prefer promotion only after it has been used or inspected enough to show it is genuinely reusable.
3. Maintain
   - Keep the skill active when recent telemetry shows real use or sustained inspection.
   - Use `last_activity_at` first, then the individual counters, and treat pinning as an explicit exemption.
4. Retire
   - Archive rather than keep accumulating near-duplicates.
   - If the skill is stale and its job is already covered by a better canonical skill, archive the duplicate and fold any unique notes into the keeper.

## Curator decision rule

The curator should use the same pattern as the backlog review loop:

- first check whether the skill is agent-created and not pinned
- then inspect telemetry (`use_count`, `view_count`, `patch_count`, `last_activity_at`)
- then compare the skill's content against nearby skills for overlap
- then decide: keep, merge, archive, or leave untouched

Use the weekly backlog review and stale-item review as the model for that decision order: durable criteria first, counters second, and raw age only as a tiebreaker.

## Concrete overlap example

`kanban-orchestrator` and `subagent-driven-development` overlap on orchestration, but they are not the same skill:

- keep `kanban-orchestrator` for board routing, decomposition, and dependency management
- keep `subagent-driven-development` for per-task implementation loops and two-stage review
- archive a new skill that only restates one of those halves without adding a distinct workflow surface
- merge any future overlaps into the keeper that already owns the action surface the user needs most often

## Signals that justify archiving a duplicate

- the skill has no unique action surface
- the same workflow is already covered by a better canonical skill
- telemetry shows only incidental inspection, not recurring use
- the skill creates maintenance churn without adding a new capability

## Signals that justify keeping both skills

- each skill owns a different phase of the workflow
- users reach for them in different situations
- the overlap is only in vocabulary, not in operational behavior
- one skill is a narrow specialization and the other is a broader orchestrator
