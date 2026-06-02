# Decision-memory loop

This reference closes the telemetry loop for Hermes self-improvement work.

## Canonical durable store

- `~/.hermes/backlog/decision-memory.json`

The store should contain only durable, redacted execution metadata:
- what was expected
- what was observed
- what actually changed
- which skill, workflow, hook, or backlog item was involved
- the recommendation for the next review pass
- evidence pointers, not raw secrets or raw transcripts

## Record shape

Each record should be compact and review-friendly:
- `ts`
- `subject_type`
- `subject_id`
- `expected`
- `observed`
- `outcome`
- `recommendation`
- `evidence`
- `risk_flags`
- `redacted`

Keep the record focused on decision support, not on logging volume.

## How the review workflow consumes it

Weekly backlog review and stale-item review should read the durable store and turn the latest observations into one of these actions:
- keep
- defer
- drop
- promote
- rollback
- retest

A failed or partial execution should push the next review toward a concrete follow-up, not just a generic note.

## What stays out

Do not store:
- secrets, tokens, passwords, or auth headers
- raw prompts or private user content
- full transcripts when a short summary will do
- noisy step-by-step logs that do not affect the decision

## Practical use

When a workflow finishes, write one compact record to the durable store and point the backlog or review note at it.
Then the next weekly or stale-item pass can reuse the same evidence instead of reconstructing the session from scratch.
