# Obsidian-backed context layer for Hermes

Use this when Hermes needs durable project continuity without carrying an entire vault in chat context.

## Core principle
- Obsidian is an external project knowledge base, not transparent agent memory.
- Hermes built-in memory is for stable user/environment facts.
- Hermes compression is for transient chat bloat.
- Obsidian is for durable project notes, decisions, and resumable state.

## Recommended note set
Keep the vault shallow and navigable:
- Project index / MOC note
- Open questions note
- Decision log note
- Session summary note
- Linked reference notes for deeper context

## Suggested folder and note shape
A compact project folder convention works well:

```text
Projects/<project-id>/
  Index.md
  Open Questions.md
  Decision Log.md
  Sessions/
    2026-06-03.md
  References/
    ...linked source notes...
```

### Project index frontmatter
```yaml
---
title: <Project Name> Index
type: moc
project: <project-id>
status: active
updated: YYYY-MM-DD
tags:
  - project/<project-id>
  - moc
  - context-layer
---
```

### Decision log frontmatter
```yaml
---
title: <Decision Topic>
type: decision
project: <project-id>
status: accepted
date: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - decision
  - project/<project-id>
---
```

### Session summary frontmatter
```yaml
---
title: Session Summary - YYYY-MM-DD
type: session-summary
project: <project-id>
status: active
tags:
  - session
  - project/<project-id>
---
```

## Retrieval policy
1. Start from the project index note only.
2. Load the session summary and decision log next.
3. Follow only links that are directly relevant to the current task.
4. Stop after the first-hop set unless a linked note is clearly needed.
5. Use tags/frontmatter/search only if the index is insufficient.
6. Never load the whole vault by default.
7. Prefer concise summaries over verbatim note dumps.

## Write-back policy
After a major task boundary, write back only the distilled outcome:
- update the session summary with what changed and where to resume
- append decisions with rationale and consequences
- refresh the index links if the project structure changed

## Interaction with Hermes features
- Use `hermes compress` when the live conversation is getting bulky.
- Use Hermes memory for stable user/environment facts.
- Use Obsidian for project continuity and long-lived reference material.
- Keep the three layers separate so they do not fight each other.

## Limits
- Do not treat the vault as automatic memory.
- Do not store secrets, tokens, or transient scratch work in durable notes.
- Do not dump the whole vault into context.
- Do not let the note layer become a second chat transcript.

## Smoke test
A valid smoke test is simple:
- Give Hermes only the project index note and one linked decision note.
- Ask it to continue the work or explain the next step.
- Hermes should use only the linked notes it actually needs and should name any additional note it requires.
- If it reaches for unrelated vault content, the workflow fails.

## Good fit
- multi-step project work with recurring context
- long-lived investigations with a stable index note
- tasks where the user wants lower token usage without losing history
