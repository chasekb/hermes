---
project_id: hermes
note_type: research-topic
updated_at: 2026-06-12T00:00:00Z
---
# Harness Engineering

## Scope
Harness engineering covers evaluation harnesses, test harnesses, sandboxes, graders/judges, observability, reproducibility, and release gates for agentic systems.

## Search queries used
- `2025 agent evaluation harness best practices official docs instrumentation reliability release gating site:docs.openai.com OR site:platform.openai.com OR site:langchain.com OR site:docs.anthropic.com`
- `2025 evaluation harness design instrumentation reliability best practices AI agents official benchmark docs`
- `SWE-bench official docs benchmark harness agent evaluation reproduction 2025`
- `site:docs.langchain.com LangSmith tracing evals agents reliability instrumentation 2025`
- `site:developers.openai.com traces graders datasets eval runs agent workflows 2025`
- `site:anthropic.com building effective agents evals tool use traces 2026`
- `OpenTelemetry GenAI semantic conventions agent tracing 2025 official`
- `site:openai.com/index harness engineering Codex agent-first world 2026`
- `site:developers.openai.com prompt optimizer eval datasets agent workflows official`
- `site:developers.openai.com/codex/use-cases/ai-app-evals`

## Sources reviewed
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
- OpenTelemetry, Semantic conventions for generative AI systems
  - https://opentelemetry.io/docs/specs/semconv/gen-ai/
- OpenTelemetry Semantic Conventions for GenAI repo, metrics and attributes
  - https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/gen-ai/gen-ai-metrics.md
  - https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/registry/attributes/gen-ai.md
- Google ADK docs, Evaluation overview and criteria
  - https://raw.githubusercontent.com/google/adk-docs/main/docs/evaluate/index.md
  - https://raw.githubusercontent.com/google/adk-docs/main/docs/evaluate/criteria.md
- Braintrust, AI agent evaluation framework
  - https://www.braintrust.dev/articles/ai-agent-evaluation-framework
- Fiddler AI, OpenTelemetry AI observability guide
  - https://www.fiddler.ai/blog/opentelemetry-ai-observability-guide
- Greptime, OpenTelemetry GenAI semantic conventions
  - https://greptime.com/blogs/2026-05-09-opentelemetry-genai-semantic-conventions

## 2026-06-29 review addendum
- OpenTelemetry Semantic Conventions for GenAI repo, Agent Framework reference scenario commit
  - https://github.com/open-telemetry/semantic-conventions-genai/commit/b028dceecdad117461a785c3af35315e7184e813
  - Why it matters: adds native Agent Framework coverage to invoke-agent-internal, inference, and execute-tool reference scenarios and extends the mock Responses server with function-call and usage-detail payloads needed for telemetry validation.

## Sources used in synthesis
- OpenAI Harness engineering
- OpenAI Evaluate agent workflows
- OpenAI Codex evals use case
- Anthropic Demystifying evals for AI agents
- LangChain harness capabilities
- SWE-bench harness docs
- OpenTelemetry GenAI semantic conventions
- OpenTelemetry Semantic Conventions for GenAI repo
- Google ADK evaluation overview and criteria

## Knowledge developed
- Trace-first evaluation is now more useful than output-only evaluation for agent systems.
- Reproducibility depends on pinned environments, isolated runs, and stable fixtures.
- Harnesses are increasingly modular: model, tools, context, approvals, observability, and graders.
- Evals are best treated as CI gates, not one-off research artifacts.
- Telemetry is becoming boundary-aware: OpenTelemetry's GenAI conventions now define separate agent-invocation and tool-execution duration histograms plus a requested reasoning-level attribute.
- ADK's evaluation docs now separate trajectory/tool-use scoring from final-response quality and expose both reference-based and rubric-based criteria for predefined datasets.
- OpenAI's results guide now treats result surfaces as part of the harness contract: final output, replay history, continuation IDs, and resumable approval state each serve a different operational need.
- OpenTelemetry's GenAI conventions are tightening boundary identity: the latest repo alignment keeps `gen_ai.agent.name` on `execute_tool` spans while aligning `invoke_agent.internal` span and metric attributes, which makes cross-boundary trace correlation more reliable.
- OpenAI's eval guide now explicitly points code-first SDK workflows to the Integrations and observability guide for high-signal traces before graders, which reinforces trace-first harnessing for SDK apps.
- OpenTelemetry's GenAI reference repo now includes native Agent Framework coverage, so harnesses should expect agent-framework to appear alongside other runtimes in invoke-agent-internal, inference, and execute-tool reference scenarios.
- Anthropic's agentic-search cookbook shows that reproducing long-horizon benchmark scores depends on harness details such as programmatic tool calling, server-side context compaction, and explicit task budgets, not just dataset and grader selection.

