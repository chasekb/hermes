---
name: workflow-skill-curation
description: Decide whether a reusable workflow should become a Hermes skill, a project note, a memory fact, or a backlog item.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [skills, curation, workflow, documentation, memory, backlog]
    related_skills: [hermes-agent, writing-plans, subagent-driven-development]
---

# Workflow Skill Curation

Use this skill when you have discovered a workflow, checklist, or operating pattern and need to decide whether it should be packaged as a reusable Hermes skill or left as project-specific documentation, memory, or backlog work.

## When to Use

- A workflow has repeated at least once and may recur again.
- You are deciding where to store durable knowledge after a research or implementation pass.
- A checklist, gap analysis, or closeout pattern needs to be packaged for future reuse.
- You are choosing between skill, note, memory, and backlog for a new capability.

## Quick Reference

- Skill = reusable procedure
- Project note = repo/project-specific context
- Memory = durable fact or preference
- Backlog = unstable work, open question, or implementation item

## Procedure

1. Identify the artifact type.
   - Is it a fact, a procedure, a project convention, or unfinished work?
2. Check repeatability.
   - Has this workflow happened more than once, or is it clearly likely to recur?
3. Check portability.
   - Would this still make sense outside the current project or session?
4. Check executability.
   - Can the workflow be expressed as instructions plus existing Hermes tools?
5. Check stability.
   - Is the workflow stable enough that future edits will be incremental rather than a redesign?
6. Check verification.
   - Can another agent tell whether the workflow succeeded?
7. Route the artifact.
   - Skill if it is procedural, repeatable, portable, and tool-executable.
   - Project note if it is durable but project-specific.
   - Memory if it is a stable fact or preference.
   - Backlog if it is still changing or needs code/workflow changes first.

## Decision Rule

Use the detailed rubric in `references/skillify-rubric.md`.

## Pitfalls

- Turning a one-off incident into a skill too early.
- Using memory for procedure or backlog for facts.
- Baking project-specific paths or conventions into a supposedly reusable skill.
- Writing a skill that is broader than the actual workflow.
- Failing to include verification, so the workflow cannot be validated later.

## Verification

A good outcome lets a future agent answer all of these:

- What problem does this skill solve?
- When should it load?
- What steps should it follow?
- How do I know the result is good?
- What should not be promoted into memory or backlog?
