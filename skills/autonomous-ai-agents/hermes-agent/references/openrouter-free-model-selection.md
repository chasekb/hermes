# OpenRouter free-model selection

Session note: when configuring Hermes for OpenRouter and the user wants the best free model, treat this as a live catalog lookup problem, not a fixed model choice.

Current verification method used in this session:
- Query `https://openrouter.ai/api/v1/models`
- Filter models where `pricing.prompt == "0"` and `pricing.completion == "0"`
- Prefer a direct free model ID over the `openrouter/free` router when the goal is "best" rather than "random free"

Observed free models in the live catalog on 2026-06-04 included:
- `openrouter/owl-alpha` — general-purpose free model, strong default for broad Hermes use
- `openrouter/elephant-alpha` — free
- `qwen/qwen3-coder:free` — strong free coding option
- `openai/gpt-oss-120b:free` — free large open-weight general model
- `nvidia/nemotron-3-ultra-550b-a55b:free` — free high-end reasoning model
- `nvidia/nemotron-3-super-120b-a12b:free` — free reasoning/model-router candidate

Practical selection guidance:
- General Hermes default: `openrouter/owl-alpha` if present and free.
- Coding-heavy sessions: prefer `qwen/qwen3-coder:free` when present; the OpenRouter model card describes it as optimized for agentic coding, tool use, and long-context reasoning.
- Comparison note: `nvidia/nemotron-3-super-120b-a12b:free` is a stronger general-purpose reasoning/chat candidate, but it is not as code-specialized as `qwen/qwen3-coder:free`.
- If the user wants a router instead of a fixed model, `openrouter/free` exists, but it randomly selects from eligible free models and is not the same as “best free model.”
- Re-check the live catalog before changing the config; the free roster changes over time.
