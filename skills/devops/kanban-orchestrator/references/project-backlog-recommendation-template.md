# Project Backlog Recommendation Template

Use this when turning a feature request into a durable backlog item instead of a one-off note.

## Required fields
- ID: stable project-scoped identifier
- Title: short, action-oriented
- Summary: one sentence describing the intended outcome
- Scope: exact repo or directory the work belongs to
- Priority: relative to existing open items
- Status: proposed / triaged / accepted / ready
- Created / updated timestamps
- Dependencies: upstream backlog items or implementation blockers
- Evidence / links: exact files, docs, or references the implementer should inspect
- Notes: maintenance constraints, source limitations, or review guidance

## Execution criteria
Write criteria so they can drive implementation and testing:
- Identify the canonical source or input set
- Define the normalization / merge rule
- Specify the refresh or update cadence/trigger
- Add a failing test or fixture-based check that proves the new behavior is needed
- Preserve existing coverage and avoid regressions
- Note any downstream consumers that must continue to work

## Closeout criteria
Write criteria that a reviewer can verify after implementation:
- The new data or behavior is present in the live path or fixture-backed test
- Existing tests still pass
- Documentation records the source, cadence, and fallback behavior
- A reviewer can reproduce the result from the documented source/fixture without manual reconstruction

## Good practice
- Keep the recommendation focused on the smallest durable slice.
- Put implementation detail in execution criteria; put acceptance proof in closeout criteria.
- Include exact file paths in evidence/links whenever possible.
- If the item is data-source driven, record source freshness and fallback behavior explicitly.
