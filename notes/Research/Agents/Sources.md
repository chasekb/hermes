---
project_id: hermes
note_type: research-sources
updated_at: 2026-06-12T00:00:00Z
---
# Sources

Central source registry for the harness and loop research pages.

## Harness engineering sources
- OpenAI, Harness engineering: leveraging Codex in an agent-first world
  - https://openai.com/index/harness-engineering/
- OpenAI Docs, Evaluate agent workflows
  - https://developers.openai.com/api/docs/guides/agent-evals.md
- OpenAI Codex use case, Add evals to your AI application
  - https://developers.openai.com/codex/use-cases/ai-app-evals
- Anthropic, Demystifying evals for AI agents
  - https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- LangChain docs, Harness capabilities
  - https://docs.langchain.com/oss/python/deepagents/harness
- SWE-bench docs, The Harness
  - https://www.swebench.com/SWE-bench/reference/harness
- OpenTelemetry GenAI semantic conventions
  - https://opentelemetry.io/docs/specs/semconv/gen-ai/

## Loop engineering sources
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
- LangGraph, Persistence / interrupts / fault tolerance
  - https://docs.langchain.com/oss/python/langgraph/persistence
  - https://docs.langchain.com/oss/python/langgraph/interrupts
  - https://docs.langchain.com/oss/python/langgraph/fault-tolerance
- AutoGen, Reflection / termination
  - https://microsoft.github.io/autogen/dev/user-guide/core-user-guide/design-patterns/reflection.html
  - https://microsoft.github.io/autogen/0.4.5//user-guide/agentchat-user-guide/tutorial/termination.html
- Google ADK, LoopAgent / SequentialAgent
  - https://github.com/google/adk-docs/blob/main/docs/agents/workflow-agents/loop-agents.md
  - https://github.com/google/adk-docs/blob/main/docs/agents/workflow-agents/sequential-agents.md
- Temporal blog, OpenAI Agents SDK integration
  - https://temporal.io/blog/announcing-openai-agents-sdk-integration

## Source hierarchy
1. First-party runtime/docs from the system owner.
2. First-party benchmark or harness repos.
3. First-party research posts from the builders.
4. Maintained benchmark ecosystems and leaderboards.

## Maintenance log
- 2026-06-12: split from the combined research notebook.

## 2026-06-16 review addendum
- OpenTelemetry GenAI semantic conventions repository
  - https://github.com/open-telemetry/semantic-conventions-genai
  - Why it matters: the old GenAI semantic-conventions docs page now points here, so this is the canonical home for GenAI spans, metrics, events, and provider-specific conventions.
- LangChain docs, Harness capabilities
  - https://docs.langchain.com/oss/python/deepagents/harness
  - Why it matters: the page now explicitly groups harness behavior into execution environment, context management, delegation, and steering, including `interrupt_on` approvals.
- LangChain docs, Fault tolerance
  - https://docs.langchain.com/oss/python/langgraph/fault-tolerance
  - Why it matters: documents per-node retries/timeouts/error handlers plus resume-safe failures, default precedence, and graceful shutdown behavior.
- LangChain docs, Interrupts
  - https://docs.langchain.com/oss/python/langgraph/interrupts
  - Why it matters: makes checkpointed HITL interrupts concrete with thread IDs, JSON-serializable payloads, resume semantics, and idempotent pre-interrupt side effects.
- Google ADK, LoopAgent
  - https://raw.githubusercontent.com/google/adk-docs/main/docs/agents/workflow-agents/loop-agents.md
  - Why it matters: the deterministic LoopAgent still exists, but the docs now explicitly recommend graph-based or dynamic workflows in ADK 2.0 and require termination logic.
- Google ADK, Runtime Event Loop
  - https://raw.githubusercontent.com/google/adk-docs/main/docs/runtime/event-loop.md
  - Why it matters: clarifies the Runner/event loop contract, where agents yield events and resume only after the runtime processes them.
- Anthropic, Claude Fable 5 and Claude Mythos 5
  - https://www.anthropic.com/news/claude-fable-5-mythos-5
  - Why it matters: the launch post explicitly treats harness scaffolding as part of benchmarked capability measurement and notes that a minimal harness changed a hard coding benchmark outcome.