## Best practices
- Start with traces, not a giant prompt blob.
- Grade the workflow, not only the final answer.
- Use deterministic checks whenever possible.
- Use model-based judges where the task is subjective or open-ended.
- Keep environments isolated to reduce drift.
- Treat evals as live CI artifacts.

## Do not dos
- Do not rely on final answers alone for evaluation.
- Do not evaluate in drifting or unpinned environments.
- Do not trust model judges without calibration.
- Do not ignore latency and cost regressions.
- Do not collapse the run result to a single final answer when continuation or review state matters.

## Emerging trends
- Trajectory-first evaluation is replacing single-turn scoring.
- Observability is standardizing around OpenTelemetry-style conventions.
- Harnesses are becoming productized control planes for agents.
- Durable execution and checkpoints are becoming table stakes.
- Long-horizon benchmark harnesses are treating compaction prompts, task budgets, and in-sandbox tool fan-out as first-class knobs for score fidelity.

## Open questions
- How should long-horizon success be measured without overfitting to benchmark quirks?
- What balance of human review and automated judges is appropriate for different tasks?
- Which trace schema will become the common baseline across vendors?

## Maintenance log
- 2026-06-12: split from the combined research notebook.
- 2026-06-16: LangChain's Deep Agents harness now spells out four built-in capability groups—execution environment, context management, delegation, and steering—and makes HITL approval via `interrupt_on` explicit.
- 2026-06-16: Anthropic's Claude Fable 5 launch post again treats harness design as part of the evaluation surface, noting that a minimal harness materially changed a difficult benchmark outcome.
- 2026-06-18: OpenAI's agent-eval guidance keeps trace grading first for workflow debugging, then datasets and eval runs for repeatability; the trace surface is the right place to catch tool-choice, handoff, and policy regressions before scaling benchmarks.
- 2026-06-19: OpenAI's orchestration guide now makes the ownership split explicit: use handoffs when a specialist should own the next turn, use `agent.asTool()` when a manager should keep control, and avoid splitting too early because it adds prompts, traces, and approval surfaces.
- 2026-06-20: OpenTelemetry's GenAI semantic-conventions repo added `gen_ai.invoke_agent.duration`, `gen_ai.execute_tool.duration`, and `gen_ai.request.reasoning.level`; Google ADK's conformance evaluation docs now formalize trajectory/tool-use scoring alongside final-response review.
- 2026-06-21: OpenAI's results guide now separates final output, replay history, continuation IDs, and resumable approval state; the guardrails guide also notes that approval interruptions can surface after handoffs or inside nested `agent.asTool()` calls, so harnesses need to preserve resumable state across multi-agent workflows.
- 2026-06-25: OpenAI's results/state guide now spells out richer run-item and diagnostics surfaces beyond the high-level result contract, including item-level tool and handoff records, raw model responses, guardrail results, and usage details; harnesses should keep these around for audits and deep debugging.
- 2026-06-26: reviewed the OpenTelemetry GenAI semantic-conventions repo alignment commit; appended source-backed notes on keeping agent identity consistent across `invoke_agent.internal` and `execute_tool` spans/metrics.
- 2026-06-27: reviewed refreshed OpenAI eval and observability docs; appended source-backed notes on starting code-first SDK workflows with built-in tracing before graders.
- 2026-06-29: reviewed the OpenTelemetry GenAI Agent Framework reference scenario commit; appended source-backed notes on native Agent Framework coverage, mock Responses function-call payloads, and usage-detail telemetry fields.
- 2026-07-02: reviewed OpenAI Agents SDK strict-schema handoff validation and Anthropic's agentic-search benchmark reproduction cookbook; appended source-backed notes on strict validation at control boundaries plus programmatic tool calling, server-side compaction, and task budgets for long-horizon benchmark harnesses.
