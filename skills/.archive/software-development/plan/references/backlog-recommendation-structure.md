# Backlog Recommendation Structure

Use this when the user asks for a backlog recommendation, prioritization note, or execution-ready review plan rather than direct implementation.

## Required shape

1. Title that names the domain and the recommendation theme.
2. Short goal statement.
3. Brief architecture / approach summary.
4. One or more prioritized recommendations.
5. For each recommendation:
   - Objective
   - Why it matters
   - Likely files / surfaces to inspect
   - Execution checklist
   - Closeout criteria
6. Recommended delivery order if multiple recommendations are present.
7. Risk notes or assumptions.
8. Tags.

## Checklist guidance

- Execution checklist should describe the work to do, from discovery through validation.
- Closeout criteria should describe the observable result or evidence that proves the item is complete.
- If the user asks for accuracy / correctness review, include data provenance and regression-test checks.
- If the user asks for optimization / training recommendations, include baseline metrics, leakage checks, and measurable success criteria.

## Writing conventions

- Keep recommendations scoped and independently actionable.
- Prefer P0 / P1 labels when priorities are obvious.
- Avoid burying the success criteria inside prose.
- Use concrete file paths and verification steps when the recommendation is implementation-adjacent.
