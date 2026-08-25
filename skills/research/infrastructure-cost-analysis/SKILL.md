---
name: infrastructure-cost-analysis
description: "Use when comparing desktop, VPS, or cloud costs."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [infrastructure, VPS, cloud, desktop, TCO, pricing, reliability]
---

# Infrastructure Cost Analysis

Use this class-level workflow when a user asks whether a workload belongs on an owned computer, VPS, cloud VM, hosted service, or a hybrid arrangement.

## Core principle
Do not compare the VPS bill with the purchase price of an already-owned computer. Treat existing hardware as sunk cost unless the decision includes buying, upgrading, or replacing it. Compare incremental monthly cost and the value of operational properties.

## Workflow
1. Define the workload and service requirement:
   - interactive versus unattended;
   - 24/7 availability, remote access, inbound webhooks, scheduled jobs;
   - CPU/RAM/storage/GPU needs;
   - local-file, desktop-app, LAN, or hardware dependencies;
   - privacy, backup, isolation, and recovery requirements.
2. Gather current prices from primary sources where feasible:
   - provider pricing pages for VPS/cloud;
   - manufacturer power specifications;
   - local electricity rate supplied by the user or clearly labeled as an assumption.
3. Normalize monthly costs:
   - VPS: compute, storage, backups, public IPv4, bandwidth, managed services, taxes;
   - desktop: incremental electricity, UPS/network upgrades, backup storage, and maintenance;
   - cloud trial/free tiers: capacity limits, account/capacity risk, and support/SLA limitations.
4. Separate economic evidence from operational inference. State assumptions and retrieval dates for volatile prices.
5. Identify the break-even point and the non-price decision drivers. A more expensive option can still be rational if uptime, security isolation, or remote availability has material value.
6. Recommend the smallest viable deployment, usually desktop-first, VPS-first, or hybrid. Avoid recommending a VPS merely because it is conventional.
7. For agent systems, account for security boundaries: a VPS with broad shell/file tools is not automatically safer; minimize tools, isolate profiles, protect credentials, and avoid exposing admin interfaces directly.

## Arithmetic
Use a calculation tool for all numerical comparisons. For continuous power:
`monthly_kWh = watts * 24 * 30 / 1000`
`monthly_electricity = monthly_kWh * price_per_kWh`
Use ranges when the actual idle/load draw or electricity rate is unknown.

## Output shape
- Bottom line first.
- Compact comparison table: cost, availability, local integration, privacy/isolation, maintenance, and failure modes.
- Explicit assumptions and source links for current pricing.
- Practical recommendation plus a trigger for revisiting it.
- Mention hybrid architecture when it captures most benefits at lower cost.

## Pitfalls
- Do not claim a VPS reduces model/API spend unless the model endpoint or workload actually changes.
- Do not count the full purchase price of already-owned hardware as a recurring cost.
- Do not use maximum-rated power as normal consumption without labeling it; provide idle and realistic-load scenarios.
- Do not treat free cloud tiers as equivalent to paid capacity or an SLA.
- Do not ignore backups, IPv4 charges, egress, taxes, or provider lock-in when they are material.
- Do not expose a full agent gateway to the public internet by default; prefer private networking, VPN/Tailscale, SSH tunnels, or a hardened reverse proxy.

## Supporting references
- See `references/desktop-vps-tco.md` for the reusable cost model, evidence checklist, and Hermes-specific hybrid patterns.
