# Desktop-versus-VPS TCO Reference

## Reusable model
For an existing desktop, calculate only incremental cost:

`monthly electricity = watts × 24 × 30 ÷ 1000 × electricity_rate`

Use idle and realistic-load scenarios rather than maximum draw alone. Add backup storage, UPS, network upgrades, and maintenance only when they are genuinely incremental.

For a VPS, include:
- monthly compute charge;
- persistent disk and snapshots;
- public IPv4 or other networking fees;
- bandwidth/egress;
- managed databases or monitoring;
- taxes and currency conversion;
- the user's maintenance time.

## Evidence checklist
Prefer, in order:
1. Official provider pricing pages.
2. Manufacturer power specifications.
3. User-provided electricity rate and measured wall draw.
4. Current free-tier documentation, including capacity and SLA limitations.

Record retrieval dates because cloud prices, free tiers, and model-provider pricing change.

## Hermes-specific decision rules
- API-hosted models cost approximately the same regardless of where Hermes runs; hosting location mainly changes availability, network path, privacy, and local-tool access.
- A desktop is usually the economical primary host when it is already owned and Hermes needs local files, browser state, Apple integrations, or interactive use.
- A small VPS is justified by unattended gateway operation, scheduled jobs, reliable inbound webhooks, remote access while the desktop is off, or isolation from personal files.
- A hybrid deployment often dominates: desktop for local integrations and a narrowly scoped VPS profile for 24/7 gateway/cron duties.
- Use private networking such as Tailscale or SSH rather than exposing a full agent control surface directly to the public internet.

## Output checklist
State the bottom line first; show assumptions; normalize monthly costs; distinguish evidence from inference; identify the break-even condition; and give a concrete revisit trigger.
