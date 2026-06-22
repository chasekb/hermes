# Repo backlog → live Hermes backlog import pattern

This reference captures the cohida session pattern for turning a repo-local backlog into live Hermes backlog recommendations.

## When to use
- The repo already has a backlog or TODO doc.
- The user wants the backlog materialized into Hermes backlog entries.
- The target item shape needs `execution_criteria` and `closeout_criteria`.

## Import recipe
1. Read the repo backlog source of truth first.
   - Prefer the repo docs over chat summaries.
2. Group work into durable recommendation items.
   - Keep one live backlog item per meaningful slice.
   - Preserve the repo's rough priority order.
3. Set the live backlog fields explicitly.
   - `project_id`: repo/project slug (for cohida, `cohida`)
   - `status`: `proposed` unless the item is already accepted/ready
   - `scope`: the repo root path
   - `links`: the source docs used to derive the item
4. Convert source backlog bullets into criteria.
   - `execution_criteria`: source, failing test/fixture, implementation boundary, regression guard
   - `closeout_criteria`: observable proof, passing tests, documentation or reproducibility evidence
5. Preserve dependencies.
   - If one item depends on another, encode it in `dependencies` instead of prose.
6. Keep ids stable and sequential.
   - Continue from the current live backlog id range rather than inventing a separate scheme.
7. Update the live backlog metadata after the write.
   - Refresh `generated_at` and append a short history note if the store uses one.

## Cohida-specific mapping used in this session
- `docs/TODO.md` → P1/P2/P3/P4 ML recommendations
- `docs/cpp_todo.md` → build / docs / final validation recommendations
- `README.md` and `docs/recommended_github_actions.md` → live links for command and CI validation items

## Pitfalls
- Do not copy the repo backlog verbatim into a single generic Hermes item.
- Do not leave execution criteria as vague narrative; make them testable.
- Do not omit `project_id` when the user explicitly requests a project-scoped backlog.
- Do not report the conversion as done until the live JSON has been re-read and verified.
