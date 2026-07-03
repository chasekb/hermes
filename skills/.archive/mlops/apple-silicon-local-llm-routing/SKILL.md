---
name: apple-silicon-local-llm-routing
description: Select and maintain local MLX model tiers for Apple Silicon laptops, balancing speed, quality, and context window headroom.
---
# Apple Silicon local LLM routing

Use this skill when choosing, replacing, or rebalancing local MLX models on Apple Silicon hardware, especially laptops with constrained unified memory.

## Core idea
On 16 GB Apple Silicon machines, the best default replacement strategy is usually a three-tier ladder rather than a single “best” model:
- fast: smallest coding-capable model that still answers reliably
- default/quality: mid-tier code model with good latency/quality balance
- longctx/analysis: larger model that still fits comfortably in 4-bit MLX

## Recommended workflow
1. Inspect the current stack state before recommending changes.
   - Check live profile mappings and routing tags.
   - Check converted model artifact sizes on disk.
   - Prefer current CLI output over stale docs.
2. Match the model ladder to hardware class.
   - 16 GB unified memory: favor 1.5B / 3B / 7B 4-bit coding models.
   - 24 GB+ unified memory: 7B / 9B / 14B become more realistic depending on context window and concurrency.
   - Avoid treating 24B+ as a default replacement on laptops unless the user explicitly wants a slow analysis tier.
3. Keep profile names stable when possible.
   - Preserve `fast`, `quality`, `longctx`, and `analysis` routing tags.
   - Update model IDs, generated configs, and docs together.
4. Make model pulls rerunnable.
   - If a populated output directory already exists, skip that profile instead of failing the whole conversion pass.
   - Only treat conflicting files or partial artifacts as hard errors.
5. Verify the replacement set.
   - Re-run profile listing and routing commands.
   - Regenerate cursor/litellm config if those outputs depend on the selected models.
   - Run the repo’s template parity and test gates after config changes.

## Selection heuristics
Prefer coding-first families when the machine is primarily used for development:
- fast: 1.5B–2B coder class
- default: 3B coder class
- longctx/analysis: 7B coder class

Prefer general-purpose families when the workload is mixed and coding specialization is less important:
- fast: 0.8B–1.5B
- default: 3B–4B
- longctx/analysis: 7B–9B

## Common pitfalls
- Don’t assume an older Hugging Face repo name still exists; re-check the live catalog.
- Don’t pick a larger model solely because it exists in MLX form; fit and latency matter more on 16 GB laptops.
- Don’t forget to align config, docs, generated gateway config, and tests when changing model names.
- Don’t delete model output directories just to rerun conversions if the tooling can safely skip populated outputs.

## Linked references
- See `references/apple-silicon-local-llm-routing.md` for a compact model-tiering note and session-derived examples.
