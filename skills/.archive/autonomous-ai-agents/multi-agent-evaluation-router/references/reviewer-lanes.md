# Reviewer lanes

Reviewer lanes must be independent of the generator lanes.

Recommended shape:
- reviewer-a: strict rubric pass
- reviewer-b: skeptical rubric pass

Rules:
- reviewers read the same candidate outputs
- reviewers do not reuse the generator's own self-assessment
- disagreement beyond the threshold triggers a tie-break synthesis pass
