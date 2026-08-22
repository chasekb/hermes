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
- OpenAI's invalid-final-output recovery handler now lets loops recover from malformed or missing structured final output with a validated fallback, optionally skip history inclusion, and avoid another model turn when the handler resolves the error.
- LangGraph's fresh-thread `update_state` path now forces a self-contained snapshot checkpoint instead of creating a stub checkpoint, so the first checkpoint on a fresh thread should be treated as an inline snapshot rather than an ancestor-backed replay seed.
- Temporal's External Storage layer does not retry `Store` or `Retrieve` inside a single task attempt; storage failures fail the task attempt and the whole task is retried, so storage calls need to be designed inside the outer task retry boundary.
- Google ADK's `output_key` behavior now reads as root-agent scoped: the key is updated when the root agent itself produces the final response, but a delegated sub-agent's final message does not trigger `output_key` on that turn.
- OpenAI's Chat Completions compatibility path now explicitly closes provider streams on early exit, so loop cancellation should be treated as a teardown path rather than a garbage-collection assumption.
- OpenAI's realtime session cleanup now treats close as a distinct phase, waits briefly for tracked guardrail/tool tasks, and shields cleanup so model transport closes only after background work settles.
- OpenAI's `agent.as_tool` docs now make nested state ownership explicit: the parent run does not inherit conversation state automatically, so client-managed history requires the same `session` on both sides, while server-managed continuation should use `previous_response_id` or `conversation_id`.
- Temporal's TypeScript OpenAI Agents integration now documents `stream: true`, `WorkflowStream`, and `WorkflowStreamClient`, and states that streaming from within the Workflow is replay-safe.

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
- When the framework exposes structured-output recovery, prefer a validated fallback handler over blind reruns, and decide explicitly whether the recovered output belongs in history.
- On a fresh thread, assert the resulting state-history shape after `update_state` and do not depend on a stub checkpoint for replay.
- Treat storage calls as part of the outer task retry boundary, and make them idempotent.
- If a delegated sub-agent may produce the visible final turn, persist the value explicitly instead of relying on `output_key`.
- When the loop can exit early, verify provider streams are closed via `aclose` or `close` and do not rely on implicit cleanup.
- Treat teardown and nested state ownership as explicit loop design choices, not incidental framework behavior.
- For streamed durable workflows, separate replay-safe workflow orchestration from the live client subscription surface.

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
- Replay shape and retry semantics are getting more granular: the same framework may now distinguish a fresh-thread snapshot from a replay-backed checkpoint, and a durability layer may retry the whole task rather than the inner storage call.

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
- 2026-07-04: reviewed OpenAI provider/config and models docs; appended source-backed notes on strict feature validation for Chat Completions fallback, streamed tool-call buffering, and the fact that provider selection can alter loop-visible state surfaces.
- 2026-07-06: reviewed the OpenAI Agents SDK invalid-final-output recovery handler commit; appended source-backed notes on validated fallback outputs, optional history exclusion, and no-extra-turn recovery for malformed structured outputs.
- 2026-07-07: reviewed LangGraph's fresh-thread snapshot fix, Temporal's external-storage retry note, and Google ADK's `output_key` clarification; appended source-backed notes on inline first checkpoints, task-attempt retry boundaries, and root-agent-scoped final-response persistence.
- 2026-07-08: reviewed OpenAI Agents SDK nested tool-state restoration and Google ADK collaboration/A2A updates; appended source-backed notes on action-bound nested replay state, delegation-tool naming, `finish_task` task return semantics, and A2A reasoning/long-running-tool/artifact capabilities.
- 2026-07-08: reviewed OpenAI Agents SDK Chat Completions early-exit cleanup; appended source-backed notes on explicit stream teardown, async `aclose`/`close` handling, and cancellation-safe loop cleanup.
- 2026-07-09: reviewed OpenAI Agents SDK realtime session cleanup and tool-state docs plus Temporal's TypeScript OpenAI Agents integration update; appended source-backed notes on deterministic teardown, explicit nested state ownership, and replay-safe workflow streaming.
- 2026-07-10: reviewed OpenAI Agents SDK 0.18.1 and same-day commits plus LangGraph 1.2.9; appended source-backed notes on run-scoped model cleanup, owned sandbox/PTY deferred tasks, monotonic realtime timing, hosted-subagent/local-tool control boundaries, and delta-channel checkpoint counters for non-fresh state updates.
- 2026-07-11: OpenAI Agents SDK 0.18.2 released serialized model-backed rollout interruptions, and Google ADK tightened loop boundaries: callback failures no longer replace the original run error, toolset cleanup is shielded from caller cancellation, dynamic workflow schedulers have explicit ownership/lifetime, and `ManagedAgent(mode='single_turn')` is an inline tool rather than a transfer target. Loops should model notification, cleanup, scheduler, and delegation failures as distinct control paths.

## 2026-07-12 review addendum
- Google ADK now awaits synchronous code-executor calls through `asyncio.to_thread` in both request pre-processing and response post-processing, with tests proving the executor runs off the event-loop thread while another coroutine proceeds. Loop designs should treat blocking tools as explicit scheduler boundaries and test that they cannot starve unrelated async work.
- OpenAI Agents SDK now raises `UserError` for conflicting provider constructor arguments instead of using assertions. Loop setup should fail deterministically in optimized production interpreters rather than silently accepting ambiguous client/API-key or endpoint configuration.

## Maintenance log
- 2026-07-12: reviewed Google ADK's synchronous-code-executor offload and OpenAI Agents SDK's optimization-safe provider validation; appended source-backed notes on non-blocking tool boundaries and deterministic setup failures.
- 2026-07-13: reviewed OpenAI Agents SDK's serialized conversation-session initialization and handoff-history parsing fixes plus Google ADK's shared rewind filtering; appended source-backed notes on single-flight lazy session creation, strict assistant-history wrapper recognition, and treating rewind application as a shared loop-state transformation before compaction.

## 2026-07-13 review addendum
- OpenAI's conversation-backed session now serializes first-session creation with an async lock and double-check, so concurrent first writes share one conversation; failed initialization remains retryable for a later writer. Loop implementations with lazy remote state should use a single-flight initialization boundary and test recovery after the initializer fails.
- OpenAI's handoff-history parser now requires assistant-role content, an accepted preamble, exact wrapper placement, and a complete wrapped body before treating text as generated nested history. This prevents user-provided or ordinary assistant text containing wrapper markers from being flattened as control state; loop tests should cover literal-marker and trailing-text cases.
- Google ADK's rewind helper now feeds both prompt building and token/sliding-window compaction, preventing annulled invocations from leaking into summaries and later prompts. Rewind markers should be modeled as state transformations with one canonical implementation, not as a prompt-only filter.

## 2026-07-14 review addendum
- Google ADK's Gemini context-cache manager now converts a zero-length cacheable conversation prefix to `None` before constructing `CreateCachedContentConfig`, because the GenAI SDK rejects an explicit empty `contents=[]` even though omitted contents are valid when system instructions or tools supply the cacheable material. Loop/cache tests should distinguish omitted state from an explicit empty collection and verify that a failed cache creation remains retryable rather than corrupting fingerprint-only metadata.

## Maintenance log
- 2026-07-14: reviewed Google ADK's Gemini context-cache empty-prefix fix; appended notes on omission-versus-empty state at the model-cache boundary and retry-safe cache metadata.

## 2026-07-15 review addendum
- Google ADK's workflow replay manager now builds direct and transitive event indexes, refreshes them when the session event count changes, routes interrupt responses by function-call ID, and uses the filtered events for rehydration and sequence barriers. Long-running loop tests should cover multi-turn event growth, descendant recovery, interrupt-response routing, and chronological replay—not only successful fresh execution.
- Google ADK's Gemini cache manager now fingerprints the model and cache backend namespace, canonicalizes serialized request mappings, and records the API's returned expiration timestamp when present, falling back to the requested TTL only when the server omits it. Loop/cache state should invalidate on model or backend changes and should not schedule reuse from a client-side expiry estimate when authoritative server metadata exists.
- Google ADK's config validation now rejects OS and socket aliases, including private implementation modules. Agent loops that resolve code references from configuration should treat module allow/deny validation as a control boundary and test optimized/private import paths.

## Maintenance log
- 2026-07-15: reviewed Google ADK workflow rehydration, cache-scope/expiry, and config-validation changes; appended notes on indexed replay, authoritative cache lifetime, and alias-complete control-boundary validation.

