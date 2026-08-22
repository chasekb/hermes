# Runtime configuration and local knowledge layer

Use this checklist when implementing recommendations against a CLI's user home or agent runtime.

## Safe sequence

1. Re-audit the live installation and classify each file as global policy, project-local guidance, managed runtime state, or sensitive data.
2. Back up only the user-authored files that will change. Never include credentials, transcript bodies, shell snapshots, telemetry payloads, or `.env` files.
3. Upgrade through the package manager already owning the install. Verify the resulting version with the CLI itself.
4. Read the installed release's live settings/hooks schema. Validate event names, exec-form arguments, timeout, and async semantics before editing settings.
5. Put cross-project policy in the global instruction file; move home/repository-specific content into project-local instructions or path-scoped rules.
6. Add skills and agents as metadata-light, on-demand surfaces. Keep the always-loaded instruction budget small.
7. For durable knowledge, use atomic records with scope, source URI, observed/review/expiry timestamps, confidence, verification state, sensitivity class, canonical identity, and supersession links. Keep raw episodes cold.
8. Before production code, write failing tests for: expiry exclusion, restricted retrieval, secret-like metadata rejection, malformed timestamps, same-scope acyclic supersession, malformed/oversized hook input, and actual serialized output budgets.
9. Verify configuration parsing, syntax, unit tests, database integrity, CLI diagnostics, and a real no-tool startup. Invoke any custom agent in a capped smoke test. Inspect only allowlisted hook metadata.
10. Update the report with implementation state, exact test evidence, rollback path, and deferred experiments.

## Failure patterns caught in review

- Storing `valid_until` without filtering expired records lets stale knowledge appear current.
- Allowing cross-scope or cyclic supersession can make every linked record disappear from active retrieval.
- Secret scanning only statements and source URIs misses sensitive canonical keys, scopes, and source-type metadata.
- Measuring compact JSON while printing indented JSON violates a character budget; serialize in the same format used for output.
- Synchronous lifecycle hooks add avoidable latency. Use asynchronous metadata-only hooks when durability requirements permit.
- A reviewer may find real issues after the first green suite; convert each finding into a failing regression test before fixing it.

## Privacy boundary

Hooks should allowlist metadata such as event name, session ID, project scope, tool name, source, and trigger. They must discard prompts, transcript paths, tool inputs, tool outputs, and arbitrary payload fields. Malformed input, oversized input, and journal I/O failures should fail open so observability cannot block the agent.

## Reusable verification commands

```sh
python3 -m unittest discover -s knowledge/tests -v
python3 -m py_compile knowledge/knowledge_store.py hooks/knowledge_event.py
python3 -m json.tool settings.json >/dev/null
python3 - <<'PY'
import sqlite3
connection = sqlite3.connect("knowledge/knowledge.db")
assert connection.execute("pragma integrity_check").fetchone()[0] == "ok"
PY
claude doctor
claude --version
```
