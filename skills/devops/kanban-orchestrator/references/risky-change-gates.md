# Risky change gates

Use these gates when a change could alter Hermes behavior, routing, or maintenance policy.

Applies to:
- workflow changes
- skill changes
- hook/router changes
- backlog model or review cadence changes
- any change that affects execution, persistence, or promotion rules

## Practical budgets

Start with the smallest budget that still makes the risk obvious.

| Change class | Budget | Required evals | Review rule |
| --- | --- | --- | --- |
| Docs-only / copy edit | Up to 2 files, no behavior change | 1 targeted doc check | Safe to ship with a short note |
| Small behavioral tweak | Up to 5 files or ~200 net lines | 2 evals: targeted smoke + regression spot-check | Require an explicit rollback note |
| Risky policy or routing change | More than 5 files, >200 net lines, or touches hooks/config/backlog serialization | 3 evals: config/format validation, targeted smoke, and round-trip or end-to-end check | Requires a prewritten rollback path and review sign-off |

If the change touches `agent-hooks/`, `config.yaml`, `backlog/backlog.json`, serializer code, or promotion/acceptance rules, treat it as risky by default.

## Required eval checks

Pick evals that prove the actual surface changed:
- syntax / format validation for docs, JSON, YAML, or code
- targeted smoke test for the exact entrypoint being changed
- round-trip read/write or replay test when persistence changes
- workflow or hook routing check when control flow changes
- one small negative test when the failure mode matters

Do not promote a change if the eval only proves that the file exists. It must prove the behavior that matters.

## Rollback / abort criteria

Rollback or abort immediately when any of the following is true:
- an eval fails
- the change leaks a secret or exposes raw sensitive data
- the behavior changes and the effect is not intentional or documented
- the rollback path is unclear or would require a data migration with no revert plan
- the change cannot be verified from the same entrypoint the user will use
- the review surface got broader but the evaluation budget did not increase

Rollback should be specific: revert the last commit, restore the prior config, or disable the new gate. Avoid vague "we'll fix it later" language.

## Weekly / stale review integration

Weekly backlog review should:
- flag pending risky changes before they spread across the tree
- require the change budget and eval plan to be written down for anything above docs-only scope
- record the decision-memory entry when a risky change passes or fails

Stale-item review should:
- treat repeated eval failures as blocker evidence
- defer items that need more budget than the current plan allows
- drop items whose implementation path is obsolete or whose rollback path is unsafe

## Sample change path

Example: updating a skill plus its reference docs.
1. Budget: 2 files, docs-only unless behavior changes.
2. Evals: markdown or JSON validation plus one targeted review pass.
3. Rollback: revert the patch if the review doc no longer matches the skill behavior.

Example: changing hook routing.
1. Budget: risky-change budget.
2. Evals: config validation, routing smoke test, and round-trip evidence that the intended hook still lands on the router.
3. Rollback: restore the previous router path or config before promoting the change.