## 2026-07-21 review addendum
- OpenTelemetry's replacement of `gen_ai.agent.steps` with `gen_ai.invoke_agent.inference_calls` and `gen_ai.invoke_agent.tool_calls` makes loop budgets more portable: loop telemetry should count model and tool calls per agent invocation rather than mapping framework-specific turns, supersteps, or handoffs into one "step" counter.
- Google ADK live mode now accepts an optional `state_delta` on `LiveRequest` and applies it as a separate state-delta event regardless of whether the request carries content, partial output, or a function response. Live loops can seed or update session state alongside bidirectional input, but replay tests should assert that state updates are represented as their own events.
- Google ADK now resolves `ManagedAgent.instruction` and forwards it as `system_instruction` on every Managed Agents API turn, including chained turns; string instructions get placeholder state injection while callable providers bypass injection. Delegation loops should treat managed-agent instruction propagation as an explicit control boundary and test state-placeholder behavior.
- Google ADK now reuses one event ID for all partial chunks in a streamed LLM response and remints only after a complete event. Loop consumers should aggregate streaming chunks by event ID and avoid executing or persisting partial chunks as independent session events.
- Temporal's new Go SDK Google ADK integration page documents deterministic ADK loop execution via `googleadk.NewContext`, Activity-backed tools via `ActivityAsTool`, durable human confirmation signals, continue-as-new session snapshots, and replay-safe streaming where model chunks are published to workflowstreams while the aggregated final response returns to the Workflow. External durability designs can now compare OpenAI Agents and Google ADK integrations across the same Temporal workflow/activity separation pattern.
- OpenAI Agents SDK v0.18.3 fixes streamed local-session retries so committed user input is owned by the run rather than a single model attempt, and fixes server-managed conversation tracking after input filters rebuild prepared items. Retry and continuation loops should verify that current-turn input is neither popped nor resent across model retries or object-ID reuse.

## Maintenance log
- 2026-07-21: reviewed OpenTelemetry per-invocation call-count metrics, Google ADK live-state, streaming, ManagedAgent, and rubric commits, Temporal's Go Google ADK integration docs, and OpenAI Agents SDK v0.18.3 retry/conversation fixes; appended notes on portable loop budgets, event-mode state deltas, managed-agent instruction propagation, streaming aggregation identity, durable workflow integration, and retry-safe continuation state.

## 2026-07-22 review addendum
- Google ADK now copies `RunConfig.custom_metadata` into `InvocationContext._custom_metadata` during model post-initialization, making run-scoped custom metadata available to tools through the invocation context. Loop code that relies on tenant, policy, or harness metadata should assert propagation into tool execution rather than only into top-level run configuration.
- Google ADK's A2A artifact-update converter now reconstructs event-level metadata such as grounding metadata, custom metadata, usage metadata, citation metadata, and error code from artifact metadata, with fallback to `None` for malformed payloads. Cross-agent loops should treat A2A metadata as replay state and test both valid round-trips and malformed-metadata fail-soft behavior.
- Google ADK's A2A converters now serialize Pydantic metadata and parts with `model_dump(mode="json")`, so raw bytes such as computer-use screenshots become JSON-safe/base64 strings before entering protobuf `Struct`. Loops that move multimodal tool outputs across A2A should test byte-bearing function responses instead of assuming text-only payloads.
- Google ADK now preserves `EventActions.requested_tool_confirmations` through session-service serialization/deserialization, fixing production resumption of requested tool confirmations. Approval loops should include persisted-session resume tests for dynamic tool confirmations and their payloads.
- OpenAI's sandbox mount boundary makes remote mounts create-time-only by default and treats ambiguous privileged mount transitions as a stop condition rather than reconciliation state. Long-running tool loops should avoid inventing dynamic mount-repair loops unless a provider explicitly advertises that capability.

## Maintenance log
- 2026-07-22: reviewed Google ADK RunConfig metadata, A2A converter, and tool-confirmation fixes plus OpenAI sandbox mount semantics; appended notes on metadata propagation, A2A replay/byte payloads, approval resumption, and avoiding implicit mount-reconciliation loops.

## 2026-07-23 review addendum
- OpenAI Agents JS now fails closed when dynamic tool approval receives malformed JSON or non-object arguments: it requests approval without invoking the dynamic `needsApproval` policy or the tool, and realtime execution sends a parse-error function output only after approval. Approval loops should treat argument parseability/object-shape as a pre-policy control boundary, especially when approval policies inspect arguments.
- OpenAI Agents JS now preserves assistant message `phase` (`commentary` or `final_answer`) across Responses history, run-state serialization, model responses, and OpenAI conversation replay; Chat Completions compatibility warns or errors under strict validation because the phase is not supported there. Loop replay should preserve intermediate-versus-final assistant phases when the provider supports them and record when compatibility layers drop that state.
- OpenAI Agents Python now cleans MCP servers that are cancelled during connect, and the failure path no longer depends on context-manager exit running after `__aenter__` fails. Loops that connect multiple MCP servers should model partial-connect cancellation as a teardown path with per-server cleanup guarantees.
- Google ADK's automatic function-calling utility now degrades gracefully for Vertex AI return types whose response schema cannot be derived: it logs a warning, omits only the response schema, and preserves parameter schemas; valid Pydantic return types still keep response schemas. Tool loops should distinguish unsupported return-schema metadata from invalid tool declarations so usable tools are not rejected unnecessarily.
- Google ADK's lazy-loading change keeps requested auth configs parseable through a field validator while avoiding eager import of heavy auth dependencies. Long-running loop state should still validate auth-config payloads on deserialize even when runtime modules are loaded lazily.
- Temporal's Google ADK integration docs now present `googleadk.NewPlugin` as the standard worker setup: the plugin registers model/MCP activities at worker start, closes cached MCP toolsets at worker stop, keeps Gemini credentials behind the Activity boundary, and leaves the model SDK's own retries disabled so Temporal `RetryPolicy` remains authoritative. External durability loops should treat worker plugin lifecycle as part of loop resource ownership.
- Anthropic's live subagent cookbook exposes per-thread `event_deltas` for coordinator/subagent teams. Loop consumers should aggregate progress by delegated thread rather than assuming the primary session stream is the complete loop transcript.

## Maintenance log
- 2026-07-23: reviewed OpenAI Agents JS dynamic-approval and assistant-phase fixes, OpenAI MCP cleanup, Google ADK Vertex schema and lazy-loading changes, Temporal Google ADK plugin docs, and Anthropic live subagent streaming; appended notes on fail-closed approval, provider-supported replay phase state, partial-connect teardown, schema-degradation boundaries, lazy validation, plugin lifecycle, and per-thread progress streams.

## 2026-07-24 review addendum
- OpenAI Agents Python moved session rewind on model retry under the retry branch, with non-streamed memory and SQLite regression tests proving committed session input is not rewound when no retry occurs. Retry loops should scope rewind state to actual retry attempts and assert current-turn input/history preservation across both streamed and non-streamed providers.
- OpenAI Agents Python now surfaces `finish_reason="content_filter"` as a synthesized refusal event even when streamed Chat Completions tool-call buffering emits no content, preventing a safety block from becoming a silent empty turn. Loop consumers should treat refusals as terminal/safety events with explicit completion, not as missing output.
- OpenAI Agents Python now encodes SDK-generated programmatic tool errors as provider-compatible JSON objects when structured tool output is expected, while preserving plain text for direct function-tool errors. Tool loops with structured outputs should parse and route typed error objects instead of assuming all error paths are strings.
- OpenAI Agents Python strict-schema validation now rejects empty `additionalProperties` mappings and non-empty schemas unless the value is explicitly `false`. Loop setup should fail closed on schema forms that allow arbitrary keys, including OpenAPI/MCP-style `additionalProperties: {}`.
- Google ADK now skips partial streaming `transfer_to_agent` function calls when resuming invocations, because such partial events are display-only and should not be replayed as persisted control state. Resumable delegation loops should filter partial streaming control calls before transfer short-circuit logic.
- Google ADK's VertexAiSessionService now applies `after_timestamp` and `num_recent_events` together rather than letting one filter override the other. Replay/windowed-session loops should test combined temporal and recency filters so resumptions do not include stale or excessive event history.
- Google ADK's AnthropicLlm now maps Anthropic stop reasons into `finish_reason` on both streaming and non-streaming responses. Provider-agnostic loop termination should consume normalized finish reasons rather than relying on provider-specific stop-reason fields.
- OpenTelemetry's `gen_ai.request.previous_response.id` attribute gives loop traces a portable way to represent provider-managed continuation links. Continuation loops should emit this attribute whenever they pass a previous response or interaction ID so replay/debug tooling can follow turn lineage.

## Maintenance log
- 2026-07-24: reviewed OpenAI Agents Python retry/session, content-filter, programmatic-tool-error, and strict-schema fixes; Google ADK replay, session-filter, and finish-reason fixes; and OpenTelemetry continuation-ID telemetry. Appended notes on retry-scoped rewinds, explicit safety refusals, structured tool errors, schema fail-closed setup, partial-transfer filtering, combined session windows, normalized termination reasons, and portable continuation lineage.

