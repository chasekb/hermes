# Persistence

Write a compact JSON record to `backlog/decision-memory.json` with at least:
- timestamp
- prompt_class
- prompt_sha
- lane metadata (provider, model, lane role)
- reviewer scores and rationale
- winner / recommendation
- short evidence pointer

Keep the record redacted and compact. Do not store full transcripts.
