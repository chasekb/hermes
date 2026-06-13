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
- Braintrust, AI agent evaluation framework
  - https://www.braintrust.dev/articles/ai-agent-evaluation-framework
- Fiddler AI, OpenTelemetry AI observability guide
  - https://www.fiddler.ai/blog/opentelemetry-ai-observability-guide
- Greptime, OpenTelemetry GenAI semantic conventions
  - https://greptime.com/blogs/2026-05-09-opentelemetry-genai-semantic-conventions

## Sources used in synthesis
- OpenAI Harness engineering
- OpenAI Evaluate agent workflows
- OpenAI Codex evals use case
- Anthropic Demystifying evals for AI agents
- LangChain harness capabilities
- SWE-bench harness docs
- OpenTelemetry GenAI semantic conventions

## Knowledge developed
- Trace-first evaluation is now more useful than output-only evaluation for agent systems.
- Reproducibility depends on pinned environments, isolated runs, and stable fixtures.
- Harnesses are increasingly modular: model, tools, context, approvals, observability, and graders.
- Evals are best treated as CI gates, not one-off research artifacts.

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

## Emerging trends
- Trajectory-first evaluation is replacing single-turn scoring.
- Observability is standardizing around OpenTelemetry-style conventions.
- Harnesses are becoming productized control planes for agents.
- Durable execution and checkpoints are becoming table stakes.

## Open questions
- How should long-horizon success be measured without overfitting to benchmark quirks?
- What balance of human review and automated judges is appropriate for different tasks?
- Which trace schema will become the common baseline across vendors?

## Maintenance log
- 2026-06-12: split from the combined research notebook.