## 2026-07-25 review addendum
- Google ADK's tool-confirmation flow now treats the continuation response as a capability-bound control signal: it resolves the original function call from session history, skips calls authored by another agent, validates registered tool membership, re-evaluates static or dynamic confirmation requirements with `ToolContext`, and rejects name or argument tampering before executing the tool. Approval loops should bind confirmations to historical function-call identity and agent ownership, not just to a user-supplied `originalFunctionCall` payload.
- Google ADK now rejects transport `base_url` and arbitrary `extra_body` overrides in `LlmAgent.generate_content_config` because extra bodies can overwrite tools, system instructions, and response schemas. Loop setup should keep transport/client selection and privileged request-body mutation outside ordinary agent config while preserving safe per-request settings such as timeout.
- OpenAI Agents Python's realtime and RunState diagnostic changes remove event IDs, event types, item types, agent names, and raw diagnostic arguments from logs when sensitive model/tool data logging is disabled. Replay and resume loops should treat diagnostics as another state-export surface and verify that state-deserialization warnings and realtime validation failures respect the same privacy boundary as traces.
- OpenAI Agents Python now rejects unsupported streamed-STT numpy dtypes before encoding audio and now parses device nodes from sandbox listings as size-zero `OTHER` entries. Voice and sandbox tool loops should validate input representation and filesystem enumeration edge cases before handing work to provider or archive layers.
- LangGraph's v3 event streaming now exposes typed run handles and always-present native projections for values, messages, lifecycle, and subgraphs. Loop consumers that multiplex graph streams should use these projections as stable consumption surfaces and reserve `extensions` for opt-in channels such as updates, checkpoints, debug, custom, and tasks.
- Temporal's Java Workflow Streams documentation now mirrors the durable streaming pattern for another SDK: create `WorkflowStream` once, preferably in a `@WorkflowInit` constructor so first-task polls and offset queries are accepted; publish events from workflows, activities, or clients; subscribe via blocking or non-blocking APIs; and carry `WorkflowStreamState` across continue-as-new for long-lived workflows. Durable agent loops that expose live progress can now compare Java alongside Go and TypeScript workflow-stream patterns.

## Maintenance log
- 2026-07-25: reviewed Google ADK confirmation/config fixes, OpenAI diagnostics/voice/sandbox fixes, LangGraph v3 streaming type commit, and Temporal Java Workflow Streams docs; appended notes on capability-bound confirmations, privileged config isolation, privacy-safe diagnostics, representation validation, typed graph stream consumption, and durable Java stream state.

## 2026-07-26 review addendum
- OpenAI Agents Python now supports async callable objects directly as function tools and preserves positional context handling for callable-object `__call__` methods. Tool-use loops can therefore treat callable instances as first-class tools, but should validate generated name safety, schema shape, context stripping, and unsupported annotations before entering the run loop.
- OpenAI Agents Python added regression coverage ensuring live `ToolContext` values are not included in tool-argument debug logging when a context-bearing function tool is invoked. Loop logging should distinguish model-supplied tool arguments from runtime context objects so enabling tool-data logs does not accidentally export live context secrets.
- Google ADK now allows `http_options.extra_body` inside `LlmAgent.generate_content_config` while still rejecting `http_options.base_url`. This narrows the 2026-07-25 privileged-config conclusion: loop setup should continue to fail closed on transport endpoint overrides, but should not assume every `extra_body` use is invalid after the follow-up fix.
- Google ADK's BigQuery plugin tests now replace fixed sleeps with `flush()` and repair cross-event-loop startup tests so threads race only on `_ensure_started`, not on non-thread-safe mock patching. Long-running loop observability tests should use explicit writer barriers and avoid introducing test-harness races that can be mistaken for runtime coalescing bugs.

## Maintenance log
- 2026-07-26: reviewed OpenAI Agents Python callable-tool/logging fixes and Google ADK config/analytics race-test commits; appended notes on callable-instance tool-loop boundaries, context-safe tool logging, narrower `extra_body` policy, explicit telemetry drains, and race-free cross-loop startup harnesses.

## 2026-07-27 review addendum
- OpenAI's Programmatic Tool Calling guide introduces a hosted inner loop where the model writes JavaScript that can run tool calls in parallel, use loops/conditions, keep intermediate results in an isolated fresh V8 runtime, and emit compact text/image outputs. Loop designs should use this only for bounded, predictable stages with explicit stop conditions, retry limits, documented input/output fields, idempotent calls, and structured failures; direct tool calls remain preferable when each result needs fresh model judgment or approval/native-artifact validation.
- Programmatic Tool Calling continuation is a nested loop contract: the application executes returned client-owned `function_call` items, returns `function_call_output` with the original `call_id` and unchanged `caller`, continues if no final message appears, and for `store: false` replays the complete ordered sequence of `program`, reasoning, function-call, function-call-output, and `program_output` items. Loop replayers should treat `caller` and program fingerprints as control state, not as incidental trace metadata.
- OpenAI Agents Python's v0.19.0 release states that `ProgrammaticToolCallingTool` integrates with Runner streaming, guardrails, approvals, sessions, and `RunState`. Programmatic-tool loops should test pause/resume through approvals and sessions, and should separate hosted JavaScript orchestration from client-owned tool execution and authorization checks.
- OpenAI Agents Python now marks pre-response Responses WebSocket `server_is_overloaded` errors as retryable while keeping partial/unsafe overloads non-retryable. Retry loops should distinguish overloads before response start from errors after output has begun, preserving replay-safety metadata instead of retrying all WebSocket failures uniformly.
- OpenAI Agents Python now uses the `last_agent` property when building streaming run error details and returns no detail object if the weakly referenced current agent has been collected, preserving the original terminal exception instead of crashing error-detail construction. Streaming closeout loops should tolerate released agent references and keep terminal exceptions primary.
- OpenAI Agents JS now propagates non-streaming run cancellation into function-tool execution, waits for cancelled stream background cleanup before resolving `completed`, and persists a checkpoint if cancellation occurs after tool resolution or interrupted-turn resolution. JS loop designs should treat cancellation as a stateful teardown path with abort-aware tools, incomplete synthetic tool results, and persistence checkpoints—not just as reader closure.

## Maintenance log
- 2026-07-27: reviewed OpenAI Programmatic Tool Calling docs, OpenAI Agents Python v0.19.0 and retry/error-detail/function-schema fixes, and OpenAI Agents JS cancellation/refusal fixes; appended notes on hosted programmatic inner loops, caller-preserving continuation/replay, approval/session integration, pre-response overload retry boundaries, weakref-safe streaming error details, and stateful cancellation teardown.

## 2026-07-28 review addendum
- OpenAI Agents Python now allows an empty streamed model input list to reach the model. Loop implementations should distinguish an intentionally empty turn from missing prepared input, especially after input filters, server-managed continuation, or replay state reconstruction.
- OpenAI Agents Python now cancels parallel input-guardrail work if the model turn fails before the guardrail completes. Loops that run model calls and guardrails concurrently should make sibling-task cancellation part of their failure protocol so late guardrail results do not mutate state after a terminal model error.
- OpenAI Agents Python's falsey-provider fix means loop setup should route explicitly by provider existence, not truthiness. Custom provider objects that define `__bool__` should not alter model-routing control flow.
- OpenAI Agents JS now propagates cancellation to streamed function tools and MCP tool requests, combines abort signals for MCP calls, avoids starting new work after a streamed cancellation once a turn has begun, preserves owned sandbox sessions for resumable streamed cancellation, and waits for cancelled stream cleanup before `completed` resolves. JS loop designs should treat cancellation as an abort-signal propagation tree with resumable state preservation, not just a reader-side stop.
- Google ADK now scopes workflow replay sequences to the current invocation even though the event index spans the full session, preventing terminal events from prior invocations from polluting a resumed invocation's sequence. Replay loops should filter by invocation ID after building session-wide context indexes.
- Google ADK now isolates delegated task branches by assigning each task a stable sub-branch while keeping `isolation_scope` keyed by the function-call ID. Delegation loops should persist branch identity separately from isolation scope so resumable task-mode subagents see only their own function calls.
- Google ADK now raises `SessionNotFoundError` when appending to a missing session across Firestore, database, and SQLite session services. Loop recovery code should handle missing-session append as a typed state-loss condition rather than a generic value error.
- Google ADK's Discovery Engine search tool now detects and caches search-result mode under a single-flight lock. Tool loops that auto-detect backend mode should coalesce concurrent detection attempts and cache successful or fallback mode decisions rather than racing duplicate probes.

## Maintenance log
- 2026-07-28: reviewed OpenAI Agents Python/JS loop commits and Google ADK replay/session/delegation/tool commits; appended notes on empty-turn streaming, sibling guardrail cancellation, truthiness-safe provider routing, abort propagation to function/MCP tools, current-invocation replay scoping, delegated branch identity, typed missing-session failures, and single-flight backend mode detection.

