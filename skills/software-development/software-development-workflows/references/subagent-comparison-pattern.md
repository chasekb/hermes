# Subagent comparison pattern

Use this pattern when the user asks to compare two or more workflow options and wants a recommendation grounded in tradeoffs.

## Setup
Spawn one subagent per option plus one synthesis subagent when the question benefits from parallel analysis.

Example split:
- Agent A: analyze option 1 on its own merits.
- Agent B: analyze option 2 on its own merits.
- Agent C: synthesize a recommendation and decision rule.

## Shared context to give every subagent
- Repository or project path
- User constraints and preferences
- Whether the answer should optimize for simplicity, safety, speed, or long-term maintenance
- Any machine / environment asymmetry that matters

## Ask each option agent to return
- Benefits
- Risks
- Operational overhead
- Failure modes
- Best-fit scenarios

## Ask the synthesis agent to return
- Practical recommendation
- If/then decision rule
- Main failure modes to avoid
- Any hybrid approach worth considering

## Pitfalls
- Do not ask the synthesis agent to invent facts not covered by the option agents.
- Do not let the subagents drift into unrelated implementation detail.
- If the user is asking for a decision, keep the final answer decisive rather than a neutral essay.
