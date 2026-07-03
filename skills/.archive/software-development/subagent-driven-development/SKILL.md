---
name: subagent-driven-development
description: "Compatibility alias for the canonical software-development-workflows subagent execution guidance."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [subagents, delegation, review, compatibility-alias]
---

# Subagent-Driven Development (Compatibility Alias)

This skill exists so older prompts and related-skill references that still name `subagent-driven-development` continue to resolve.

Canonical guidance lives in `software-development-workflows`:
- use the `Subagent execution` section for parallel or isolated work
- use `Independent review` before landing changes
- use `Planning`, `Test-first implementation`, and `Systematic debugging` as needed

## When to load this alias
- An older prompt or doc explicitly names `subagent-driven-development`
- A lookup needs to resolve the historical skill name without breaking
- You want the canonical replacement surfaced through a stable wrapper

## What to do next
Load `software-development-workflows` for the real operating guidance.
If you are maintaining references, prefer the canonical umbrella skill in new content and keep this file only for compatibility.
