---
project_id: hermes
note_type: research-topic
updated_at: 2026-06-12T00:00:00Z
---
# Loop Engineering

## Scope
Loop engineering covers agent control loops, tool-use loops, reflection/review loops, retries, termination, guardrails, and multi-step orchestration.

## Search queries used
- `site:platform.openai.com/docs agent loops tool use guardrails retries termination criteria reflections 2025`
- `site:docs.anthropic.com tool use agents reflections guardrails retries computer use 2025`
- `site:langchain-ai.github.io/langgraph loops graph conditional edges retry termination guardrails 2025`
- `site:microsoft.github.io/autogen agent loop reflection termination tool use 2025`
- `site:google.github.io/adk agent loop orchestration termination guardrails 2025`
- `site:platform.openai.com/docs orchestrate handoffs agent builder control flow multi-agent 2025`
- `site:docs.langchain.com langgraph retry policy backoff max_attempts retry_on official`
- `site:docs.anthropic.com how tool use works agentic loop stop_reason tool_use official`
- `site:developers.openai.com/api/docs/guides/agents running agents state lastAgent resumable run loop`
- `site:docs.langchain.com/oss/python/deepagents overview planner subagents filesystem official`

## Sources reviewed
- OpenAI, Orchestration and handoffs
  - https://developers.openai.com/api/docs/guides/agents/orchestration
- OpenAI, Guardrails and human review
  - https://developers.openai.com/api/docs/guides/agents/guardrails-approvals
- OpenAI, Results and state
  - https://developers.openai.com/api/docs/guides/agents/results
- OpenAI Agents SDK, Running agents
  - https://openai.github.io/openai-agents-python/running_agents
- Anthropic, How tool use works
  - https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/how-tool-use-works
- Anthropic, Strict tool use
  - https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/strict-tool-use
- LangGraph, Persistence
  - https://docs.langchain.com/oss/python/langgraph/persistence
- LangGraph, Interrupts
  - https://docs.langchain.com/oss/python/langgraph/interrupts
- LangGraph, Fault tolerance
  - https://docs.langchain.com/oss/python/langgraph/fault-tolerance
- AutoGen, Reflection
  - https://microsoft.github.io/autogen/dev/user-guide/core-user-guide/design-patterns/reflection.html
- AutoGen, Termination
  - https://microsoft.github.io/autogen/0.4.5//user-guide/agentchat-user-guide/tutorial/termination.html
- Google ADK, LoopAgent
  - https://github.com/google/adk-docs/blob/main/docs/agents/workflow-agents/loop-agents.md
- Google ADK, SequentialAgent
  - https://github.com/google/adk-docs/blob/main/docs/agents/workflow-agents/sequential-agents.md
- Temporal blog, OpenAI Agents SDK integration
  - https://temporal.io/blog/announcing-openai-agents-sdk-integration

## Sources used in synthesis
- OpenAI Orchestration and handoffs
- OpenAI Guardrails and human review
- OpenAI Results and state
- OpenAI Agents SDK running agents
- Anthropic How tool use works
- Anthropic Strict tool use
- LangGraph persistence / interrupts / fault tolerance
- AutoGen reflection / termination
- Google ADK loop/sequential agents
- Temporal + OpenAI Agents SDK integration

## Knowledge developed
- Production loops should be bounded and explicit, not left to free-form prompting.
- Tool-use loops should be schema-first and strongly typed.
- Termination must be semantic plus budget-based, not just a max-turn cap.
- Durable execution, checkpoints, interrupts, and human-in-the-loop steps are increasingly native primitives.

## Best practices
- Make termination explicit and bounded.
- Separate transient failures from logic bugs in retry policy.
- Keep tool schemas strict and typed.
- Use checkpoints for loops that can pause, resume, or last more than one request.
- Treat approvals and interrupts as first-class control-flow primitives.

## Do not dos
- Do not let loops run without explicit termination criteria.
- Do not treat iteration caps as success.
- Do not retry control-flow signals or logic bugs as if they were transient errors.
- Do not pass untrusted text into privileged developer/system contexts.

## Emerging trends
- Loops are shifting from linear chains to graphs/workflows.
- Durable execution is becoming table stakes.
- Human-in-the-loop approvals are now native primitives.
- Planner + subagent + filesystem patterns are rising for long-horizon work.

## Open questions
- How many iterations should self-correction loops get before escalation?
- When is a critic loop better than a fresh replan?
- Where should durability live: inside the framework or in an external workflow engine?

## Maintenance log
- 2026-06-12: split from the combined research notebook.
