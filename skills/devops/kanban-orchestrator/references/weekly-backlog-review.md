# Weekly backlog review

Use this playbook for the recurring Hermes backlog review.

## Goal

Re-rank the backlog, surface stale items, and promote accepted items into runnable work.

## Inputs

- `~/.hermes/backlog/backlog.json`
- recent Kanban completion evidence
- any new user requests or gaps discovered during the week

## Review steps

1. Load the backlog and sort by status, dependency depth, and last updated time.
2. Identify items that are still proposed or triaged and decide whether to accept, defer, or drop them.
3. Promote accepted items into ready/runnable slices using the backlog-to-kanban bridge.
4. Note blocked items and whether the blocker is external, internal, or obsolete.
5. Capture a short review summary and write it back to the backlog history.

## Good outputs

- a shorter, better ordered backlog
- a list of ready items for Kanban
- a stale-item shortlist
- any follow-up skill or workflow changes

## Minimal verification

- every accepted item has execution criteria
- every ready item has a clear runnable slice
- every closed item has evidence
