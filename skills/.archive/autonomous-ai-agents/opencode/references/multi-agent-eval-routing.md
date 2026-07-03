# Multi-agent OpenCode evaluation routing notes

Session-derived notes for using OpenCode as part of a Hermes evaluation-and-routing workflow.

## Pattern
- Fan out the same prompt to Codex plus multiple OpenCode agents pinned to different free models.
- Treat generation, scoring, reviewer comparison, and persistence as separate lanes.
- Keep the evaluation rubric independent from the agent that produced the candidate output.
- Use reviewer disagreement as a signal, not a failure by itself; tie-breaks should be explicit.

## Rubric shape
Use named criteria with stable anchors:
- correctness
- completeness
- instruction-following
- risk / safety
- usefulness for future routing decisions

## Persistence fields
Keep the durable record compact and queryable:
- prompt fingerprint
- agent model / provider
- reviewer ids
- criterion scores
- reviewer rationale
- tie-break outcome
- final routing recommendation

## Operational cautions
- Do not let the generator lane self-score.
- Do not collapse the multi-agent comparison into a single opaque summary before scores are persisted.
- Keep low-stakes OpenCode routing evidence-backed: use historical scores to justify future delegation, not vice versa.

## Related notes
- `references/low-stakes-routing-for-hermes.md`
- `SKILL.md` one-shot workflow section
- `skills/autonomous-ai-agents/multi-agent-evaluation-router/SKILL.md`
