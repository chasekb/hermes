# Model-Variant Comparison Reference

Use this checklist for model IDs that look like tiers or codenames.

## Evidence sequence

1. Open the vendor's official model pages and model directory.
2. Capture intended use, reasoning label, context, output limit, knowledge cutoff, pricing, and rate-limit tables.
3. Query the live provider catalog and compare canonical slugs, modalities, tools, reasoning parameters, moderation, per-request limits, and prices.
4. Inspect the local integration's static fallback and live-discovery paths. Record whether the selected provider uses account-specific discovery.
5. Search public repositories only for implementation facts; do not treat model names or price as proof of quality.
6. If benchmarks are absent, report the quality ordering as unverified and recommend a controlled workload benchmark.

## Claim discipline

- Vendor tier labels support intended-use claims, not guaranteed benchmark superiority.
- Provider descriptions such as "latency-sensitive" are product positioning, not measured latency guarantees.
- Identical API envelopes do not prove identical underlying models.
- Different provider catalogs can expose different names, limits, or routing behavior.
- Report retrieval dates and preserve source URLs.

## Recommended output

Return a compact table, then separate:

- Verified differences
- Shared published capabilities
- Not documented
- Inferences and confidence
- Practical selection rule
