---
name: public-source-market-research
description: "Class-level workflow for evidence-led research from public sources: market state, adoption signals, monetization, services, and dated citations."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [research, market-intel, public-sources, evidence, citations, adoption, monetization]
---

# Public-Source Market Research

Use this umbrella when the task is to answer a current-state question from public evidence: who is adopting a product, how people are monetizing it, what services exist, and whether the market signal is real.

## Core loop
1. Convert the prompt into evidence questions, not just a topic.
   - Adoption: who is using it, how many, and what is the scale signal?
   - Monetization: what are people selling, at what price, and through what channel?
   - Product state: what do the official docs say about plans, pricing, and availability?
   - Ecosystem: are there agencies, partners, plugins, or communities forming around it?
2. Prefer primary sources first.
   - Official product/docs pages.
   - Company newsrooms and pricing pages.
   - GitHub repos, npm/PyPI/registry stats, package release pages.
   - First-party partner/service pages.
3. Use secondary sources only as support or discovery.
   - Public consulting pages.
   - Dated news, conference recaps, or market writeups.
   - Treat SEO-heavy explainers as leads unless independently corroborated.
4. Record the date of the evidence and the retrieval date separately.
5. Return findings as bullets with source URLs, dates, and a short interpretation.

## Evidence standards
- Prefer sources that are dated, live, and directly state the claim.
- If a page makes a scale claim, look for an independent corroborator or an API-backed metric.
- If a service page claims pricing, note whether it is advertised pricing, estimated pricing, or self-reported consulting rates.
- If you cannot validate a claim, label it as unverified instead of smoothing it over.

## Source hierarchy
1. Official docs / pricing / newsroom
2. Public APIs and platform telemetry
3. Public repository stats and release pages
4. Public service/consulting pages
5. News articles and analyst commentary
6. Search snippets only as discovery, never as final proof

## Workflow families

### Market/state snapshots
Use for “what’s the current state of X?” questions.
- Capture current product state, pricing, and ecosystem signals.
- Summarize by category rather than source-by-source narration.

### Adoption signals
Use for “is this getting traction?” questions.
- Pull concrete indicators: stars, downloads, followers, active repos, partner counts, certification counts, and public customer references.
- Prefer live counts with retrieval timestamps.

### Monetization and services
Use for “how are people making money with this?” questions.
- Look for consulting offers, implementation retainers, subscription products, managed services, training, and templates/agents sold as products.
- Include public price points when available.
- Distinguish vendor pricing from third-party services built around the tool.

### Competitive comparison
Use when comparing multiple tools or vendors.
- Normalize the comparison dimension first: price model, distribution, adoption, enterprise channel, or ecosystem maturity.
- Avoid mixing incompatible metrics without explanation.

### Model/provider variant comparison
Use when comparing model IDs whose names suggest tiers or variants.
1. Dispatch independent research tracks when the user asks for a multi-agent survey: official documentation, live provider metadata, and local integration/catalog inspection.
2. Prefer the vendor's model pages and rate-limit documentation over names, prices, or third-party descriptions.
3. Query the live provider catalog and compare a fixed field set: canonical slug, context window, max output, modalities, tools, reasoning controls, pricing, moderation, per-request limits, and rate limits.
4. Separate verified capability/tier claims from inference. Pricing and catalog metadata do not prove quality, latency, or training differences.
5. Inspect the local integration's routing path: static fallback catalogs may differ from live/account-specific discovery, and a model exposed by one provider may not be available through another.
6. If no benchmark or controlled smoke test is available, say so plainly and recommend a workload-based evaluation rather than inventing a ranking.
7. Return a compact comparison table, source URLs, retrieval date, confidence/uncertainty, and a practical selection rule.

## Output shape
- Short bullet findings.
- Each bullet should carry one claim and one source URL.
- Include date(s) in the bullet where possible.
- Separate “evidence” from “inference.”

## Pitfalls
- Do not rely on search snippets as proof when the source page is accessible.
- Do not confuse SEO content with evidence of adoption.
- Do not use a single metric to infer market fit.
- Do not present scraped claims without noting whether they are self-reported.
- Do not omit retrieval dates when the claim is live and fast-changing.

## Support files
- See `references/source-ranking-and-checks.md` for source ranking, claim validation checks, and a small playbook for current-market research.
- See `references/agentic-coding-agent-economics.md` for a compact evidence bank and opportunity ranking example for agentic coding-tool monetization research.
- See `references/model-variant-comparison.md` for the model/provider variant comparison checklist and claim-discipline rules.

## When to save a note or artifact
If the research will be reused, promote the best evidence into a durable note with sources and dates rather than leaving it buried in chat.
