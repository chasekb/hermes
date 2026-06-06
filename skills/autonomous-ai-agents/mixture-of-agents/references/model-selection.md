# MoA model selection notes

Use the live OpenRouter catalog when picking MoA reference models. Do not assume a fixed free roster.

Selection guidance:
- Prefer direct model IDs over router aliases when you want predictable behavior.
- Keep the reference set small at first: 2-4 models is usually enough.
- Prefer models your account can actually call without fallback or quota issues.
- Favor diversity only when it adds value; avoid piling on near-duplicate models.

Current implementation defaults observed in this session:
- `openrouter/owl-alpha`
- `qwen/qwen3-coder:free`
- `openai/gpt-oss-120b:free`
- `nvidia/nemotron-3-super-120b-a12b:free`

Current aggregator default observed in this session:
- `nvidia/nemotron-3-super-120b-a12b:free`

Practical heuristic:
- General reasoning/chat: start with `openrouter/owl-alpha` if it is present and available.
- Coding-heavy tasks: prefer `qwen/qwen3-coder:free` when available.
- Broader synthesis: consider a reasoning-oriented model, but keep at least one model that is strong at code or math when that is the task.

Verification pattern:
- run the MoA test file with dev deps
- run a mocked invocation to confirm the exact reference list and aggregator wiring
- only then try a live OpenRouter call
