---
project_id: hermes
note_type: research-topic
updated_at: 2026-06-12T00:00:00Z
---
# Skill Curation

## Scope
Decide whether a discovered workflow should become a reusable Hermes skill, remain a project note, become a memory fact, or stay in backlog until it stabilizes.

## Search queries used
- `site:hermes-agent.nousresearch.com/docs skills creating skills curator best practices hermes`
- `site:hermes-agent.nousresearch.com/docs Hermes curator skills lifecycle telemetry stale archive`
- `site:hermes-agent.nousresearch.com/docs Hermes memory persistent memory skills workflow documentation`
- `site:hermes-agent.nousresearch.com/docs user-guide features skills Hermes skills system creating skills best practices`
- `"should we skill-ify it" Hermes`
- `"checklist-driven workflow" Hermes skill curation`
- `"workflow skill curation" Hermes`
- `"memory-promotion" checklist Hermes skill`

## Sources reviewed
- Hermes Agent docs, Creating Skills
  - https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills/
- Hermes Agent docs, Skills System
  - https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/
- Hermes Agent docs, Curator
  - https://hermes-agent.nousresearch.com/docs/user-guide/features/curator/
- OpenAI, Harness engineering: leveraging Codex in an agent-first world
  - https://openai.com/index/harness-engineering
- Anthropic, Effective context engineering for AI agents
  - https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Research notes on harness and loop engineering
  - [[Harness Engineering]]
  - [[Loop Engineering]]
  - [[Harness Loop Synthesis]]

## Sources used in synthesis
- Hermes Agent docs, Creating Skills
- Hermes Agent docs, Skills System
- Hermes Agent docs, Curator
- OpenAI, Harness engineering: leveraging Codex in an agent-first world
- Anthropic, Effective context engineering for AI agents

## Knowledge developed
- Hermes skills are best treated as reusable procedures, not as generic note dumps.
- Memory should hold facts and preferences; it is the wrong place for procedures.
- Project notes should hold durable project-specific context.
- Backlog should hold unstable or still-changing work.
- A workflow should be skill-ified only when it is repeatable, procedural, portable, tool-executable, stable enough to maintain, and verifiable.
- The more a workflow depends on exact repo paths or changing implementation details, the more likely it belongs in a project note or backlog rather than a skill.
- Harness and loop engineering findings are good candidates for skillification only when they repeatedly show up as a reusable operating procedure.

## Best practices
- Keep the skill trigger short and specific.
- Put the common path first.
- Use progressive disclosure: body first, references second.
- Include pitfalls and verification.
- Split long supporting detail into reference files.
- Keep the skill narrow enough to stay discoverable.
- Make the output artifact explicit: skill, note, memory, or backlog.

## Do not dos
- Do not skill-ify a one-off incident too early.
- Do not use memory for procedures.
- Do not use backlog for stable facts.
- Do not bake project-only paths into a supposedly reusable skill.
- Do not create a megaskill that tries to own unrelated workflows.
- Do not flatten support files when packaging a skill.

## Emerging trends
- Skill systems are trending toward progressive disclosure and curator-managed lifecycle control.
- Self-improving agent systems increasingly treat reusable workflow packaging as a first-class behavior.
- The boundary between docs and skills is becoming clearer: notes describe context, skills describe procedure.
- Curator-style telemetry makes skill maintenance and consolidation more practical over time.

## Should we skill-ify it? rubric
Score each question 0-2.
- 0 = no / not yet
- 1 = partly
- 2 = yes

Questions:
1. Repeatability — has this happened more than once, or is recurrence likely?
2. Procedural shape — can the workflow be written as steps rather than just notes?
3. Portability — would it help in more than one project, profile, or session?
4. Tool-executability — can Hermes already perform it with existing tools?
5. Stability — is the workflow stable enough to document now?
6. Verifiability — can a future agent tell whether it worked?

Interpretation:
- 9-12: skill-ify
- 5-8: usually keep as a project note or backlog until it stabilizes
- 0-4: do not skill-ify yet

## Recommendation patterns
- Skill: reusable procedure with a stable trigger and a clear verification step.
- Project note: durable but project-specific context.
- Memory: stable fact, preference, or environment detail.
- Backlog: still-changing work or an implementation task that needs code first.

## Maintenance log
- 2026-06-12: created after researching Hermes skill authoring, curator behavior, and the harness/loop research notes.
