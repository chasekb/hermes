# Activity Tracking Checklist → Memory Promotion

## Session takeaway
This reference captures the concrete rule set learned while implementing Hermes activity-checklist capture and selective memory promotion.

## Promotion criteria
Promote a checklist entry only when it has:
- a stable action or subject
- a clear scope
- a verifiable evidence pointer
- a terminal status such as closed or verified
- future reuse value

## Do not promote
Keep the item in the checklist when it is:
- in progress
- a routine status ping
- missing evidence
- duplicated from another status update
- transient operational chatter

## Suggested fields
Useful fields for telemetry or checklist capture:
- action
- scope
- evidence
- status
- owner or actor
- session id

## Implementation notes
- Preserve the source checklist as the trace.
- Write compact redacted records into decision memory.
- Keep redaction in the capture path.
- Require a trace-back link from the memory record to the source note.

## Verification example
A good record lets a reviewer answer:
- What was done?
- Where is the evidence?
- Why is it durable?
- What source note does it trace back to?
