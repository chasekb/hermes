# Routing workflow

1. Compute a prompt fingerprint and classify the prompt class.
2. Launch one Codex lane and at least two OpenCode lanes pinned to distinct free models.
3. Preserve each lane output verbatim with provider, model, session/workdir, timestamp, and fingerprint.
4. Run at least two independent reviewer passes against the same outputs.
5. Reconcile with an explicit tie-break rule.
6. Persist the compact record to the decision-memory store.
7. Reuse the stored record only as evidence, not as a hidden policy switch.