## 2026-07-29 review addendum
- OpenAI Agents Python now completes the cancellation symmetry around parallel guardrails and model work: the prior fix cancelled input-guardrail work when the model failed, and the new streamed-run fix cancels streamed model work when an input guardrail fails first. Loop tests should cover both race orderings and assert that no sibling task can continue mutating state after the winning failure path has terminated the turn.
- OpenAI Agents Python now cancels sibling enablement checks when one check fails across function-tool preparation, realtime tool filtering, handoffs, model settings, and sessions. Loop setup should treat enablement as a fail-fast fan-out phase with explicit sibling cancellation, not as independent background checks that may outlive the failed control boundary.
- OpenAI Agents Python now honors falsey custom input builders for `agent.as_tool`, extending the recent falsey-provider lesson to nested-agent input adaptation. Loop configuration should test existence by `is not None` for provider, builder, and mount-like knobs rather than truthiness.
- OpenAI Agents Python now counts streamed retries even when the terminal streamed result lacks usage metadata. Retry loops should increment attempt/retry state from retry control flow rather than from usage-bearing terminal events alone.
- OpenAI Agents Python's valid-item SQLite session limit fix changes replay-window semantics: loops using positive recency limits should count replayable session items after validity filtering, not raw storage rows.
- OpenAI Agents JS now preserves verified Docker sandbox sessions across resumes with explicit session-state trust validation, and its path-grant fixes support native Windows paths plus Docker workdirs inside granted roots. Resumable tool loops should separate persisted sandbox state from verified trust state and re-check path grants before reusing a session.
- Google ADK now scopes tool thread pools to the event loop they serve and shuts them down when that loop is collected, while Vertex RAG memory now uses async client calls and closes clients in `finally`. Long-running loops should treat executor pools, RAG clients, and sandbox clients as loop-owned resources with event-loop-local lifetime and cancellation-safe closeout.
- Google ADK's CLI telemetry consent update handles `KeyboardInterrupt` and `EOFError` by defaulting telemetry off for the current session without writing persistent config. CLI loops that prompt for preferences should treat interruption as a safe local default, not as consent or persisted state.

## Maintenance log
- 2026-07-29: reviewed OpenAI Agents Python guardrail/model and enablement-check cancellation commits, falsey input-builder and retry-accounting fixes, OpenAI Agents JS sandbox resume/path-grant fixes, and Google ADK threadpool/RAG/client/CLI commits; appended notes on cancellation symmetry, fail-fast fan-out setup, truthiness-safe configuration, retry counters, valid replay windows, sandbox trust state, event-loop-scoped resources, and interrupt-safe telemetry consent.

## 2026-07-30 review addendum
- Google ADK now exposes an `elicitation_callback` on `McpToolset`, forwards it through `MCPSessionManager` and `SessionContext`, and documents it for MCP `elicitation/create` requests including URL-mode out-of-band flows such as auth challenges. MCP-enabled loops should model elicitation as a first-class pause/response control path, separate from sampling, progress callbacks, tool confirmation, and ordinary tool results.
- Google ADK's OpenAPI OAuth2 credential exchanger now detects expired OAuth2 credentials and refreshes them in place when a refresh token exists; if session creation or refresh fails, it logs a warning and falls back to the existing token rather than replacing it. Authenticated tool loops should test expired-token refresh success, refresh failure fallback, missing refresh tokens, and redaction-safe logging so auth recovery does not corrupt credential state.
- Google ADK's DataAgentToolset now parses Data Agent locations from resource names when settings omit location, supports EU/US REP and regional endpoint routing, and accepts an explicit API endpoint override; the Apigee LLM client now applies per-request HTTP timeouts to both regular POSTs and streaming requests. Tool loops should treat location/endpoint selection and timeout propagation as part of loop setup and failure provenance, especially for regional compliance or latency-sensitive runs.
- Google ADK's streaming aggregator and audio cache now avoid quadratic accumulation by joining chunk lists once. Long-running multimodal loops should test high-chunk streaming and audio flush paths under realistic sizes, because inefficient accumulation can become a hidden termination or timeout failure mode.
- Google ADK's CLI telemetry now groups commands by parent terminal with inactivity-based TTL pruning and logs executed subcommands/flags when telemetry is enabled. CLI-driven loops should keep telemetry consent, interrupt/default-off behavior, session grouping, and command metadata capture as explicit state boundaries rather than accidental side effects of command execution.

## Maintenance log
- 2026-07-30: reviewed Google ADK MCP elicitation, OAuth2 refresh, DataAgent endpoint routing, Apigee timeout, streaming aggregation, and CLI telemetry commits; appended notes on elicitation as a loop control path, credential-refresh fallback, regional endpoint provenance, high-chunk streaming complexity, and CLI telemetry state boundaries.

## 2026-07-31 review addendum
- OpenAI Agents Python voice streaming now propagates consumer cancellation instead of swallowing it, closes STT websockets on cancellation, blocks the audio dispatcher while idle without spinning, and exits dispatch when a stream task emits `session_ended`. Voice loops should model cancellation, idle wait, stream failure, and session-ended as explicit closeout paths rather than relying on queue polling or downstream garbage collection.
- OpenAI Agents Python now preserves raw realtime server events while validating normalized copies. Realtime loop code should avoid mutating raw provider payloads in-place when adapting them for SDK compatibility, because raw events are replay and audit state.
- OpenAI Agents Python now cleans failed MCP servers before reconnecting and redacts URL credentials across SDK error, tracing, tool-origin, and nested cleanup surfaces. MCP loops should treat reconnect as a cleanup-then-retry transition and preserve sanitized server identity separately from live connection secrets.
- OpenAI Agents Python now enforces Redis and Dapr session closed state, idempotent close, and owned-client release; it also makes positive recency limits count valid items after corrupt entries are skipped. Durable memory loops should treat close as terminal for the session object and count replay windows over valid conversational items, not raw backend records.
- OpenAI Agents Python now preserves tagged sandbox `EnvValue` subclasses and rejects ephemeral paths during Modal tar hydration. Sandbox loops should preserve environment-value discriminators across manifest serialization and fail closed when restored archives try to materialize excluded/ephemeral paths.
- OpenAI Agents Python now exposes the original callable behind a wrapped function tool and keeps keyword-collision parameter names during output trimming. Tool loops and diagnostics can map generated schemas back to source callables, but should test that trimming and wrapping do not change callable argument shape.
- Google ADK now threads `App` plugins into eval execution paths. Evaluation loops should include plugin side effects and lifecycle hooks when replaying or generating eval cases, not bypass them by resolving only the root agent.
- Google ADK now serializes exact event timestamps, uses stored payload epochs over naive datetime conversions, tie-breaks equal timestamps by event ID, and honors `num_recent_events=0` in Vertex sessions. Replay loops should distinguish `0` from unset, preserve timestamp epochs through DST ambiguity, and keep tied-event ordering deterministic.
- Google ADK's tool-confirmation flow now stops re-validating confirmations that have already been consumed. Approval loops should persist consumption state and avoid reprocessing accepted confirmations on later request-building passes.
- Google ADK code executors now kill timed-out code process groups for both container and unsafe-local executors. Tool-use loops that run code should treat timeout as a hard resource cleanup boundary, including subprocesses spawned by the model's code.
- Google ADK's `set_model_response` path now returns schema-validation feedback to the model instead of accepting invalid structured output. Structured-output loops can make validation failure a corrective model turn, but should keep invalid payloads out of final-response extraction until validation succeeds.
- Google ADK now reports LLM capabilities and routes output-schema/tool compatibility from the model object. Loop setup should branch on declared capabilities and record the report in failure provenance, especially where output schemas and tools cannot be combined.
- Google ADK now runs synchronous OAuth2 token exchange/refresh calls off the event loop and wraps Anthropic rate-limit errors into ADK model errors. Authenticated/provider loops should test token refresh under concurrency and rate-limit retry classification without blocking unrelated async work.
- Google ADK now supports `audio_stream_end` as a live request signal with priority ordering after activity start/end and before blobs/content; `state_delta` is still always applied. Realtime loops should include explicit audio-stream-end turns and verify state deltas are processed independently of the selected live input signal.
- Google ADK now restricts network-fetched A2A agent-card RPC targets and ignores unsafe peer-supplied `EventActions` metadata. Remote-agent loops should enforce trust boundaries before sending RPCs and never let peer metadata mutate local state/artifacts except for documented peer-settable action fields.
- LangGraph checkpoint stores now make namespace-prefix search segment-aware. Graph memory loops that use namespace prefixes should test sibling namespace isolation so state from `foobar` cannot be selected by a `foo` prefix filter.

## Maintenance log
- 2026-07-31: reviewed OpenAI Agents Python voice/realtime/MCP/memory/sandbox/tool commits, Google ADK eval/session/confirmation/code-executor/schema/model/auth/realtime/A2A commits, and LangGraph checkpoint-store namespace matching; appended notes on cancellation closeout, raw-event immutability, cleanup-before-reconnect, memory closed-state, plugin-aware eval loops, deterministic replay windows, confirmation consumption state, process-group timeouts, schema-feedback correction loops, capability-driven setup, non-blocking auth refresh, audio-stream-end control signals, and A2A trust boundaries.

