---
name: local-llm-routing
description: Select and maintain local LLM tiers for laptop-class hardware, balancing speed, quality, context-window headroom, and profile/config consistency.
---

# Local LLM Routing

Use this umbrella when choosing, replacing, or rebalancing local models on constrained hardware, especially laptop-class machines with limited memory or thermal headroom.

## Core idea
A stable local setup usually works better as a small tiered ladder than as a single “best” model:
- fast: smallest model that still answers reliably
- default/quality: mid-tier model with the best latency/quality balance
- long-context / analysis: larger model that still fits comfortably with headroom

## Workflow
1. Inspect the live routing state first.
   - Check current profile mappings, tags, and config outputs.
   - Prefer live CLI output over stale docs or old notes.
2. Match the ladder to the hardware class.
   - Small-memory laptops: favor smaller coding-capable models with a clear fast/default split.
   - Larger unified-memory machines: allow a stronger long-context tier, but keep latency realistic.
3. Keep profile names stable when possible.
   - Preserve routing tags such as `fast`, `quality`, `longctx`, and `analysis` unless the user explicitly wants a rename.
   - Update model IDs, generated configs, and docs together.
4. Make model changes rerunnable.
   - Skip already-populated output directories when the tooling supports it.
   - Treat partial artifacts or conflicting files as the exception, not the default failure mode.
5. Verify the new routing set.
   - Re-run profile listing and routing commands.
   - Regenerate any derived config files.
   - Confirm the chosen models actually fit the intended use case.

## Apple Silicon notes
- Apple Silicon laptops often need a stricter size/latency tradeoff than desktop-class systems.
- Use the same decision rule: fit first, then quality, then context headroom.
- Do not pick a larger model just because it exists in converted form.
- Keep the model ladder understandable for future edits; routing tags should make the intent obvious.

## Selection heuristics
Prefer coding-first families when the machine is primarily used for development:
- fast: smallest coding-capable model that remains reliable
- default: mid-tier coder class
- long-context / analysis: larger coder class only if it still leaves headroom

Prefer general-purpose families when the workload is mixed and coding specialization is less important:
- fast: smallest model that still follows instructions well
- default: balanced general model
- long-context / analysis: larger general model with enough context headroom

## Common pitfalls
- Don’t assume an older model name or repo still exists; check the live catalog.
- Don’t pick a larger model solely because it is available in converted form.
- Don’t forget to align config, docs, generated routing files, and tests when changing model names.
- Don’t delete output directories unless the tooling cannot safely reuse them.

## References
- Put session-specific model catalogs, exact conversion notes, and hardware findings in `references/`.