## 2026-06-18 review addendum
- OpenAI Docs, Evaluate agent workflows
  - https://developers.openai.com/api/docs/guides/agent-evals.md
  - Why it matters: the guide keeps the evaluation sequence explicit—start with trace grading for workflow debugging, then move to datasets and eval runs when you need repeatability.
- Temporal, Production-ready agents with the OpenAI Agents SDK + Temporal
  - https://temporal.io/blog/announcing-openai-agents-sdk-integration
  - Why it matters: the integration is in Public Preview and is a concrete example of putting durable execution outside the agent framework while keeping loop control in a workflow engine.

## 2026-06-19 review addendum
- OpenAI Docs, Orchestration and handoffs
  - https://developers.openai.com/api/docs/guides/agents/orchestration
  - Why it matters: it now explicitly separates delegated ownership (`handoffs`) from manager-style bounded specialist calls (`agent.asTool()`), and warns that over-splitting adds prompts, traces, and approval surfaces.
- LangGraph, Fault tolerance
  - https://docs.langchain.com/oss/python/langgraph/fault-tolerance
  - Why it matters: it makes retry-versus-error-handler ordering explicit, checkpoints failure provenance, clarifies that interrupts bypass retries/error handlers, and adds cooperative drain/shutdown semantics via `RunControl`.

## 2026-06-20 review addendum
- OpenTelemetry Semantic Conventions for GenAI repo, metrics and attributes
  - https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/gen-ai/gen-ai-metrics.md
  - https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/registry/attributes/gen-ai.md
  - Why it matters: adds dedicated `gen_ai.invoke_agent.duration` and `gen_ai.execute_tool.duration` histograms plus `gen_ai.request.reasoning.level`, which makes agent/tool boundaries and requested reasoning effort first-class telemetry.
- Google ADK docs, Evaluation overview and criteria
  - https://raw.githubusercontent.com/google/adk-docs/main/docs/evaluate/index.md
  - https://raw.githubusercontent.com/google/adk-docs/main/docs/evaluate/criteria.md
  - Why it matters: formalizes trajectory and tool-use evaluation separately from final-response quality, with both reference-based and rubric-based criteria for predefined datasets.

## 2026-06-21 review addendum
- OpenAI Docs, Results and state
  - https://developers.openai.com/api/docs/guides/agents/results
  - Why it matters: separates final output, replay history, continuation IDs, and resumable approval state, which makes continuation strategy a first-class loop concern.
- OpenAI Docs, Guardrails and human review
  - https://developers.openai.com/api/docs/guides/agents/guardrails-approvals
  - Why it matters: says approval interruptions can happen after handoffs or inside nested `agent.asTool()` calls, so human-review state must survive across multi-agent control flow.
- LangGraph, Fault tolerance
  - https://docs.langchain.com/oss/python/langgraph/fault-tolerance
  - Why it matters: documents `run_timeout` vs `idle_timeout`, progress signals, `refresh_on="heartbeat"`, and manual `runtime.heartbeat()` calls for long-running async nodes.

## 2026-06-22 review addendum
- LangGraph, Fault tolerance
  - https://docs.langchain.com/oss/python/langgraph/fault-tolerance
  - Why it matters: adds callable retry predicates, `node_attempt` inspection for fallbacks, structured `NodeTimeoutError` fields, and per-`Send` timeout overrides for fan-out tasks.
- OpenAI Agents SDK, Running agents
  - https://openai.github.io/openai-agents-python/running_agents
  - Why it matters: documents the `Runner` loop directly, including `RunState`-based resumption, `RunResultStreaming`, and explicit `max_turns`/`RunConfig` control surfaces.

## 2026-06-24 review addendum
- LangGraph, Fault tolerance
  - https://docs.langchain.com/oss/python/langgraph/fault-tolerance
  - Why it matters: now distinguishes `run_timeout` from `idle_timeout`, adds `refresh_on="heartbeat"` and explicit `runtime.heartbeat()` semantics, exposes `execution_info.node_attempt` even without retries, and returns structured `NodeTimeoutError` context for attempt-aware fallback handling.

