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
- Google ADK docs, Evaluation overview and criteria
  - https://raw.githubusercontent.com/google/adk-docs/main/docs/evaluate/index.md
  - https://raw.githubusercontent.com/google/adk-docs/main/docs/evaluate/criteria.md
- OpenTelemetry Semantic Conventions for GenAI repo, metrics and attributes
  - https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/gen-ai/gen-ai-metrics.md
  - https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/registry/attributes/gen-ai.md
- Temporal blog, OpenAI Agents SDK integration
  - https://temporal.io/blog/announcing-openai-agents-sdk-integration

## 2026-06-29 review addendum
- OpenTelemetry Semantic Conventions for GenAI repo, Agent Framework reference scenario commit
  - https://github.com/open-telemetry/semantic-conventions-genai/commit/b028dceecdad117461a785c3af35315e7184e813
  - Why it matters: adds native Agent Framework coverage to invoke-agent-internal, inference, and execute-tool reference scenarios, which expands the first-party telemetry baseline loop designs should match.

## 2026-06-30 review addendum
- LangGraph commit, snapshot `DeltaChannel` overwrite supersteps
  - https://github.com/langchain-ai/langgraph/commit/9a27693c64d3a0d6847dfe1c3d57e301cbf15bbf
  - Why it matters: snapshots delta channels after overwrite semantics are applied so sparse replay starts from the same post-overwrite value rather than a pre-overwrite mix.
- LangGraph commit, make `Overwrite` survive JSON roundtrips
  - https://github.com/langchain-ai/langgraph/commit/1b5ca0a1b1e1889879e43536fc5efd0739a3c479
  - Why it matters: preserves overwrite intent across JSON-serialized state updates by recognising the discriminator form emitted after dataclass erasure.

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
- Google ADK evaluation overview and criteria
- OpenTelemetry Semantic Conventions for GenAI repo
- Temporal + OpenAI Agents SDK integration

## Knowledge developed
- Production loops should be bounded and explicit, not left to free-form prompting.
- Tool-use loops should be schema-first and strongly typed.
- Termination must be semantic plus budget-based, not just a max-turn cap.
- Durable execution, checkpoints, interrupts, and human-in-the-loop steps are increasingly native primitives.
- External workflow engines can own the durability layer for long-running agent loops: Temporal's Agents SDK integration frames Workflows as the control plane for loops, branching, and parallelism, while Activities hold the unpredictable calls.
- Loop telemetry is becoming more granular: OpenTelemetry now exposes separate agent-invocation and tool-execution duration metrics, plus a reasoning-level request attribute.
- Evaluation guidance is increasingly trajectory-aware: ADK's evaluation docs score tool-use trajectories separately from final responses, which makes loop shape itself an explicit benchmark target.
- OpenAI's results guide now makes result surfaces first-class loop inputs: continuation history, server-managed IDs, handoff ownership, and resumable approval state are distinct choices.
- LangGraph now documents progress-resetting idle timeouts and manual `runtime.heartbeat()` calls, which makes liveness signaling part of loop design for long-running async work.
- OpenAI's `Runner.run()` accepts a `RunState` for resuming interrupted runs, exposes streaming via `RunResultStreaming`, and keeps `max_turns` as an explicit loop budget.
- LangGraph now exposes attempt-aware retry hooks and per-push timeout overrides, which makes fallback selection and fan-out budgeting part of the loop design instead of hidden framework behavior.
- LangGraph now distinguishes automatic progress refresh from strict `refresh_on="heartbeat"` mode, so long-running nodes can choose whether only explicit `runtime.heartbeat()` calls reset the idle clock.
- `execution_info.node_attempt` is available even without a retry policy and defaults to `1`, which gives loop code an attempt counter for fallback selection.
- Loop telemetry is also getting more boundary-consistent in OpenTelemetry's GenAI conventions: `execute_tool` spans carry `gen_ai.agent.name` while `invoke_agent.internal` span and metric attributes are being aligned, so loop trace joins should use explicit agent identity rather than inferred ownership.
- LangGraph now documents dynamic `Send`-level timeout overrides for fan-out/map-reduce dispatch: a `Send` can tighten the target node's timeout for a specific push, and if omitted the static node timeout still applies.
- OpenTelemetry's GenAI reference repo now includes native Agent Framework coverage, which means loop telemetry validation has another first-party runtime emitting agent/tool/inference spans and usage details.
- LangGraph 1.2.7 fixes now preserve `Overwrite` semantics across JSON-serialized state updates and snapshot delta channels after overwrite supersteps, which makes replay correctness depend on both serialization shape and checkpoint timing.
- Anthropic's agentic-search cookbook shows that long-horizon loops need explicit task budgets, compaction-aware instructions, and in-sandbox tool calling to keep search state and grading behavior stable across dozens of tool turns.
- OpenAI Agents SDK handoff validation now respects strict JSON schema mode with strict Pydantic behavior, which reduces the risk of silent type coercion at control boundaries.