## 2026-08-01 review addendum
- OpenTelemetry's new `get_response` / `gen_ai.get_response.client` span separates loop-state retrieval from inference. Replay or audit loops that fetch prior Responses by ID should represent the fetch as its own non-inference operation and avoid treating historical token counts on the fetched response as new loop cost.
- OpenAI Agents JS v0.14.2 brings the JS runtime to the same loop boundary pattern already tracked for Python: raw realtime transport events are preserved separately from validated internal events; sandbox archive hydration fails closed on ephemeral paths; MCP reconnect cleans selected servers before retrying; and MCP URL credentials are removed from errors, serialized/external metadata, diagnostics, traces, and model-visible tool names. JS loop replayers should keep raw payloads immutable, sanitize server identity for exported state, and model reconnect as cleanup-then-retry rather than retry-first.
- OpenAI Agents JS sandbox secret references now persist as reconstructable references in RunState/session envelopes while resolved secret values remain runtime-only and are re-bound through the current trusted manifest at resume. Loops that resume sandbox sessions should treat secret resolution as a trust-gated runtime step, not as serialized state.
- Google ADK auth recovery now supports fallback OAuth token strings and prefixless credential lookups from session state. Authenticated tool loops should test both prefixed and prefixless credential keys plus fallback token strings before escalating to a fresh authorization flow.
- Google ADK's rubric-text normalization and defaulted output-schema fix tighten correction-loop behavior: decorated rubric echoes should still match expected criteria, and defaulted structured-output fields should not be converted into required fields during `set_model_response` feedback.
- Temporal's TypeScript documentation now marks External Storage as Pre-release for TypeScript while Go/Python remain Public Preview, and clarifies that the OpenAI Agents integration streaming topic is configured on the Client `OpenAIAgentsPlugin`, not the Worker plugin. Durable loop designs should record SDK-specific maturity and client-vs-worker streaming configuration rather than assuming all Temporal integration surfaces share one stage or setup point.

## Maintenance log
- 2026-08-01: reviewed OpenAI Agents JS v0.14.2, OpenTelemetry GenAI fetch-response telemetry, Google ADK auth/eval/schema commits, and Temporal TypeScript integration docs; appended notes on non-inference response fetches, JS raw-event/sandbox/MCP loop parity, trust-gated secret references, credential fallback lookup, rubric/schema correction loops, and SDK-specific Temporal integration maturity/configuration.

## 2026-08-02 review addendum
- OpenAI Agents Python v0.19.2 releases the current cleanup/replay baseline for loop code: LiteLLM streams now close on normal, cancelled, and failure paths; cleanup failures after a terminal completion no longer invalidate an already delivered completed response; raw realtime events remain immutable audit state; MCP reconnect is cleanup-before-retry with redacted identity; voice cancellation and idle audio dispatch have explicit closeout behavior; and memory sessions enforce closed state plus valid-item recency windows. Loop tests should treat these as released behavior when choosing minimum Python SDK versions.
- OpenAI Agents Python now accumulates streamed tool guardrail results onto `RunResultStreaming` and `RunResultStreaming.to_state()`. Streaming loops that pause, resume, or audit tool calls should preserve tool-input and tool-output guardrail results as run state, not infer them from tool outputs after the fact.
- OpenAI Agents Python now replaces a closed default event loop before `AgentRunner.run_sync()` schedules work, while still reusing an open thread-default loop and rejecting calls from an already-running loop. Synchronous loop wrappers should include closed-default-loop recovery tests, especially when surrounding applications or test suites close event loops between runs.
- OpenAI Agents Python and JS both now follow MCP pagination for tool discovery; Python also paginates prompts. Agent loops should not assume MCP discovery is a single request: continuation cursors, per-page retries, cursor-cycle termination, aggregate metadata publication, and prompt/tool cache consistency are part of the setup loop before model turns begin.
- OpenAI Agents Python's explicit zero-value contracts make falsey control inputs more granular: zero disables or defaults some settings, is invalid for MCP lifecycle timeouts, and remains a meaningful explicit value for some SQL/session limits. Loop setup should branch by field semantics rather than by truthiness, extending the earlier falsey-provider/builder lesson to timeout, cache, and result-limit knobs.
- OpenTelemetry's GenAI reference guidance sharpens loop-span ownership: a local agent framework owns agent/tool/workflow spans it actually performs, but model inference belongs to the underlying provider/client instrumentation unless the framework is itself the only model-call boundary. Loop instrumentation should therefore avoid emitting duplicate inference spans for delegated model calls while still preserving agent-level control spans.

## Maintenance log
- 2026-08-02: reviewed OpenAI Agents Python v0.19.2 and same-day loop fixes, OpenAI Agents JS MCP pagination, and OpenTelemetry GenAI instrumentation-ownership guidance; appended notes on released cleanup/replay baselines, streamed guardrail state, closed-loop `run_sync` recovery, paginated MCP setup loops, field-specific zero semantics, and delegated inference-span ownership.

## 2026-08-03 review addendum
- OpenAI Agents Python's ordered deduplication fixes make tool-call replay order part of loop correctness: when duplicate input items collapse, the latest tool output is preserved but kept after its originating call. Replay loops should retain call-before-output ordering even when filters, retries, or session saves remove duplicates.
- OpenAI Agents Python now separates streamed handoff calls from `tool_called` events. Loop consumers that trigger tool execution, approval UI, or telemetry counters from streamed events should branch on handoff versus tool semantics instead of treating every call-shaped event as executable tool work.
- OpenAI Agents Python's agent-tool name-collision handling makes nested-agent setup a deterministic pre-run boundary: colliding normalized names can fail before the loop starts unless explicit names disambiguate them. Loop setup should resolve tool identity once and fail closed on ambiguous derived names.
- OpenAI Agents Python and JS strict-schema normalization for closed typeless object schemas tightens setup loops for MCP/OpenAPI-style tools. Loops should not rely on a missing `type: object` to bypass strictness when object properties and `additionalProperties: false` clearly define a closed object, but nullable roots should still fall back when strict conversion cannot be safe.
- OpenAI Agents JS realtime sessions now run output guardrails against text deltas as well as audio transcript streams. Realtime loops should treat text-only deltas as guardrail-evaluable output and include immediate cutoff behavior for both text and audio modalities.
- OpenAI Agents JS now serializes the OpenAI conversation-session ID lifecycle: concurrent lazy `getSessionId()` calls share one created conversation, failed creation remains retryable, and clear-before-create is a no-op. Conversation-backed loops should use a single-flight lifecycle boundary for remote session IDs and test failure/retry plus concurrent first-turn writes.
- OpenAI Agents JS now preserves approved tool results across output-guardrail failures in both streamed and non-streamed paths. Pause/resume loops should persist the authorization-proven tool result even when a later generated response is blocked, rather than rewinding the approved side effect out of state.
- OpenTelemetry's `execute_tool` reference update reinforces that a loop should emit tool-execution spans only where the framework/library actually executes the tool. Loops that delegate tool execution to another instrumentable layer should preserve control-flow spans but avoid duplicate execute-tool telemetry.

## Maintenance log
- 2026-08-03: reviewed OpenAI Agents Python/JS loop commits and OpenTelemetry GenAI execute-tool ownership update; appended notes on ordered replay deduplication, handoff/tool stream separation, deterministic agent-tool naming, typeless strict object handling, realtime text guardrails, conversation-session single-flight lifecycle, guardrail-state preservation, and execute-tool span ownership.

