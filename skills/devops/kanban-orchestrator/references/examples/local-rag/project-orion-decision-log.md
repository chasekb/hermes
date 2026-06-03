---
title: Selective Retrieval Decision
type: decision
project: orion
status: accepted
date: 2026-06-03
updated: 2026-06-03
tags:
  - decision
  - project/orion
---

# Selective Retrieval Decision

## Context
The vault should not be loaded wholesale into context.

## Decision
Use the project index note as the entry point, then read only the linked decision log and session summary that are directly relevant to the task.

## Rationale
This keeps token usage predictable while preserving durable project continuity.

## Consequence
If the needed answer is not in the index plus linked notes, Hermes must ask for a different linked note instead of pulling the whole vault.
