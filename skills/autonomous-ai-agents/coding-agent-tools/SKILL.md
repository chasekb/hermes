---
name: coding-agent-tools
description: "Delegate coding to external agent CLIs and choose the right agent workflow."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [coding-agent, delegation, cli, automation, review]
---

# Coding Agent Tools

Use this umbrella when the task should be delegated to an external coding agent instead of being done directly in Hermes.

## Core idea
Pick the agent that best matches the environment and then constrain it tightly:
- one repo or workdir
- one goal
- explicit verification
- concrete output expectations

## General rules
- Prefer bounded one-shot runs for small tasks.
- Use interactive or background sessions only when the task truly needs iteration.
- Keep each agent in a single repository or worktree.
- Monitor long-running jobs instead of assuming progress.
- Always verify the final diff and tests yourself.

## Choosing an agent
- **Claude Code**: strong default for autonomous coding, refactors, and PR review loops.
- **Codex**: useful for GitHub/OpenAI-centric coding workflows and branch-local automation.
- **OpenCode**: useful when you want a provider-agnostic coding worker with TUI and CLI modes.

## Workflow shape
1. Describe the task narrowly.
2. Provide the repository path and any required constraints.
3. Start the agent in the safest mode that fits the task.
4. Capture progress or outputs if the run is long.
5. Verify changed files, test results, and remaining risks.

## Pitfalls
- Do not let the agent roam across unrelated directories.
- Do not use interactive mode when a one-shot run will do.
- Do not trust a claimed success without reading the resulting diff or test output.
- Do not confuse provider auth quirks with task failure; check the exact CLI and session state.

## Legacy subclasses absorbed into this umbrella
This class-level tool-selection workflow replaces the narrower standalone skills for Claude Code, Codex, and OpenCode delegation.
