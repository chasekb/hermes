# Capability Inventory Audit

Use this when the user asks for a broad inventory or gap analysis across several surfaces, especially combinations like:
- hooks / hook routers
- MCP servers
- skills / skill availability
- profile or project enablement

## Goal
Produce a ranked, evidence-backed report that separates:
- installed / present
- enabled / wired into the active project or profile
- verified-working

## Recommended split
Use one subagent per surface, plus one synthesis subagent when the request spans more than two surfaces.

Example lanes:
1. Hooks: discover which hooks exist, which are active, and which are missing from the current project.
2. MCP servers: discover configured servers, enabled tools, and runtime-test coverage.
3. Skills: discover installed skills, loaded/available skills, and any missing umbrella coverage.
4. Synthesis: combine the findings into a single prioritized gap report.

## Reporting rules
- Do not collapse "installed" and "enabled" into one bucket.
- Do not call something working until there is runtime evidence.
- If "popularity" is ambiguous, state the ranking criterion used. Common choices: default/bundled, frequently referenced in the repo, or currently enabled in the profile.
- Prefer a short table with columns: item, surface, state, evidence, recommended next action.

## Evidence examples
- Skills: `skills_list`, `skill_view`, or repository inspection
- MCP servers: `hermes mcp test <name>` or equivalent runtime verification
- Hooks: config or runtime registration evidence, not just file presence

## Pitfalls
- Reporting a missing item without checking whether it is disabled rather than absent.
- Treating static presence as proof of runtime availability.
- Mixing project-level and profile-level enablement without labeling the source.
- Letting the synthesis agent guess at ranking without stating the rule.