## 2026-08-04 review addendum
- OpenAI Agents Python v0.19.3 releases additional loop-state closeout fixes: max-turn handler output is persisted to session history, output guardrail results survive tripwire aborts, committed tool session records are kept when a streamed output guardrail trips, falsey output extractors and handoff input filters are honored, closed AsyncSQLite sessions reject use, failed SQLite inserts roll back, and uninitialized `clear_session()` avoids creating a remote conversation. Loop replay should include max-turn and guardrail terminal states as persisted artifacts, not only successful model outputs.
- OpenAI Agents Python v0.19.3 also tightens realtime and voice loop behavior: realtime output guardrails apply to text deltas, delayed audio guardrail interruption is scoped to the response whose audio tripped, interrupt truncation is clamped to received audio, voice streams clean up tasks when they close early, and STT event handling completes after listener errors. Realtime loops should scope cancellations and playback interruption by response ID and include text-only, audio-buffered, and listener-error cases.
- OpenAI Agents Python's v0.19.3 tracing and extension fixes make loop closeout attribution sharper: streamed task spans use the run's workflow name rather than an outer trace's workflow, AnyLLM provider streams can finish close after cancellation, completed streamed runs are preserved even if provider-stream close fails, and model-call failures are recorded on the provider's own span. Streaming loops should separate terminal run outcome from post-terminal close errors while preserving provider-span failure provenance.
- OpenAI Agents JS now preserves inline compaction items across turns and exposes `compaction_item_created` events. Loop implementations that compact long histories should treat compaction markers as explicit control-state boundaries for resume and replay, not as disposable model metadata.
- OpenAI Agents JS now keeps causal call-before-output order during input deduplication and resolves ambiguous tool/handoff names with owner-scoped approval state. Resumable JS loops should test duplicate provider IDs, nested-agent approvals, and tool-name collision policies before executing or resuming tool work.
- Google ADK's LiteLLM timeout fix clarifies a unit boundary in loop setup: ADK `http_options.timeout` is milliseconds, but LiteLLM expects seconds. Loop timeout budgets should record both configured and provider-translated values so failure provenance distinguishes a real model delay from unit-conversion drift.
- OpenTelemetry's expanded `create_agent` reference coverage clarifies loop ownership for remote agents: creating Anthropic Managed Agents, AWS Bedrock Agents, Google GenAI agents, Mistral agents, Azure AI Foundry agents, or OpenAI Assistants is a client-side agent-service operation, while the remote service owns later reasoning/model/tool internals. Local frameworks such as AutoGen should not emit `create_agent` spans just because a local agent object was constructed.
- Temporal Visibility docs now explicitly classify schedule list/count and other cross-execution reads as Visibility operations with eventual consistency and rate limits. Durable agent loops that coordinate through schedules or worker/deployment listings should avoid immediate list-after-write assumptions and prefer ID-specific lookups when they need strongly scoped confirmation.

## Maintenance log
- 2026-08-04: reviewed OpenAI Agents Python v0.19.3, OpenAI Agents JS compaction/order/collision commits, Google ADK Data Agent and LiteLLM timeout commits, OpenTelemetry `create_agent` reference coverage, and Temporal Visibility docs; appended notes on persisted terminal states, response-scoped realtime interruption, provider-stream closeout, explicit compaction markers, JS causal replay/tool identity, timeout-unit provenance, remote-agent create ownership, and eventual-consistency boundaries for durable workflow listings.

## 2026-08-05 review addendum
- OpenAI Agents Python v0.19.4 makes more terminal and negative loop states released behavior: completed tool-guardrail results, content-filter refusals, non-streaming agent-span failures, MongoDB closed-state enforcement, empty-add no-op conversation behavior, branch-ID reuse rejection, failed realtime connection cleanup, sandbox token budgets, and provider thinking-block preservation are all part of the public baseline. Loop replay should preserve these terminal artifacts and avoid treating filtered, blocked, or empty-add paths as missing state.
- OpenAI Agents Python's `run_producer_consumer` pattern changes streaming closeout expectations: paired producer/consumer tasks should propagate the primary failure, cancel and drain the sibling, and avoid hanging queue consumers. Loop code should model streaming callbacks, Codex event handlers, agent-as-tool streaming, and sandbox-memory workers as paired lifecycles with explicit failure and cancellation propagation.
- OpenAI Agents Python now cancels sibling sandbox environment resolvers when one `EnvValue` resolver fails. Sandbox loops that resolve secrets or environment values concurrently should make fail-fast sibling cancellation part of manifest resolution, preventing later secret-store/network resolvers from continuing after the manifest is already invalid.
- OpenAI Agents Python's MCP compatibility work means MCP setup loops must tolerate both MCP Python SDK v1 and v2 behavior. Discovery, prompt/tool listing, transport startup, retry, and metadata tests should run as a compatibility matrix before the agent loop begins.
- OpenAI Agents JS added idempotent session-history transactions for append and replace-suffix operations and fixed repeated history provenance. Loop state persistence should treat session mutation as a transaction with expected suffixes and idempotence keys, not as blind append-only writes, especially across retries, compaction, streaming, and callback-supplied rewrites.
- OpenAI Agents JS now preserves committed tool effects when output guardrails block the visible final response. Loop implementations should not roll back executed tools just because final output is hidden; instead, they should persist execution status and replayable side-effect evidence while marking final output inaccessible.
- OpenAI Agents JS now cancels and drains sibling tool work after concurrent tool failure. Parallel tool loops should use a fail-fast sibling-cancellation boundary so a losing tool does not continue mutating session, sandbox, or external state after another concurrent tool has failed the turn.
- OpenAI Agents JS realtime failed connection attempts now clean up WebRTC/WebSocket connection state and restore prior connection parameters where needed. Realtime loops should treat failed connect as an explicit cleanup transition before retrying or restoring a previous model/API-key/URL state.
- Google ADK's GCP auth provider thread-local REST client cache changes loop resource ownership for concurrent credential flows: auth clients are per-thread resources rather than shared provider state. Authenticated loops should test credential acquisition under concurrent threads and prevent cross-thread client reuse from becoming a hidden race.
- OpenTelemetry's workflow-duration metric rename from `gen_ai.workflow.duration` to `gen_ai.invoke_workflow.duration` makes workflow invocation the named loop boundary. Loop telemetry should emit the new metric name alongside any `invoke_workflow.internal` span and migrate dashboards/alerts away from the old name.
- OpenTelemetry's MCP status clarification means a server receiving client-caused JSON-RPC errors should not necessarily mark its server span as failed, while the client side reports JSON-RPC error codes as errors. MCP loop retries and SLOs should classify client/server responsibility separately instead of feeding all MCP errors into server-failure retry policy.
- Temporal's Python Google GenAI integration guide extends the external-durability loop pattern to direct Google GenAI/Gemini/Vertex model calls: model calls can be invoked from Workflows through the plugin, tools should be Activities, streaming/files/MCP/managed-agent paths are documented, and Activity timeout/retry policy remains the durable control boundary.

## 2026-08-22 review addendum
- OpenAI Agents JS now treats an empty, length-truncated Chat Completions result as `ModelBehaviorError` with `unsafeToReplay=true` and `responseStarted=true`, while retaining usage and raw terminal evidence. Loop retry policy should route this state to correction/escalation rather than blind replay, and should preserve usage even when no successful final response exists.
- Google ADK's MCP liveness probe now tolerates SDK versions that move or remove private stream attributes and pairs the probe with an owned task-aliveness check. MCP loops should classify "known disconnected" separately from "not observable" and avoid making private transport layout a hard availability dependency.
- Google ADK's live streaming tools can yield user-facing `Event(message=...)` updates directly while yielding plain values to the model; direct updates do not consume a model turn or tokens, are persisted to session history, and can be stopped through an explicit tool. Long-running loops should separate user-progress events from model-directed results and make duplicate background-task prevention and cancellation explicit.
- Google ADK's multimodal tool-results plugin now supports opt-in session retention across turns for text/file parts while keeping inline audio/image data one-shot. Loop state policy should declare retention scope and prevent binary payloads from being unintentionally replayed across turns.

## Maintenance log
- 2026-08-05: reviewed OpenAI Agents Python v0.19.4 and commits for producer/consumer closeout, MCP compatibility, and sandbox env-resolver cancellation; OpenAI Agents JS commits for session transactions, blocked-output persistence, sibling tool cancellation, content-filter/refusal surfacing, invalid-argument redaction, repeated provenance, and realtime cleanup; Google ADK auth concurrency; OpenTelemetry workflow/MCP semantic-conventions; and Temporal Python Google GenAI docs. Appended notes on terminal-state preservation, transactional session mutation, fail-fast sibling lifecycles, MCP compatibility/status semantics, thread-local auth ownership, renamed workflow metrics, and durable Google GenAI loop integration.

## 2026-08-06 review addendum
- 2026-08-06: OpenAI Agents Python's atomic session mutation work changes loop-state persistence from best-effort item writes toward transaction-like logical mutations across supported stores. Retry/resume loops should treat session append, pop, clear, and suffix replacement as atomic state transitions, and should surface oversized or failed logical batches as failed mutations rather than replaying a partially written turn.
- 2026-08-06: OpenAI Agents Python's Chat Completions request-ID propagation gives loops a transport-neutral provider correlation field. Error-handling loops should keep the request ID alongside response IDs, continuation IDs, and trace spans so support/debug escalation can identify the exact provider request even when no Responses object ID exists.
- OpenAI Agents Python's `apply_patch` mapping coercion now preserves `move_to`. File-edit loops that accept JSON-like patch plans should validate destination preservation before execution, because a lost move target changes a move into an invalid or destructive operation.
- OpenAI Fast mode can now be selected through OpenAI Agents Python `extra_args={"service_tier": "fast"}` for supported models. Loop schedulers that choose between normal and latency-sensitive paths should make service tier an explicit input to routing, budget, retry, and evaluation decisions rather than hiding it inside provider-specific request extras.

