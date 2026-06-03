# Public skill / MCP / workflow survey gate

Use this gate whenever you are about to add a new Hermes skill, MCP server integration, rule, workflow, or any capability surface broad enough that it could duplicate an existing pattern.

## Why this exists
- Avoid reinventing a pattern that already exists.
- Keep broad reconnaissance in subagents so the primary agent can synthesize.
- Preserve reusable findings in a durable reference instead of losing them in chat.

## Trigger conditions
Run the gate when:
- a new capability surface is proposed
- an existing skill/workflow is being generalized
- an MCP integration is being added or replaced
- a backlog item explicitly asks for prior-art or survey-first work
- it is unclear whether a reusable pattern already exists

## Survey lanes
Split the work into focused subagents instead of one wide search:
1. Existing Hermes skills, references, and backlog items.
2. Public analogs from comparable agent ecosystems such as Claude Code, Codex, and Clawdhub.
3. MCP server patterns, wrappers, and configuration.
4. Current Hermes workflow registry, intake docs, and backlog state.

## Subagent brief template
Use a short, lane-specific prompt for each subagent.

```text
Goal: Survey the <lane> for reusable prior art before we design a new capability.

Return:
- sources inspected (URLs or file paths)
- reusable patterns
- gaps or missing pieces
- what should NOT be duplicated
- a recommendation: reuse, adapt, or new
- a one-paragraph synthesis for the orchestrator

Constraints:
- Prefer evidence over speculation.
- Cite the exact docs or files you inspected.
- Keep the answer concise and structured.
```

## Required output shape
The orchestrator should collect the lane results into one compact record.

```json
{
  "sources": ["..."],
  "reusable_patterns": ["..."],
  "gaps": ["..."],
  "do_not_duplicate": ["..."],
  "recommendation": "reuse|adapt|new",
  "subagents": [
    {"lane": "...", "id": "...", "finding": "..."}
  ],
  "notes": "..."
}
```

## Decision rule
- Reuse an existing umbrella skill or reference when the pattern already exists.
- Adapt by patching an umbrella skill or adding a reference/helper when the pattern is close but incomplete.
- Create a new skill only if the surface is genuinely distinct and reusable.

## Intake integration
For backlog-driven work, the gate belongs before implementation starts:
1. Read the backlog item or user request.
2. If the request could duplicate an existing capability, run the survey gate.
3. Add the survey findings to the backlog item's execution criteria or closeout notes.
4. Then implement the chosen reuse/adapt/new path.

## What to record
Preserve the survey outcome in a durable place:
- backlog item history / evidence
- a reference file under the owning umbrella skill
- a skill patch when the reusable pattern belongs in a skill

Record at least:
- the lanes that were surveyed
- the sources checked
- the recommendation and why
- whether the outcome reused, adapted, or created something new

## Pitfalls
- Do not do the broad survey entirely in the primary agent when subagents can parallelize it.
- Do not create a new skill just because a one-session task succeeded.
- Do not let the survey result live only in chat history.
- Do not skip the skill-vs-tool decision gate.