## 2026-06-25 review addendum
- OpenAI Docs, Results and state
  - https://developers.openai.com/api/docs/guides/agents/results
  - Why it matters: now makes the result contract explicitly include replay-ready history, `lastAgent`/`lastResponseId` continuation surfaces, resumable approval snapshots, and richer run-item diagnostics for audits and debugging.
- LangChain docs, Fault tolerance
  - https://docs.langchain.com/oss/python/langgraph/fault-tolerance
  - Why it matters: clarifies that the default idle refresh mode is `refresh_on="auto"`, which resets on state writes, stream output, child-task scheduling, runtime writer calls, and callback events, while `refresh_on="heartbeat"` stays strict.

## 2026-06-26 review addendum
- OpenTelemetry Semantic Conventions for GenAI repo, invoke_agent/execute_tool attribute alignment
  - https://github.com/open-telemetry/semantic-conventions-genai/commit/48126929c29206df00303d37d761e9c3e8e8c9af
  - https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/gen-ai/gen-ai-metrics.md
  - Why it matters: aligns agent/tool boundary telemetry, keeps `gen_ai.agent.name` on tool spans, and removes `gen_ai.agent.version` from the internal invoke-agent span, which makes cross-boundary trace correlation cleaner.

## 2026-06-27 review addendum
- OpenAI Docs, Evaluate agent workflows
  - https://developers.openai.com/api/docs/guides/agent-evals.md
  - Why it matters: now explicitly tells code-first SDK workflows to start with Integrations and observability for high-signal traces before formalizing graders.
- OpenAI Docs, Integrations and observability
  - https://developers.openai.com/api/docs/guides/agents/integrations-observability
  - Why it matters: clarifies the SDK-specific tracing/observability loop and the boundary between SDK-managed MCP wiring and tool semantics.
- LangGraph, Fault tolerance
  - https://docs.langchain.com/oss/python/langgraph/fault-tolerance
  - Why it matters: documents `Send`-level timeout overrides for dynamic fan-out, so timeout provenance should be captured per push when evaluating long-running loops.

## 2026-06-29 review addendum
- OpenTelemetry Semantic Conventions for GenAI repo, Agent Framework reference scenario commit
  - https://github.com/open-telemetry/semantic-conventions-genai/commit/b028dceecdad117461a785c3af35315e7184e813
  - Why it matters: adds first-party Agent Framework coverage to the GenAI reference scenarios and extends the mock Responses server with function-call and usage-detail payloads, making the telemetry baseline broader and more realistic.

## 2026-06-30 review addendum
- LangGraph commit, snapshot `DeltaChannel` overwrite supersteps
  - https://github.com/langchain-ai/langgraph/commit/9a27693c64d3a0d6847dfe1c3d57e301cbf15bbf
  - Why it matters: snapshots delta channels after overwrite semantics are applied so sparse replay starts from the same post-overwrite value rather than a pre-overwrite mix.
- LangGraph commit, make `Overwrite` survive JSON roundtrips
  - https://github.com/langchain-ai/langgraph/commit/1b5ca0a1b1e1889879e43536fc5efd0739a3c479
  - Why it matters: preserves overwrite intent across JSON-serialized state updates by recognising the discriminator form emitted after dataclass erasure.

## 2026-07-02 review addendum
- OpenAI Agents SDK commit, enforce strict Pydantic validation when `strict_json_schema=True`
  - https://github.com/openai/openai-agents-python/commit/56921c89fc01a0bee60d5e2a1e3c698a22cde585
  - Why it matters: handoff and output validation now opt into strict Pydantic behavior when strict JSON schemas are enabled, which prevents silent type coercion at control-flow boundaries and makes schema failures easier to catch in harnesses.
- Anthropic cookbook notebook, Reproducing Claude's Agentic Search Benchmark Scores
  - https://raw.githubusercontent.com/anthropics/anthropic-cookbook/main/evals/agentic_search/reproduce_agentic_search_benchmarks.ipynb
  - Why it matters: shows that published DeepSearchQA and BrowseComp scores are reproducible on the public Messages API when the harness uses programmatic tool calling, server-side compaction, and explicit task budgets.
