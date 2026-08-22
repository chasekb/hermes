---
name: remote-ci-backlog-closeout
description: "Use for backlog work verified and closed through remote CI."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [backlog, github-actions, ci, closeout, evidence, remote-build]
    related_skills: [project-backlog-workflows, containerized-build-verification, github-pr-workflow]
---

# Remote-CI Backlog Closeout

Archived after absorption into `containerized-build-verification`. The reusable backlog closeout lane now lives in that umbrella's labeled “Backlog closeout lane” section. This archive preserves the former skill identity and recovery pointer.

## Former scope

Use for backlog implementation that must be committed and pushed, forbids local builds, and requires GitHub Actions as build proof. Select the exact branch/event/head SHA run, poll it to completed/success, require every required job, preserve concrete evidence, and distinguish `done` from `closed` when runtime-only criteria remain unverified.

## Former reference

The detailed remote-CI evidence checklist was moved to:
`skills/devops/containerized-build-verification/references/remote-ci-evidence-checklist.md`
