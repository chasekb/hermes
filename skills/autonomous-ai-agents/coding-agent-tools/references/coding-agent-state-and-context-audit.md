# Coding-Agent State and Context Audit

Use this reference when auditing a local coding-agent home for token waste, extension state, and durable knowledge gaps.

## Audit questions

1. What is loaded on every cold start?
2. What is discovered or loaded only when relevant?
3. What persists for session resume but is not automatically injected?
4. What is merely cached on disk?
5. Which learned facts or procedures are promoted into durable memory or skills?
6. How much context is repeatedly referenced per model call?
7. Are cache hits masking attention-heavy long sessions?
8. Which current product features are unavailable because of version lag?

## Safety boundary

Default to metadata-only inspection. Do not read or print:

- credentials, tokens, OAuth state, or `.env` files;
- auth-cache bodies;
- shell-snapshot bodies;
- backup bodies;
- transcript message text;
- telemetry payload bodies.

Inspect filenames, sizes, JSON keys, record types, usage fields, tool names, and CLI-reported activation state. If transcript content is genuinely required, obtain explicit authorization and narrow the scope.

## State classification

Classify every discovered surface before estimating token impact:

| Class | Examples | Token implication |
|---|---|---|
| Hot/startup | Global instructions, unconditional rules, memory index | Recurring context and attention cost |
| Warm/lazy | Path rules, skill bodies, deferred tools, retrieved notes | Costs only when matched or invoked |
| Episodic/resumable | Session JSONL, task state, file history | Usually relevant only on resume or explicit search |
| Cold/disk-only | Marketplace clones, disabled plugins, backups, caches | Storage cost; do not count as active prompt context |

Never infer activation from files alone. Confirm with the product CLI: version, configured MCP servers, installed/enabled plugins, agents, and diagnostics.

## Metadata-only transcript audit

Use a recursive file walk rather than fixed-depth globs. Nested subagent logs are easy to miss and can materially change totals.

For each valid JSONL record, aggregate only:

- `input_tokens`;
- `cache_creation_input_tokens`;
- `cache_read_input_tokens`;
- `output_tokens`;
- usage-record count;
- record type/subtype;
- structured tool-use names;
- compaction markers;
- malformed-record count.

Compute:

- total referenced input = uncached + cache creation + cache read;
- cache-read share;
- cache-creation share;
- average referenced input per usage record;
- average output per usage record;
- tool calls per usage record.

Do not equate cumulative stored counters with current billing, and do not claim every transcript byte is resent on every turn. Use the figures to diagnose context shape, not to reconstruct private conversations.

## Live-state discipline

Agent homes mutate while agents run. Therefore:

1. Take an initial structural inventory.
2. Run independent research/audit tracks.
3. Take one final recursive metadata snapshot.
4. Timestamp the published figures.
5. Search the report for stale intermediate counts before finalizing.

A changing count is not an audit failure; presenting it as timeless is.

## Multi-agent research split

Use three independent tracks:

1. **Local architecture audit**
   - Startup context, settings, extensions, memory, transcripts, caches, and quantified token mechanisms.
2. **State-of-the-art evidence**
   - Official product docs, MCP/skills standards, context management, memory research, and empirical claims.
3. **Target-architecture critique**
   - Hot/warm/cold tiers, capture, retrieval, security, observability, rollout order, and evaluation gates.

Require source URLs, confidence labels, and explicit distinction among verified capabilities, empirical results, recommendations, and inference. Synthesize only after all tracks complete.

## Interpretation rules

- High prompt-cache reuse is good for cost and latency, but it does not shrink the context window or restore attention.
- A large context window is working capacity, not permission to load more permanent instructions.
- Raw transcripts are evidence, not durable semantic memory.
- Generated memory is revisable knowledge, not the right home for mandatory policy.
- Procedures belong in skills; path-specific conventions belong in scoped rules; volatile facts should be retrieved from their live source.
- MCP standardizes transport and discovery, not ranking, truth maintenance, retention, or trust.
- A marketplace cache or manifest inventory is not an installed capability set.

## Preferred target architecture

Use “store broadly, inject narrowly”:

- **Hot:** tiny global and project control-plane instructions.
- **Warm:** path-scoped rules, skill descriptions/bodies, project memory index, and bounded retrieved facts.
- **Cold:** raw transcripts, full tool output, superseded knowledge, and complete evidence.

Durable records should carry source, timestamp, project/path scope, confidence, sensitivity, validity window, content hash, and supersession/contradiction links.

Start with lexical/FTS retrieval. Add embeddings only after a labeled query set demonstrates a recall gap.

## Capture and consolidation

Hooks should capture quietly and asynchronously:

- `PostToolBatch`: event envelope plus pointer/hash for large output;
- `PreCompact`: objective, decisions, evidence pointers, modified files, and open tasks;
- `SessionEnd`: final manifest and candidate-learning queue;
- instruction-load events: what loaded and why.

Do not summarize every tool call into active context. Candidate learnings should be redacted, deduplicated, classified, and reviewed before promotion. Never silently edit global instructions from generated observations.

## Initial operating budgets

Useful starting targets—not universal constants:

- 3–6 retrieved snippets;
- 1–2K retrieved tokens per normal query;
- 4–8K operational ceiling for unusually large MCP results;
- large logs persisted to disk with path, hash, metadata, and selected excerpts;
- local lexical retrieval p95 below 200 ms;
- capture-only hook overhead p95 below 100 ms;
- at least 95% provenance coverage for injected durable claims.

## Rollout order

1. Upgrade after reviewing release notes and backing up configuration.
2. Fix wrongly scoped global instructions.
3. Establish fresh-session, focused-compaction, and task-sensitive reasoning policies.
4. Verify native project memory and add a few narrow skills/rules.
5. Add asynchronous evidence capture and a local FTS index.
6. Add budgeted, cited retrieval.
7. Add selected MCP servers only after output, permission, and secret-handling policies exist.
8. Experiment with embeddings, learned retrieval, or automatic skill synthesis only after the deterministic baseline passes evaluation.

## Evaluation gates

Freeze representative tasks and compare features enabled versus disabled. Track:

- task success and verification quality;
- total and uncached input tokens per task;
- retrieved-context tokens;
- cache-read/cache-creation shares;
- compaction count and post-compaction corrections;
- repeated rediscovery calls;
- retrieval precision@k;
- stale/contradicted-memory use;
- source-pointer coverage;
- hook latency and MCP result size;
- secret-scanner results.

A reasonable first gate is at least 15% median main-context reduction with no quality loss; target 25% after retrieval is mature. Keep all new hooks, MCP servers, and retrieval injection independently disableable.

## Common pitfalls

- Fixed-depth globs that omit nested subagent logs.
- Treating cached marketplaces as enabled plugins.
- Treating cache-hit ratio as proof of context efficiency.
- Publishing live counts without timestamps.
- Moving long procedures from one startup file into another startup import; imports organize context but do not save tokens.
- Adding a vector database before defining provenance, contradiction, and evaluation policy.
- Letting external tool or web output promote itself into authoritative instructions.
- Writing a large audit report but failing to add it to the durable research index.
