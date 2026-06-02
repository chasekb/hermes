# Hermes capability audits with subagents

Use this workflow when the user asks to inventory or compare project/runtime capabilities such as:
- installed/enabled MCP servers
- available skills in the active project/profile
- hook coverage or hook routing
- what is missing vs what is already wired in

## Recommended pattern
1. Split the audit into independent slices and run them in parallel with subagents.
   - one subagent for hooks/config
   - one for MCP servers
   - one for skills
   - one for project/profile-specific overrides or enabled state
2. Prefer direct verification over inference.
   - inspect the live config/state
   - list the relevant inventory
   - test candidates that look enabled but may not actually connect
3. Reconcile the subagent results in the parent session and report only confirmed findings.

## Good probes
- MCP inventory: list configured servers, then test a few representative ones to confirm transport/auth/tool discovery.
- Skill inventory: list skills available to the current profile/project and note which ones are enabled or missing.
- Hooks: inspect the project Hermes config and hook router path; verify which hook events are wired and whether they point to the expected router.

## Reporting guidance
- Separate “available globally” from “enabled in this project/profile”.
- Call out uncertainty explicitly when a server/skill exists but was not verified in the current profile.
- Do not treat a single discovery command as sufficient if a downstream connection test is available.

## Session pattern that worked
- Parallel probes can be faster than one monolithic scan when the surfaces are independent.
- A small set of representative MCP tests is usually enough to validate transport + discovery.
- This audit style is useful for “what’s missing?” questions before installing or enabling new capabilities.

## Session note: 8-subagent capability audit decomposition
When the user asks for a ranked inventory of missing capabilities (for example, "most popular hooks, MCP servers, and skills not installed/enabled in this project"), split the audit more finely instead of letting one worker do everything.

Recommended split:
1. hooks/config surface
2. MCP server inventory
3. installed skills inventory
4. enabled/disabled skills state
5. project/profile override discovery
6. bundled/default catalog comparison
7. popularity shortlist synthesis
8. final reconciliation and deduplication

Rules:
- Treat "installed", "enabled", and "verified working" as separate states.
- Treat project scope and profile scope as separate from global scope.
- Use direct verification for anything that claims to be enabled.
- Return a ranked shortlist of missing capabilities only after reconciling the slices.