## Best practices
- Make termination explicit and bounded.
- Separate transient failures from logic bugs in retry policy.
- Keep tool schemas strict and typed.
- Use checkpoints for loops that can pause, resume, or last more than one request.
- Treat approvals and interrupts as first-class control-flow primitives.
- Use an external workflow engine when the loop must survive crashes, rate limits, or long pauses without losing orchestration state.
- Use retry metadata and per-call timeout overrides to tailor recovery and fan-out budgets, rather than treating every attempt identically.
- Resume interrupted runs from serialized run state when the framework exposes it, instead of rebuilding the loop from scratch.
- Use heartbeat-only idle refresh when you need strict liveness semantics; otherwise, understand which node activity resets the clock.
- For deep-research loops, keep model instructions about the question and answer format explicit through compaction so the post-compaction run does not lose the grading contract.
- Enforce strict schema validation on handoff inputs and outputs when the framework supports it, so control-flow coercion does not masquerade as success.

## Do not dos
- Do not let loops run without explicit termination criteria.
- Do not treat iteration caps as success.
- Do not retry control-flow signals or logic bugs as if they were transient errors.
- Do not pass untrusted text into privileged developer/system contexts.
- Do not rely on wall-clock time alone when the node can emit progress signals.

## Emerging trends
- Loops are shifting from linear chains to graphs/workflows.
- Durable execution is becoming table stakes.
- Human-in-the-loop approvals are now native primitives.
- Planner + subagent + filesystem patterns are rising for long-horizon work.
- Benchmark-driven loop design is increasingly centered on compaction, tool-call fan-out, and task budgets as first-class controls.

## Open questions
- How many iterations should self-correction loops get before escalation?
- When is a critic loop better than a fresh replan?
- Where should durability live: inside the framework or in an external workflow engine?

## Maintenance log
- 2026-06-12: split from the combined research notebook.
- 2026-06-16: LangGraph now documents per-node retries, timeouts, and error handlers alongside resume-safe failures and checkpointed interrupts; Google ADK's LoopAgent and runtime event loop reinforce deterministic workflows with explicit termination and event-driven resumption.
- 2026-06-18: Temporal's Agents SDK integration is in Public Preview and makes Durable Execution the headline loop primitive; LangGraph's fault-tolerance docs also make retry-policy precedence over error handlers explicit and keep clean stop/resume at superstep boundaries.
- 2026-06-19: LangGraph's fault-tolerance docs now spell out that retry policy runs before node-level error handlers, failure provenance is checkpointed, interrupts bypass both retries and error handlers, and cooperative shutdown via `RunControl.request_drain()` stops after the current superstep and resumes from a checkpoint; these controls require `langgraph>=1.2`.
- 2026-06-20: OpenTelemetry's GenAI semantic-conventions repo added dedicated agent/tool duration histograms and a requested reasoning-level attribute; Google ADK's conformance docs now make trajectory/tool-use quality a first-class loop-evaluation target.
- 2026-06-21: OpenAI's results guide now makes continuation surfaces explicit (`finalOutput`/`final_output`, history, `lastAgent`/`last_agent`, `lastResponseId`/`last_response_id`, and `interruptions` + `state`), and LangGraph's fault-tolerance docs add heartbeat-based idle timeouts for long-running async nodes.
- 2026-06-22: reviewed LangGraph fault-tolerance updates and the OpenAI Agents SDK running-agents guide; appended source-backed notes on callable retry predicates, attempt-aware fallbacks, per-send timeout overrides, `NodeTimeoutError` metadata, and `RunState`-based resumption with explicit `max_turns` and streaming surfaces.
- 2026-06-24: reviewed the current LangGraph fault-tolerance docs; appended source-backed notes on `refresh_on="heartbeat"`, manual heartbeat semantics, `execution_info.node_attempt`, and structured timeout behavior for long-running nodes.
- 2026-06-25: reviewed the current LangGraph fault-tolerance docs; appended source-backed notes on default `refresh_on="auto"` idle refresh signals, strict heartbeat-only mode, and `TimeoutPolicy`-based separation of run and idle timeouts for node attempts.
- 2026-06-26: reviewed the OpenTelemetry GenAI semantic-conventions repo alignment commit; appended source-backed notes on keeping agent identity consistent across `invoke_agent.internal` and `execute_tool` spans/metrics.
- 2026-06-27: reviewed refreshed LangGraph fault-tolerance docs; appended source-backed notes on `Send`-level dynamic timeout overrides for fan-out paths and preserving timeout provenance when dispatching work per item.
- 2026-06-29: reviewed the OpenTelemetry GenAI Agent Framework reference scenario commit; appended source-backed notes on the expanded native telemetry surface and function-call/usage-detail payloads.
- 2026-06-30: reviewed LangGraph 1.2.7 fixes; appended source-backed notes on JSON-roundtrip-safe `Overwrite` handling and delta-channel snapshot timing after overwrite supersteps.
- 2026-07-02: reviewed Anthropic's agentic-search benchmark reproduction cookbook and OpenAI Agents SDK strict handoff validation; appended source-backed notes on task budgets, compaction prompts, in-sandbox tool calling, and strict schema enforcement at loop boundaries.
