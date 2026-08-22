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

## Multi-agent routing and evaluation
Use this lane when you need to compare several agent outputs or combine multiple model perspectives.
- Prefer it when a single agent is likely to miss tradeoffs or edge cases.
- Keep generation, scoring, and final synthesis separate.
- Record the prompt class, models used, and final routing decision so the result can be reused later.
- Treat MoA-style synthesis as a reusable workflow, not a one-off trick.

## Workflow shape
1. Describe the task narrowly.
2. Provide the repository path and any required constraints.
3. Start the agent in the safest mode that fits the task.
4. Capture progress or outputs if the run is long.
5. Verify changed files, test results, and remaining risks.

## Coding-agent state and context-efficiency audits
Use this lane when assessing a coding-agent home such as `~/.claude`, `~/.codex`, or another local harness.
- Inspect the direct local source first; do not infer current state from old sessions.
- Exclude credentials, auth caches, shell snapshots, backup bodies, and transcript message text unless the user explicitly authorizes them.
- Separate four surfaces: startup-loaded instructions, conditionally loaded rules/skills/tools, resumable transcript state, and disk-only caches/catalogs.
- Verify extension activation with the agent CLI. A cloned marketplace, plugin manifest, or MCP file is not evidence that the capability is enabled or consuming context.
- Audit transcript usage through metadata only: recurse through all JSONL paths, including nested subagent logs; aggregate input, cache-creation, cache-read, output, compaction, and tool-name fields without emitting message bodies.
- Timestamp metrics because active agent directories mutate during inspection. Re-run the final recursive snapshot before publishing.
- Treat prompt-cache efficiency and context efficiency as different metrics: cache hits reduce repeated computation/cost but do not reduce context occupancy or attention dilution.
- Compare local state against current official documentation and the currently published CLI version, then label observed facts, estimates, causal hypotheses, and recommendations separately.
- For multi-agent research, split local audit, external state-of-the-art evidence, and target-architecture critique into independent tracks; synthesize only after all three return.
- Prefer a layered target: tiny hot instructions, path-scoped warm rules, on-demand skills/subagents, and cold provenance-rich evidence retrieved under a strict budget.

See `references/coding-agent-state-and-context-audit.md` for the metadata-only audit checklist, synthesis pattern, and rollout gates.

## Inspecting CLI-backed providers and delegation lanes
When evaluating whether to add a coding-agent CLI as a Hermes provider or delegation backend, inspect the existing provider router, auth resolver, child-agent builder, subprocess adapters, config defaults, and tests before proposing edits. Prefer a delegation lane when the external CLI is an autonomous runtime rather than a stable inference protocol: a first-class provider additionally requires transport selection, prompt/tool serialization, lifecycle, cancellation, model catalog, and client construction changes. Reuse the existing child-result schema and observability fields when adding a lane. Keep CLI-managed credentials in the external process's own store or inherited environment; never read or copy credential files into config or reports.

Record auth precedence separately for helper functions versus the authoritative runtime resolver—legacy convenience helpers may order environment variables differently. For external-process providers, trace command and argument precedence, working-directory propagation, timeout/termination behavior, and stderr handling. Treat missing test directories or binaries as repository/setup facts, not durable feature limitations; propose fake-executable tests for deterministic subprocess verification.

See `references/cli-provider-delegation-inspection.md` for the concrete Hermes inspection checklist and the Claude Code/Copilot ACP comparison pattern.

## Pitfalls
- Do not let the agent roam across unrelated directories.
- Do not use interactive mode when a one-shot run will do.
- Do not trust a claimed success without reading the resulting diff or test output.
- Do not confuse provider auth quirks with task failure; check the exact CLI and session state.

## Legacy subclasses absorbed into this umbrella
This class-level tool-selection workflow replaces the narrower standalone skills for Claude Code, Codex, OpenCode delegation, MoA-style multi-model synthesis, and multi-agent evaluation routing.
