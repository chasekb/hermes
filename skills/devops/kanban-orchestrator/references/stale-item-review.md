# Stale-item review

Use this when backlog items stop moving or remain blocked long enough that they might no longer be worth doing.

Registry entry: `references/workflow-registry.md` → `stale-item-review`

## Heuristics

Consider an item stale when one or more of the following are true:

- no status change for an extended period
- blocked with no new blocker information
- duplicate of a newer item
- low value compared with current priorities
- the implementation path has become obsolete

## Decision labels

- keep
- defer
- drop

## Review flow

1. Read the item and its history.
2. Check the last updated timestamp and blocker notes.
3. Decide whether the item should still be kept, deferred, or dropped.
4. If kept, update the backlog with the next actionable step.
5. If deferred, record the reason and revisit date.
6. If dropped, mark it closed/archived with a short explanation.

## Next action after review

- keep: update the backlog with the next concrete step
- defer: record the revisit date and blocker summary
- drop: archive or close the item after the closeout note is written
- risky or repeatedly failing changes: capture the evaluation failure and route the work through `references/risky-change-gates.md` before trying again

## Evidence to record

- reason for the stale classification
- proposed action
- any dependency or replacement item
- reviewer identity or source
- whether the decision-memory store supports the recommendation
