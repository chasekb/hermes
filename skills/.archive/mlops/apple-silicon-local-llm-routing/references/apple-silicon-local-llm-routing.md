# Apple Silicon local LLM routing reference

This note captures the current working model-selection pattern for Apple Silicon laptops with 16 GB unified memory.

## Practical ladder for 16 GB machines
Coding-first stack:
- fast: Qwen/Qwen2.5-Coder-1.5B-Instruct
- default/quality: Qwen/Qwen2.5-Coder-3B-Instruct
- longctx/analysis: Qwen/Qwen2.5-Coder-7B-Instruct

General-purpose fallback ladder:
- fast: Qwen/Qwen3.5-0.8B or another sub-2B model
- default/quality: Qwen/Qwen3.5-2B to Qwen/Qwen3.5-4B
- longctx/analysis: Qwen/Qwen3.5-4B to Qwen/Qwen3.5-9B

## What made the 16 GB recommendation work
- 4-bit MLX quantization is the practical default.
- 7B is the highest size that still feels like a reasonable laptop default for code-heavy work.
- 9B can work, but it is better as a heavier analysis tier than a general replacement.
- 24B+ class models are typically too large to be a comfortable default on a 16 GB MacBook Air.

## Workflow notes
- Use the live model catalog rather than assuming repo names are stable.
- Re-run `ai-dev models --json` after config changes to confirm the ladder and tags.
- Make `pull-models` rerunnable: skip already-populated output directories instead of failing the entire batch.
- Keep routing tags (`fast`, `quality`, `longctx`, `analysis`, `default`) aligned across config, docs, and cursor output.

## Session-derived example
The working coding-first replacement set used in this repository was:
- `local-mlx-fast` → `mlx-community/Qwen2.5-Coder-1.5B-Instruct-4bit`
- `local-mlx` → `mlx-community/Qwen2.5-Coder-3B-Instruct-4bit`
- `local-mlx-longctx` → `mlx-community/Qwen2.5-Coder-7B-Instruct-4bit`