## 2026-08-08 review addendum
- OpenAI Agents Python now binds approval state to concrete tool invocations. Approval/resume loops should carry the exact pending invocation identity and reject stale, cross-call, or concurrent-call approvals before executing a tool.
- OpenAI Agents Python now records request counts even when a provider omits usage. Loop accounting should preserve the completed request/retry event independently from optional token telemetry, rather than treating absent usage as an absent turn.
- OpenAI Agents Python realtime tool-call updates now enter session history. Realtime loops should persist incremental tool-call state before completion so interruption and resume reconstruct the same control state as the live session.
- Google ADK now keeps jittered retry delays within `max_delay`; retry loops should test the post-jitter value against the declared ceiling instead of assuming a nominal backoff formula is sufficient.
- Google ADK's parallel function-call path now preserves every tool result. Fan-out loops should join results by call identity and fail tests on dropped results when several tool responses share one turn.
- Google ADK artifact hardening rejects tampered metadata and avoids inconsistent partial writes. Durable loops should treat artifact metadata validation and atomic publication as part of the state transition, not as post-hoc storage hygiene.
- Google ADK now collects evaluation state from workflow nodes. Workflow-loop evaluators should include node-produced state in the eval artifact so a workflow is not scored only from its final root response.
- OpenAI Agents JS v0.14.3 turns the previously reviewed JS loop-state fixes into a release baseline: session mutation transactions, collision-stable tool identities, approved tool-result persistence, sibling tool cancellation, repeated-history provenance, realtime failed-connect cleanup, and content-filter refusal surfacing should be assumed available only at or above that version.
- OpenAI Agents JS AI SDK adapter fixes preserve response order and complete final output across reasoning, text, and tool-call interleavings. Adapter loops should avoid reducing a turn to the last text part; instead they should reconstruct final output from ordered response items while keeping tool boundaries intact.
- OpenAI Agents JS final-output validation redaction makes structured-output failure a privacy-preserving terminal loop state. Structured-output loops should retain redacted validation-failure provenance for correction or escalation without logging raw invalid payloads when sensitive data logging is disabled.
- Google ADK's typed-dict schema emission means loop setup can expose map value types to the model for `dict[K, V]` tool parameters. Tool loops should still distinguish untyped dictionaries from typed maps so flexible metadata bags remain open while typed maps get stricter model-visible schemas.
- Google ADK's Claude 5 model routing update keeps new Claude model-family names on the Anthropic LLM path. Model-selection loops should include model-name regex/routing tests for new families before using them in automated provider fallback or capability decisions.
- Google ADK Live now detects `task_completed` anywhere among parallel function responses. Live sequential loops should treat completion signals as order-insensitive semantic events, especially when models call a completion tool alongside ordinary tools in the same turn.

## Maintenance log
- 2026-08-06: reviewed OpenAI Agents Python atomic session/request-ID/apply-patch/Fast-mode commits, OpenAI Agents JS v0.14.3 and AI SDK/final-output redaction commits, and Google ADK typed-dict/model-routing/live-flow commits; appended notes on transaction-like session transitions, provider request correlation, destination-preserving patch moves, service-tier routing, release-pinned JS loop baselines, ordered adapter reconstruction, redacted structured-output failures, typed-map setup, new model-family routing, and order-insensitive live completion.

## 2026-08-09 review addendum
- OpenAI Agents Python's durable pending-input work makes resumed input a first-class loop state: each admitted occurrence has an identity, server-managed input is committed only after acceptance, and unaccepted input remains pending for the next attempt. Resume loops should distinguish staged, admitted, server-accepted, filtered, and committed input states so a retry cannot duplicate or silently lose user input.
- OpenAI Agents Python now prunes orphaned tool outputs when applying limited session windows. Loop compaction should preserve call/result pairing as an invariant and should not resume from a state containing a result whose call was evicted.
- OpenAI Agents Python adds an application approval boundary for unsafe retries. Retry loops should expose replay-risk evidence to policy code and require an explicit decision before repeating side-effect-capable model/tool sequences; ordinary transient retry classification is not sufficient.
- OpenAI Agents Python preserves local shell outputs across `RunState` resume, so tool loops can resume from completed local work without re-execution. The persisted state should retain output provenance and distinguish completed execution from a pending retry.
- OpenAI Agents JS now serializes compaction session mutations. Long-running JS loops should treat compaction as a serialized state transition, not an in-memory marker, and test concurrent/interrupting compaction against resume so the latest compaction boundary cannot be lost or reordered.

## Maintenance log
- 2026-08-09: reviewed OpenAI Agents Python/JS durable-resume and retry commits; appended notes on identity-bound pending input, call/result-safe compaction, explicit unsafe-replay approval, shell-output resume, and serialized JS compaction state.

## 2026-08-10 review addendum
- OpenAI Agents Python and JS now serialize overlapping MCP lifecycle operations so concurrent close calls share one cleanup task instead of starting duplicate server shutdowns. MCP loops should make lifecycle transitions single-flight, expose cleanup failures separately from caller cancellation, and test reconnect-after-close races.
- OpenAI Agents Python adds finite default MCP connect/cleanup waits and bounded CI jobs. Loop policies should give setup and teardown explicit deadlines; an agent run is not complete until resource closeout either succeeds or records a bounded timeout outcome.
- OpenAI Agents Python preserves typed sandbox error contracts while redacting protected mount details. Sandbox loops should classify failures by stable operation/error code while ensuring secrets and mount paths do not cross the diagnostic boundary.
- OpenAI Agents Python now forwards a transcription-session close error to the consumer when the producer otherwise completed cleanly. Voice/stream loops should treat producer close as a terminal transition and never leave consumers blocked because cleanup failed after apparent success.
- OpenAI Agents JS now carries pending input through resumable `RunState` with occurrence identity and server-acceptance checkpoints. JS loops should distinguish input staged for the next turn from input accepted by a server-managed conversation, matching the Python resume contract and preventing duplicate admission.
- OpenAI Agents JS now round-trips JSON-compatible structured tool outputs in `RunState`. Tool loops should preserve structured values as replay state, reject cyclic/non-finite values deterministically, and avoid using stringification as the persistence format.
- Google ADK's single-file eval config discovery reduces setup ambiguity but creates a resolution boundary: explicit config wins, local single-file evals may infer adjacent `test_config.json`, and remote/eval-set IDs do not. Eval loops should persist the resolved-config decision for reproducibility.
- SWE-bench's new CLI separates evaluation from post-run reporting, allowing saved logs to be re-graded without containers. Benchmark loops should make execution logs durable and keep verdict computation replayable after harness/parser changes.

## Maintenance log
- 2026-08-10: reviewed OpenAI Agents Python/JS MCP, timeout, sandbox, voice, and RunState commits; Google ADK eval CLI changes; and SWE-bench CLI changes. Appended notes on single-flight lifecycle cleanup, bounded closeout, privacy-safe terminal errors, durable cross-SDK input/output replay, explicit eval configuration, and replayable benchmark grading.

## 2026-08-11 review addendum
- OpenAI Agents Python v0.20.0 and JS v0.15.0 make durable pending input a released cross-SDK loop contract: paused runs can stage identity-bearing input that remains pending through serialization until a safe model request, with server-acceptance and replay-policy boundaries. Hermes loops should distinguish staged, admitted, accepted, and committed input rather than treating resume input as an ordinary prompt.
- OpenAI Agents JS's historical `RunState` corpus adds migration and negative-path evidence to the loop boundary, including future-schema, malformed-schema, prototype-key, and incompatible sandbox-state cases. Resume logic should fail closed on unsupported state and preserve a versioned compatibility corpus as part of release gates.
- OpenAI Agents Python's strict-schema fixes reject unsafe `$ref` siblings and schemas beyond a safe recursion depth. Loop setup should reject ambiguous or computationally unsafe control/tool schemas before model execution, and record schema-rejection provenance as a setup failure rather than a model-turn failure.
- Google ADK's eval-result persistence saves aggregated case results before failure assertions, so failed evaluation loops leave inspectable artifacts. Evaluation orchestration should persist attempt/result state before raising on a failed criterion and keep the artifact tied to the app and eval-set identity.
- Google ADK's Cloud Run sandbox fix prevents an executor from waiting forever, while its BigQuery analytics update adds explicit delivery/termination observability and event IDs for retry-duplicate identification. Sandbox and telemetry loops should have bounded executor waits, explicit terminal outcomes, and stable event identity across delivery retries.
- SWE-bench's harness fixes expose a loop invariant: every input instance must reach an explicit outcome even when image setup, browser sandbox startup, or output decoding encounters infrastructure faults. Benchmark loops should reconcile input, executed, graded, and dropped counts before closeout.

