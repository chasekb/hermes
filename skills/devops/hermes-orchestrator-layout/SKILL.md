---
name: hermes-orchestrator-layout
description: Canonical layout and workflow for one global Hermes orchestrator profile plus project-specific clones.
version: 1.0.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, profiles, kanban, orchestration, layout]
---

# Hermes Orchestrator Layout

This skill describes the recommended repository/profile layout for a single canonical orchestrator plus project-specific clones.

Canonical source repo:
- /Users/bernardchase/Documents/unordered_map/priority_queue/sum/square/y_bar/map/hermes-orchestrator-layout

## Recommended structure

- Keep one global orchestrator profile as the template.
- Clone that profile for each project.
- Keep shared orchestration guidance in one skill.
- Keep project-specific state in project-local profile directories.

## Suggested profile pattern

- `orchestrator-global` — canonical template profile
- `project-alpha` — clone for one project
- `project-beta` — clone for another project

## Typical workflow

1. Create a canonical orchestrator profile.
2. Clone it for each project.
3. Keep `delegation.orchestrator_enabled` on.
4. Use `delegation.max_spawn_depth: 2` if subagents should orchestrate subagents.
5. Keep kanban dispatch and decomposition enabled for routing work.
6. Point any shared skill source at the same canonical skill directory.

## Practical rule

Use the global profile for shared behavior and policy. Use project-specific profiles for local overrides, credentials, notes, and board context.
