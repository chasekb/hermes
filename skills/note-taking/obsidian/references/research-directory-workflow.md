# Research directory workflow

This reference captures the durable note structure used for Hermes research work.

## Directory shape
- `Research/Research Index.md` — top-level landing page for general research navigation.
- `Research/Research Workflow.md` — append-only automation and daily update rules.
- `Research/Agents/Agents Research Index.md` — hub for agent-systems research.
- `Research/Agents/Harness Engineering.md` — harness-specific synthesis.
- `Research/Agents/Loop Engineering.md` — loop-specific synthesis.
- `Research/Agents/Harness Loop Synthesis.md` — cross-cutting overlap and Hermes implications.
- `Research/Agents/Sources.md` — canonical source registry.

## Operating rules
- Keep research append-only.
- Separate topical notes from the source registry.
- Put automation instructions in the workflow note, not in the topic notes.
- Use the top-level research index as the first navigation step for general research.
- Update the synthesis page only when overlap or system implications change.

## Maintenance pattern
- Daily cron job appends only new evidence-backed findings.
- If nothing substantive changed, record that explicitly instead of inventing filler.
- Prefer primary sources and official docs.
- Update the Hermes project index with a link to the research landing page so project notes can navigate into the general research area.