## Maintenance log
- 2026-08-11: reviewed OpenAI Agents Python/JS releases and schema/RunState commits, Google ADK eval/sandbox/analytics commits, OpenTelemetry GenAI workflow-reference changes, and SWE-bench harness fixes; appended notes on durable input state, migration-safe resume, pre-execution schema rejection, failed-eval persistence, bounded sandbox/telemetry closeout, and explicit benchmark instance accounting.

## 2026-08-12 review addendum
- OpenAI Agents JS's new scripted model and sandbox-session utilities make controlled replay of model turns, tool calls, approvals, retries, streams, and sandbox state a first-party loop-testing surface. Hermes loop tests should use scripted scenarios for deterministic state-transition coverage and reserve live calls for capability tests.
- OpenAI Agents Python now closes model streams when streamed turns terminate through failure, rather than leaving provider resources open on a terminal path. Stream loops should treat failure closeout as a required transition and test it separately from successful output aggregation.
- Google ADK's GCS evaluation managers reject unsafe path segments before blob-name construction. Evaluation loops should validate app/eval identifiers before persistence and surface rejected identifiers as explicit setup outcomes.
- LangGraph's node-level `trace_policy` enables selective tracing in graph execution. Loop instrumentation can now distinguish critical transitions from deliberately quiet nodes without making trace policy an undocumented global switch.

## Maintenance log
- 2026-08-12: reviewed OpenAI Agents Python/JS, Google ADK, LangGraph, OpenTelemetry GenAI, and SWE-bench commits; appended notes on scripted replay, failure-path stream closure, evaluation-identifier validation, and node-scoped tracing.

## 2026-08-13 review addendum
- OpenAI Agents Python now isolates interruption results across copied `RunState` objects. Resume and approval loops should copy interruption state immutably or copy-on-write so one branch cannot consume or mutate another branch's pending control signal.
- OpenAI Agents Python adds a configurable maximum to MCP retry backoff. MCP loops should expose the ceiling in policy/configuration and preserve effective delay provenance; retry budgets need both attempt and wall-clock bounds.
- OpenAI Agents JS Standard Schema support extends schema-first control boundaries to inputs and outputs supplied by external schema libraries. Loop adapters should normalize schema validation failures into explicit setup/turn outcomes rather than silently coercing incompatible outputs.
- Google ADK's evaluation path now treats an agent crash before any metric execution as an evaluation failure. Loop/eval orchestration should make no-metric crashes terminal infrastructure outcomes, not successful runs with missing measurements.
- Google ADK's Apigee completion client now bounds request timeout and redirects. Provider loops should keep transport deadlines and redirect policy visible in failure provenance and avoid unbounded network transitions.

## Maintenance log
- 2026-08-13: reviewed OpenAI Agents Python/JS and Google ADK loop changes; appended notes on branch-safe interruption state, bounded MCP retry timing, Standard Schema validation boundaries, no-metric crash termination, and bounded provider transport behavior.

## 2026-08-14 review addendum
- OpenAI Agents Python now gives each copied `RunState` checkpoint a fresh tool-state scope and copies nested approval ledgers before resumption. Approval loops should make checkpoint identity explicit and prevent decisions from leaking between independently resumable branches.
- OpenAI Agents Python's max-turn handling now preserves session semantics across data-redacted failures and cleanup paths. Termination handlers should test both the returned max-turn outcome and session/stream cleanup, including redacted exception boundaries.
- OpenAI Agents JS mirrors interruption-snapshot detachment and isolates interruption result arrays. JavaScript resume loops should not reuse mutable interruption collections across retries or branches.
- Google ADK parallel workflow cancellation now propagates to in-flight workers and drains them with a bounded timeout. Fan-out loops should record cancellation propagation, drain outcome, and timeout provenance as explicit terminal state.
- SWE-bench's exit-code spoof defense makes benchmark termination evidence multi-sourced: parsed test statuses are insufficient when the underlying test command failed. Evaluation loops should preserve command exit status separately from parser output and classify disagreement as an invalid/incomplete result.

## 2026-08-15 review addendum
- Google ADK now runs an agent used as a tool under the caller's `RunConfig`, while preserving a separate per-invocation LLM-call ceiling and disabling incompatible code-execution support for the nested run. Delegation loops should propagate caller metadata, labels, HTTP settings, and limits deliberately, while recording which settings are intentionally transformed at the boundary.
- Google ADK's live flow now cancels background tool tasks when the owning run ends and bounds shutdown waiting to one second. Live loops should record cancellation propagation and bounded drain outcomes as terminal state instead of declaring completion when orphaned tool work remains.
- Google ADK's workflow automation no longer passes raw GitHub event JSON into an agent prompt; it passes an identifier and fetches content through the API. Tool loops should keep untrusted event data outside prompt construction where possible and use narrow identifiers plus explicit retrieval/authorization boundaries.
- OpenAI Agents JS v0.16.0 preserves Chat Completions reasoning on the assistant message it belongs to. Cross-provider loops should retain message-role/phase ownership during conversion so replay and subsequent turns do not reinterpret reasoning as an unrelated tool or user event.

## Maintenance log
- 2026-08-15: reviewed OpenAI Agents Python/JS v0.21.0/v0.16.0 and Google ADK runtime/security commits; appended notes on delegated RunConfig propagation, bounded live-tool cancellation, identifier-based untrusted-input handling, and message-ownership-safe replay.

## 2026-08-16 review addendum
- OpenAI Agents Python/JS model-call timeouts create a new loop boundary distinct from whole-run limits: each attempt can be cancelled and classified as a timeout, with Python preserving timeout provenance in model spans and preventing unsafe stateful replay. Loop policies should distinguish per-attempt deadline, full-run deadline, caller cancellation, retry eligibility, and cleanup completion.
- Run-scoped sandbox cwd support changes relative tool-path resolution without making the workspace private to the run; Docker networking can be disabled explicitly. Loops that delegate sandbox work should carry cwd/network policy in state and revalidate the cwd before resumed execution.
- Google ADK's bounded, relevance-ranked in-memory retrieval limits prompt growth to ten results and makes result ordering deterministic by match count then insertion order. Memory-augmented loops should treat retrieval count and ranking as explicit context-budget controls.
- SWE-bench's zero-count rejection and task-repository retention sharpen terminal evidence: a parsed summary is not enough, and a re-grade must preserve the original test environment identity. Evaluation loops should retain independent execution evidence and immutable grading provenance through report-only passes.
- Google ADK now sorts function-call arguments when rendering cross-agent context, reducing nondeterministic textual context differences. Cross-agent loop replay should canonicalize rendered argument order while retaining the original structured arguments.

## 2026-08-17 review addendum
- OpenAI Agents Python's `apply_patch` control loop now rejects an `Update File` action that has no actual diff hunk, even when it includes a move directive. Mutation loops should enforce operation-shape preconditions before applying filesystem changes and record the rejected action as a terminal tool error rather than treating it as a successful no-op.
- SWE-bench's Modal/task-repository guard makes execution topology an explicit loop precondition: a remotely built image cannot be paired with a local task repository whose tests or patches would be evaluated against a different tree. Evaluation loops should fail before setup when source/build identity is incompatible, and preserve interpreter identity in smoke-test commands.
## 2026-08-18 review addendum

- OpenAI Agents Python's updated workflow policy makes runtime probing an approval-scoped loop: planning does not authorize execution, and changing the disclosed command, material, or capability scope requires new approval. Hermes control loops should represent probe authorization and scope changes as explicit states rather than inferred permissions.
- Google ADK's equality-based session-event deduplication closes a replay loop hazard in which copied broadcasts could reapply state deltas. Resumable loops should use event equality/identity semantics deliberately and test duplicate delivery before mutating session state.
- Google ADK's A2A long-running-function fix reads the function name from the data payload rather than metadata when choosing `auth_required` versus `input_required`. Cross-agent loops should derive control decisions from the canonical payload field and test both continuation states.

## 2026-08-20 review addendum
- OpenAI Agents JS now treats unsuccessful Responses terminal events as model failures while recording their usage, and marks response-started failures unsafe to replay. Loop policies should separate terminal failure classification, billed-usage accounting, and retry safety instead of converting every failed response into an empty successful turn.
- Google ADK added a regression guard against duplicate function execution when computer-use/function-calling support is enabled, and its function-response flow now pairs a response with the call it answers. Tool loops should key execution and result reconciliation by canonical call identity and test duplicate delivery under capability-enabled paths.
- Google ADK now runs local code execution in a plain child interpreter. Execution loops should treat interpreter/process identity and process cleanup as explicit boundaries, with failure evidence retained separately from the parent agent process.
- Google ADK's SQLite session merge now follows `dict.update()` semantics, making resumed state conflict behavior explicit. Persistence loops should test overwrite/merge precedence rather than relying on incidental dictionary iteration or append order.
- Google ADK stopped forwarding credential requests from `RemoteA2aAgent` to the remote peer. Cross-agent loops should keep credential prompting local to the owning trust boundary and fail closed when a remote continuation requests credentials.
