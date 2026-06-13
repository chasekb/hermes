# Should We Skill-ify It? Rubric

## Purpose
This rubric decides whether a discovered workflow should become a reusable Hermes skill or stay as project-specific documentation, memory, or backlog work.

## Decision matrix

Score each question 0-2.
- 0 = no / not yet
- 1 = partly
- 2 = yes

Questions:
1. Repeatability: Has this happened more than once, or is recurrence likely?
2. Procedural shape: Can the workflow be written as steps rather than just notes?
3. Portability: Would it help in more than one project, profile, or session?
4. Tool-executability: Can Hermes already perform it with existing tools?
5. Stability: Is the workflow stable enough to document now?
6. Verifiability: Can a future agent tell whether it worked?

Interpretation:
- 9-12: skillify
- 5-8: usually keep as project note or backlog until the pattern stabilizes
- 0-4: do not skillify yet

## What becomes what

### Skill
Use when the artifact is a reusable procedure.
Examples:
- checklist-driven workflow
- gap analysis with a consistent decision tree
- memory-promotion rule set
- notebook maintenance routine

### Project note
Use when the artifact is durable but project-specific.
Examples:
- repo paths
- team conventions
- a project backlog item
- local state or environment details

### Memory
Use when the artifact is a stable fact, preference, or environment detail.
Examples:
- user preferences
- fixed filesystem facts
- stable tool quirks
- environment invariants

### Backlog
Use when the artifact is still changing or needs implementation work first.
Examples:
- a new runtime hook
- a workflow that needs code before it can be standardized
- an unresolved design choice

## Skill-ify if all of these are true
- Repeated or likely to repeat
- Procedural and tool-executable
- Portable beyond one project
- Stable enough to maintain
- Verifiable
- Narrow enough to be useful

## Do not skill-ify if any of these are true
- One-off diagnosis
- Mostly project facts rather than procedure
- Still unstable or under design
- Needs code changes before it can be reusable
- Broad enough to become a megaskill

## Packaging guidance

If you do skill-ify it:
- keep the trigger short
- put the procedure first
- push long detail into references
- include pitfalls and verification
- avoid hardcoding project-only paths unless the skill is project-scoped on purpose

## Output format
When deciding, return:
- Recommendation: skill / project note / memory / backlog
- Score: X/12
- Reason: one sentence
- Next step: the smallest useful follow-up
