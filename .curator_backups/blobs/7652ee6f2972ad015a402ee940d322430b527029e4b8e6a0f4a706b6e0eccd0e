# CI and tmux build-debug playbook

This reference captures the working pattern that emerged from the trade repo session.

## tmux log capture

When a long-running build or service is already emitting logs in a tmux pane:
- capture from the most recent clear marker/sentinel
- keep the slice narrow enough to isolate the new failure
- prefer the first explicit error in the captured window, not the last line

Use this when the pane already contains lots of successful startup noise and you need the failure that happened after the latest restart marker.

## CI verification

For push-triggered GitHub Actions verification:
- check the workflow/run status, not just a single job
- treat the run as incomplete until every required job has completed
- if a watch command fails because of an annotations/API fetch issue, re-check the run directly before concluding anything
- a fast job succeeding does not imply the workflow is done if the slow backend job is still running

## Cleanup boundary

When a user asks to stop a local build:
- stop the active process
- prune transient local build artifacts/images/cache if appropriate
- do not delete database data directories unless the user explicitly approves that action

## Triage order

1. capture the live failure context
2. identify the first real error
3. decide whether the fix belongs in compose/config, build flags, or source code
4. verify at the same layer that failed
5. only then move to the next layer

## Useful reminder

If local runtime startup looks partially healthy, verify the slowest remaining job/service before reporting success.
