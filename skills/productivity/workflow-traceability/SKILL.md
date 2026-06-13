---
name: workflow-traceability
description: Track execution-ledger workflows, activity checklists, and selective promotion of durable outcomes into memory or decision logs.
---

# Workflow Traceability

Use this skill when a task needs a durable execution ledger, a checklist of concrete steps, and a rule for deciding what should be promoted into longer-lived memory or decision records.

## Trigger conditions
- You are maintaining an activity checklist, session summary, decision log, or similar execution trail.
- You need to decide whether a note, checklist entry, or workflow event should be preserved as durable knowledge.
- You are wiring telemetry, hooks, or automation that captures workflow state.
- You need to keep transient progress separate from durable decisions.

## Core model
Treat these as different layers:
1. Backlog/spec: what should happen.
2. Checklist/execution ledger: what actually happened.
3. Decision memory: what is durable enough to keep.

Do not collapse all three into one note.

## Procedure
1. Identify the source of truth for execution state.
2. Capture the step, scope, actor/session, evidence, and terminal status.
3. Redact transient noise and any sensitive values.
4. Promote only durable outcomes into decision memory or a decision log.
5. Keep the original checklist entry intact as the trace.
6. Verify that promoted records still point back to the source artifact.

## Promotion rules
Promote when the record has:
- a stable subject or action
- a clear scope
- a verifiable evidence pointer
- a terminal state such as closed or verified
- future reuse value beyond the current session

Do not promote when the record is:
- in progress
- just a status ping
- a duplicated progress update
- missing evidence
- obviously transient or speculative

## Operational patterns
- Use explicit checklist fields when possible: action, scope, evidence, status, owner/actor, session id.
- Prefer compact structured records over prose when emitting telemetry.
- Keep redaction in the capture path, not as a later cleanup step.
- Preserve traceability between the source note and the promoted record.

## Pitfalls
- Do not treat a backlog item as the execution log.
- Do not auto-promote every completed task; durable value still matters.
- Do not overwrite source notes when adding memory; preserve the original evidence trail.
- Do not store transient progress chatter in memory.
- Do not lose the link between the promoted record and the originating checklist entry.

## Verification
A good workflow-traceability implementation answers:
- What happened?
- Where is the evidence?
- Why is this durable?
- Can I trace it back to the source note or run?

If any answer is weak, keep the information in the execution ledger only.

## Support files
- `references/activity-tracking-checklist-memory-promotion.md` — checklist promotion rules, pitfalls, and verification cues.
