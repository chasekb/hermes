# Russell 3000 source notes

Session notes for the market backlog item `HERMES-BL-0014`.

Observed requirements:
- Use a constituent list, not a proxy ETF ticker, as the source of truth.
- Preserve existing symbol-manager coverage while adding the broader universe.
- Make refresh behavior reproducible from a fixture or repeatable source path.
- Validate deduplication and ordering stability in tests.

Useful framing:
- Treat the Russell 3000 universe as a data-source problem first, then a parsing/normalization problem.
- Prefer a refresh path that can be reproduced by a reviewer without manual curation.
- Record any source limitations or fallback behavior in the backlog item and the supporting docs.
