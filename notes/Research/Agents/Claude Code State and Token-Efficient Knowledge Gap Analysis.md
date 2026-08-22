---
project_id: hermes
note_type: research-report
updated_at: 2026-07-10T03:54:05Z
scope: /Users/bernardchase/.claude
status: implemented
---
# Claude Code State and Token-Efficient Knowledge Gap Analysis

## Executive summary

At audit time, `~/.claude` was a functioning but minimally curated Claude Code home. It retained sessions and benefited substantially from prompt caching, but did not convert tool use and corrections into a durable, selectively retrieved knowledge system. The foundational recommendations were implemented on 2026-07-10; the original measurements below remain the pre-implementation baseline.

The highest-value findings are:

1. `~/.claude/CLAUDE.md` is globally loaded but describes the Claude home directory as though it were the current repository. This is a scope error: unrelated projects receive irrelevant startup context and potentially misleading instructions.
2. The two discovered project auto-memory directories are empty despite eight top-level session transcripts and 613 valid local JSONL records at the final snapshot. Historical state exists, but learned knowledge is not being promoted into the documented durable-memory surface.
3. There are no user-level agents, rules, commands, or skills; no configured MCP servers; and no installed plugins. The cloned official plugin marketplace is only a cache/catalog, not an enabled capability set.
4. Prompt caching is effective: 89.93% of recorded input tokens were cache reads. However, the average total input referenced per recorded model call was approximately 36,599 tokens. The primary optimization target is context breadth and relevance, not cache-hit rate alone.
5. The installation was on Claude Code `2.1.197`; it has now been moved to the Homebrew `latest` channel and verified at `2.1.206`.
6. The target architecture should separate always-loaded policy, path-scoped rules, on-demand procedural skills, per-project learned memory, and a cold indexed evidence store. Retrieval and consolidation should be event-driven and provenance-aware rather than implemented as a large startup prompt.

## Scope and safety

The original audit inspected `/Users/bernardchase/.claude` read-only. It did not read or print:

- `.credentials.json` contents;
- OAuth tokens, API keys, secrets, or `.env` files;
- shell snapshot bodies;
- backup bodies;
- transcript message text.

Transcript processing was limited to structural metadata, usage counters, record types, and tool names. The subsequent implementation modified only the user-authored/configuration surfaces listed below; it did not inspect or rewrite transcript bodies, credentials, telemetry payloads, or shell snapshots.

## Implementation status — 2026-07-10

The foundational hot/warm/cold architecture is now active.

| Recommendation | Implemented state |
|---|---|
| Runtime | Homebrew channel changed from `claude-code` to `claude-code@latest`; `claude --version` and `claude doctor` verify `2.1.206` with no installation issues |
| Global context | `~/.claude/CLAUDE.md` reduced from directory-specific layout documentation to five cross-project guidance bullets |
| Project context | Claude-home-specific instructions moved to `~/.claude/.claude/CLAUDE.md` |
| Scoped rules | `~/.claude/.claude/rules/knowledge-code.md` applies only to knowledge/hook Python paths |
| Reasoning policy | `alwaysThinkingEnabled` changed from `true` to `false`; medium effort remains available and can be raised per task |
| Skills | Added `capture-learning`, `recall-knowledge`, and `context-checkpoint`; startup debug logs report three user skills loaded |
| Subagents | Added the read-only Haiku `evidence-researcher` with a 12-turn cap; an isolated two-turn invocation completed successfully |
| Durable knowledge | Added a standard-library SQLite/FTS5 store at `~/.claude/knowledge/knowledge.db` with provenance, confidence, verification, review, sensitivity, deduplication, and supersession fields |
| Retrieval budgets | Search is bounded by both record count and rendered character count; the default skill requests at most five records and 6,000 characters |
| Capture hooks | `PostToolBatch`, `PreCompact`, and `SessionEnd` hooks write allowlisted metadata only, all asynchronously; prompt, transcript-path, tool-input, and tool-output content is discarded |
| Native project memory | Added a 411-byte `MEMORY.md` only for the Claude-home project, pointing to bounded retrieval rather than duplicating knowledge |
| MCP safety | Set `MAX_MCP_OUTPUT_TOKENS=8192`; no MCP server was added before task-success and context-cost baselines exist |
| Permission hygiene | Removed temporary Podman script commands, a fixed-PID probe, and a nonexistent `update-config` skill permission while preserving reusable permissions |

### Hardening follow-up

The independent review found no blocking issues. Its medium-severity findings were fixed before closeout: expired records are excluded and expose `valid_until`; restricted records are excluded unless explicitly requested; timestamp and all free-text metadata fields are validated for ISO-8601 shape and secret-like content; supersession requires same scope, compatible canonical keys, and an acyclic active chain; and CLI search output is compact so the character budget applies to emitted output. Malformed and oversized hook input now have regression coverage.

### Verification evidence

- Thirteen deterministic `unittest` cases pass for scoped FTS retrieval, idempotent deduplication, expiry, restricted retrieval, timestamp/secret rejection, supersession integrity, character/record budgets, CLI output budgets, and metadata-only hook capture.
- SQLite reports `integrity_check = ok`; the database is mode `0600`, and the hook implementation creates event files with mode `0600`.
- A no-tool Claude startup returned `OK` and emitted a metadata-only `SessionEnd` event.
- A capped custom-subagent run returned `SUBAGENT_OK` and emitted both `PostToolBatch` and `SessionEnd` metadata events. It used two parent turns and stayed under the configured $0.25 smoke-test cap.
- Startup debug output reports three user skills loaded; no user configuration-schema errors were observed.
- `claude doctor` reports no installation issues. MCP and plugin lists remain empty by design.
- Credential-pattern scanning across the user-authored implementation files found no matches.

### Rollback and deliberately deferred work

The pre-change files are backed up at `~/.claude/backups/recommendations-20260710T024138Z/`.

The following actions remain deferred until their roadmap gates are met:

- terminating or archiving idle interactive sessions, because that can destroy resumable work;
- adding MCP servers or plugins, because no integration currently justifies persistent schema or result overhead;
- embeddings, learned retrieval, automatic consolidation, or a Hermes bridge, pending FTS-only evaluation;
- changing default effort below medium, pending task-class A/B measurements;
- automatic semantic extraction from transcript bodies, pending explicit privacy and redaction policy.

## Pre-implementation current-state inventory

### Installed runtime

| Item | Observed state | Evidence |
|---|---|---|
| Claude Code | `2.1.197` | `claude --version` |
| Current npm release | `2.1.206` | `npm view @anthropic-ai/claude-code version`, retrieved 2026-07-10 UTC |
| Configured model | `claude-fable-5[1m]` | `~/.claude/settings.json:2` |
| Thinking | Always enabled, medium effort | `~/.claude/settings.json:7-9` |
| Status line | Directory, branch, model, remaining context, clock | `~/.claude/statusline-command.sh:3-29` |
| Configured MCP servers | None | `claude mcp list`; structural inspection of `~/.claude.json` |
| Installed plugins | None | `claude plugin list` |
| Active agent processes | Three idle interactive sessions at audit time | `claude agents --json` |

The baseline runtime was nine patch versions behind the published npm version. The implementation upgraded it to `2.1.206`; the table above is retained as historical audit evidence.

### Storage profile

`~/.claude` occupied approximately 7.5–7.7 MB during the live audit:

| Surface | Approximate size | Interpretation |
|---|---:|---|
| `plugins/` | 5.5 MB | Cloned official marketplace/catalog; no plugins are installed |
| `projects/` | 1.2 MB | Session and subagent JSONL history |
| `cache/` | 420 KB | Internal caches |
| `backups/` | 180 KB | Configuration backups |
| `shell-snapshots/` | 116 KB | Shell state snapshots |
| Other surfaces | Small | Settings, status line, history, session metadata, telemetry |

The marketplace clone accounts for most disk space but does not imply active plugin loading. Disk size is not the token problem; startup-loaded and turn-carried context are.

### Knowledge and extension surfaces

| Surface | State |
|---|---|
| Global `~/.claude/CLAUDE.md` | Present, 20 lines, 1,499 bytes |
| User `~/.claude/rules/` | Missing |
| User `~/.claude/skills/` | Missing |
| User `~/.claude/agents/` | Missing |
| User `~/.claude/commands/` | Missing |
| Project auto-memory directories | Two, both empty |
| Project auto-memory Markdown files | Zero |
| Primary session JSONLs | Eight |
| Subagent JSONLs | One |
| Valid JSONL records | 613 at 2026-07-10T02:25:39Z; zero malformed |
| Tool calls represented in structured assistant records | 117 |

The global `CLAUDE.md` is not a useful global preference file. It states that “this is `~/.claude`” and describes Claude Code’s internal home layout (`~/.claude/CLAUDE.md:3-20`). Because user-level `CLAUDE.md` is loaded in every project, this content is both irrelevant and potentially misleading outside the Claude home directory.

### Local permission state

`~/.claude/.claude/settings.local.json` is project-local configuration for sessions launched from `~/.claude`, not global settings. It contains a historical allowlist including:

- temporary script paths;
- process-specific commands and PIDs;
- broad package-manager operations;
- read permissions for selected user directories;
- GitHub API and web-search permissions.

Several entries are stale or overly specific (`~/.claude/.claude/settings.local.json:17-22`). This is configuration residue, not reusable knowledge.

## Token and context baseline

The final audit snapshot aggregated usage metadata from nine JSONL files without reading message bodies. The directory was live and counts changed during inspection; the values below are timestamped 2026-07-10T02:25:39Z rather than presented as immutable state.

### Recorded usage

| Metric | Total |
|---|---:|
| Uncached input tokens | 51,613 |
| Cache-creation input tokens | 898,880 |
| Cache-read input tokens | 8,492,013 |
| Total referenced input tokens | 9,442,506 |
| Output tokens | 137,825 |
| Model usage records | 258 |
| Structured tool calls | 117 |
| Explicit compaction markers detected | 0 |

### Derived indicators

| Indicator | Value | Interpretation |
|---|---:|---|
| Cache-read share of input | 89.93% | Prompt caching is already strong |
| Cache-creation share | 9.52% | Some recurring context is repeatedly introduced or invalidated |
| Uncached input share | 0.55% | Low; not the main problem |
| Average total input per model usage record | 36,598.9 tokens | Active context is broad despite caching |
| Average output per model usage record | 534.2 tokens | Output size is moderate relative to context carried |
| Tool calls per model usage record | 0.453 | Tool use exists but is not systematically converted into memory |

Cache reads are discounted and operationally useful, but they still represent context that the model must attend to. A high cache-hit rate can coexist with poor relevance and diluted instruction adherence. The optimization objective should therefore be “minimum relevant active context per successful task,” not simply “maximum cache-hit ratio.”

### Tool-use profile

The structured tool calls were dominated by Bash (80), followed by Read (19), AskUserQuestion (4), Edit (3), WebSearch (3), Skill (2), ToolSearch (2), and one each for Agent, SendMessage, Write, and Monitor.

This profile shows meaningful operational learning opportunities—successful commands, environment quirks, tool failures, and workflows—but no corresponding project memory files were found.

## Official capability baseline

### CLAUDE.md and rules

Anthropic documents two cross-session mechanisms:

- human-authored `CLAUDE.md` instructions;
- Claude-authored auto-memory.

Both load at the start of every conversation. Anthropic recommends keeping each `CLAUDE.md` under 200 lines and moving multi-step procedures into skills or path-scoped rules. Path-scoped `.claude/rules/*.md` files load only when matching files are touched, reducing irrelevant context.

Source: https://code.claude.com/docs/en/memory

### Auto-memory

Auto-memory is enabled by default and stored per project in `~/.claude/projects/<project>/memory/`. The first 200 lines or 25 KB are loaded into every session for that project. It is intended for build commands, debugging discoveries, preferences, and recurring patterns.

Source: https://code.claude.com/docs/en/memory#auto-memory

### Skills

Skills implement progressive disclosure: descriptions are available for discovery, while full bodies load only when invoked. Anthropic explicitly recommends skills for repeated procedures and long reference material that should not live in `CLAUDE.md`. Once loaded, skill content remains in context for the turn/session lifecycle, so the main body should stay concise and supporting files should be loaded only when needed.

Source: https://code.claude.com/docs/en/skills

### Subagents

Subagents have separate context windows and return summaries, protecting the main conversation from search results, logs, and exploratory file contents. They can use cheaper models, restricted tools, maximum-turn budgets, isolated worktrees, selected skills, selected MCP servers, and their own persistent memory scopes.

Source: https://code.claude.com/docs/en/sub-agents

### Hooks

Claude Code exposes lifecycle events suitable for deterministic capture and governance, including:

- `SessionStart` and `SessionEnd`;
- `PreToolUse`, `PostToolUse`, and `PostToolBatch`;
- `SubagentStart` and `SubagentStop`;
- `InstructionsLoaded`;
- `PreCompact` and `PostCompact`;
- `Stop`, `StopFailure`, and task completion events.

Hooks can invoke commands, HTTP endpoints, MCP tools, prompts, or agents. They are appropriate for metadata capture and deterministic policy; they should not indiscriminately inject verbose context on every event.

Source: https://code.claude.com/docs/en/hooks

### MCP and tool discovery

Claude Code’s MCP integration supports tools, prompts, resources, dynamic list changes, local/project/user scopes, and tool search. Tool search is enabled by default in supported environments so a large tool catalog does not have to be loaded eagerly. Plugin-bundled MCP servers are only active when their plugins are enabled.

Source: https://code.claude.com/docs/en/mcp

## Gap analysis

### Gap 1: Incorrect global instruction scope

**Current state:** The global `CLAUDE.md` describes `~/.claude` itself.

**Impact:** Every project can receive irrelevant directory-specific instructions. This consumes startup context and risks incorrect behavior.

**Target:** Global instructions should contain only stable personal preferences and cross-project safety conventions. The Claude-home description belongs in `/Users/bernardchase/.claude/.claude/CLAUDE.md` or a path-scoped local rule, not the global file.

**Priority:** P0; high impact, low effort, low risk.

### Gap 2: Historical transcripts without knowledge consolidation

**Current state:** Eight primary session logs and 117 structured tool calls existed at the final snapshot, but the two project memory directories contained zero Markdown files.

**Impact:** Useful discoveries remain trapped in episodic logs and must be rediscovered. Raw transcripts grow without improving future startup context.

**Target:** Promote only stable, reusable, source-linked facts into project memory. Keep raw transcripts as cold episodic evidence, not startup context.

**Priority:** P0; high impact, medium effort, medium risk because incorrect memories can persist.

### Gap 3: No progressive procedural knowledge

**Current state:** No user or project skills/commands exist.

**Impact:** Multi-step workflows are re-explained or rediscovered; putting them into CLAUDE.md would create token bloat.

**Target:** Create narrowly triggered skills with concise entrypoints and supporting references/scripts. Procedures load only on demand.

**Priority:** P1; high impact, medium effort, low-to-medium risk.

### Gap 4: No path-scoped rules

**Current state:** No user rules directory exists, and the global file is unconditional.

**Impact:** Global context cannot be selectively applied by language, repository area, or task class.

**Target:** Use path-scoped rules for file-type and subsystem conventions. Leave only universal guidance always loaded.

**Priority:** P1; medium-high impact, low effort, low risk.

### Gap 5: No tool/MCP knowledge interface

**Current state:** No MCP servers are configured, even though a marketplace catalog exists.

**Impact:** Claude cannot query Hermes session search, skill catalogs, durable memory, or local indexed notes through a bounded retrieval interface. Users must paste or manually expose context.

**Target:** Add a small, read-first local knowledge MCP surface with tool search, strict output caps, provenance, and explicit write approval. Do not expose the entire Hermes tool catalog by default.

**Priority:** P1/P2; potentially high impact, medium-high effort, security-sensitive.

### Gap 6: No lifecycle capture/consolidation pipeline

**Current state:** Global settings contain no hooks.

**Impact:** Tool outcomes, corrections, compaction summaries, and task completions are not evaluated for promotion into reusable knowledge.

**Target:** Use lightweight hooks to record metadata and queue candidate learnings. Consolidate asynchronously or at session end; never synchronously summarize every tool result into the main context.

**Priority:** P1; high impact, medium effort, medium risk.

### Gap 7: Context breadth is not governed by task budgets

**Current state:** The status line shows remaining context, but no compaction markers were found, and the 1M-context model referenced an average of approximately 36.6K input tokens per recorded model call in the final snapshot.

**Impact:** Large context capacity can hide unnecessary accumulation. Cache efficiency reduces cost but not attention dilution.

**Target:** Establish context budgets by task class, use subagents for exploration, compact at defined thresholds, and start fresh sessions for unrelated tasks.

**Priority:** P0/P1; high impact, low-to-medium effort, low risk.

### Gap 8: Version lag

**Current state:** Installed `2.1.197`; published `2.1.206`.

**Impact:** The installation misses or predates documented improvements such as newer nested skill discovery, richer hook events, updated MCP behavior, and subagent defaults.

**Target:** Review release notes, back up settings, upgrade, and run a configuration smoke test before implementing newer patterns.

**Priority:** P0; medium-high impact, low effort, low-to-medium upgrade risk.

### Gap 9: Stale local permissions and idle-session sprawl

**Current state:** Project-local allow rules include temporary scripts, exact PIDs, and historical commands; three interactive agents were idle.

**Impact:** Configuration accumulates without lifecycle management. Stale permissions add noise and may broaden authority unexpectedly.

**Target:** Remove expired one-off permission entries after review, prefer command-class rules, and establish session cleanup/retention policy.

**Priority:** P1/P2; medium impact, low effort, medium safety value.

## Target architecture

### Tier 0: Enforced controls

Use settings, permissions, sandboxing, and deterministic hooks for behavior that must not be left to model judgment:

- secret-file deny rules;
- destructive-command gates;
- write approval for durable memory;
- source and scope validation;
- output size limits.

This tier is not prompt context.

### Tier 1: Hot, always-loaded context

Keep the global `CLAUDE.md` very small:

- stable personal preferences;
- universal safety conventions;
- pointers describing where project-specific knowledge lives;
- no repository-specific architecture;
- no long procedures;
- no transient state.

Target: tens of lines, not hundreds.

### Tier 2: Warm, conditionally loaded context

Use:

- project `CLAUDE.md` for stable architecture and core commands;
- path-scoped `.claude/rules/` for language/subsystem conventions;
- skill descriptions for discovery;
- project auto-memory `MEMORY.md` as a compact index of validated learnings.

Target: only context relevant to the current repository and touched paths.

### Tier 3: On-demand procedural context

Use skills for:

- recurring debugging procedures;
- deployment/checklist workflows;
- MCP/tool-specific operating procedures;
- research and verification playbooks;
- reusable scripts and templates.

Keep `SKILL.md` entrypoints concise. Store examples, references, and scripts in linked files loaded only when necessary.

### Tier 4: Cold indexed knowledge

Maintain a local evidence store containing:

- source-backed facts;
- tool outcomes and environment quirks;
- workflow evaluations;
- decisions and supersession links;
- session summaries;
- provenance, timestamps, confidence, scope, and expiry metadata.

Expose it through targeted lexical/semantic search rather than injecting it at startup. Raw transcripts remain cold evidence and should not be treated as authoritative memory.

### Tier 5: Episodic archive

Keep session JSONLs, subagent logs, and traces for audit and replay under retention policy. Promote only reusable knowledge upward. Archive or prune stale episodes according to policy, never by deleting credential or database state.

## Knowledge lifecycle

1. **Observe:** Tool calls and user corrections generate candidate learnings.
2. **Filter:** Reject secrets, transient task status, outputs lacking provenance, and facts likely to expire quickly.
3. **Normalize:** Store a compact declarative fact or procedure with source, project scope, timestamp, and confidence.
4. **Deduplicate:** Merge semantically equivalent entries; preserve supersession history.
5. **Promote:** Route facts to memory, procedures to skills, policies to rules/settings, and project commands to project CLAUDE.md.
6. **Retrieve:** Query by task, repository, paths, tools, and recency. Inject only top-ranked snippets within a token budget.
7. **Verify:** Confirm retrieved knowledge against live files/tools when the source is mutable.
8. **Decay:** Expire or demote stale entries; never let old tool output silently override current state.
9. **Evaluate:** Measure whether retrieval reduces tokens and correction loops without lowering task success.

## Recommended roadmap

### Phase 0 — Baseline and hygiene

- Upgrade Claude Code after reviewing release notes and backing up configuration.
- Move the Claude-home-specific global instructions to project-local scope.
- Replace the global `CLAUDE.md` with concise cross-project guidance.
- Review and remove stale PID/temp-path permission entries.
- Close abandoned idle sessions after confirming they are not needed.
- Record baseline metrics: tokens per successful task, cache-read share, context at completion, correction count, tool failures, and re-discovery events.

### Phase 1 — Native Claude mechanisms

- Enable and verify per-project auto-memory; diagnose why no memory files were created.
- Add a small set of path-scoped rules rather than unconditional global rules.
- Create three high-value skills from repeated workflows, not a bulk migration.
- Define a low-cost read-only research/exploration subagent with explicit turn and tool limits.
- Adopt task-class context budgets and compaction thresholds.

### Phase 2 — Local knowledge bridge

- Expose selected Hermes knowledge capabilities to Claude through a local read-only MCP server or narrow CLI wrapper:
  - session search;
  - skill discovery/read;
  - project-note search;
  - memory candidate submission.
- Enable MCP tool search; avoid `alwaysLoad` except for tiny critical servers.
- Cap result size and return ranked snippets with provenance rather than whole files/transcripts.
- Require explicit approval for durable writes.

### Phase 3 — Automated consolidation

- Add `PostToolBatch`, `SubagentStop`, `PreCompact`, and `SessionEnd` hooks that enqueue metadata and candidate learnings.
- Run consolidation out of band so hook output does not flood the active context.
- Route candidates by type: fact, procedure, policy, decision, transient state, or discard.
- Add deduplication, contradiction detection, freshness checks, and supersession links.

### Phase 4 — Evaluation and adaptive retrieval

- Build a replayable task set from recurring work.
- Compare no-memory, native-memory, and indexed-retrieval variants.
- Measure success, correction turns, input tokens, cache creation/read, latency, and stale-memory incidents.
- Promote only mechanisms that improve task success or materially lower tokens at equal quality.

## Metrics and acceptance gates

Track at minimum:

- total and uncached input tokens per completed task;
- retrieved-context tokens per task;
- cache-read and cache-creation shares;
- average context at completion;
- compaction count and post-compaction correction rate;
- repeated discovery/tool calls for previously learned facts;
- memory precision: retrieved entries that were actually useful;
- stale or contradicted memory rate;
- user correction turns;
- skill invocation success rate;
- MCP result size and truncation rate;
- task success and verification pass rate.

Initial acceptance gates:

1. Reduce average relevant input context without reducing task success.
2. No durable memory write may contain secrets or unverified mutable-state claims.
3. Every durable fact must record source, scope, and timestamp.
4. Every procedure must include verification and failure handling.
5. Retrieval must have a hard token/result budget.
6. Live files and systems override remembered state.

Initial measurable targets proposed by the architecture review:

- keep median retrieval payload below 1.5K tokens;
- return 3–6 atomic, cited snippets per retrieval by default;
- keep local lexical retrieval p95 below 200 ms;
- keep capture-only hook overhead p95 below 100 ms;
- achieve at least 95% source-pointer coverage for injected durable claims;
- achieve precision@5 of at least 0.8 on a hand-labeled retrieval set;
- keep known stale or contradicted facts below 2% of retrievals;
- reduce median main-context input by at least 25% without a statistically meaningful decline in task success or verification quality.

## Risks

- **Memory poisoning:** incorrect tool output becomes durable. Mitigate with provenance, confidence, and approval.
- **Staleness:** mutable state outlives its validity. Mitigate with timestamps, TTLs, and source-first verification.
- **Context over-retrieval:** semantic search returns plausible but irrelevant notes. Mitigate with scope/path filters and token budgets.
- **Instruction conflicts:** global, project, local, rule, and skill instructions disagree. Mitigate with ownership and precedence audits.
- **MCP exposure:** broad servers expose secrets or dangerous writes. Mitigate with narrow tools, read-only defaults, roots, sandboxing, and approvals.
- **Hook amplification:** every tool call triggers expensive summarization. Mitigate with deterministic filtering, batching, and asynchronous consolidation.
- **Transcript fallacy:** session history is treated as truth. Mitigate by keeping episodes as evidence and validating against live sources.

## Sources

Official sources retrieved 2026-07-10 UTC:

- Anthropic, Claude Code memory: https://code.claude.com/docs/en/memory
- Anthropic, Claude Code skills: https://code.claude.com/docs/en/skills
- Anthropic, Claude Code subagents: https://code.claude.com/docs/en/sub-agents
- Anthropic, Claude Code hooks: https://code.claude.com/docs/en/hooks
- Anthropic, Claude Code MCP: https://code.claude.com/docs/en/mcp
- Anthropic, context engineering for agents: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Anthropic, tool search: https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool
- Anthropic, prompt caching: https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- Anthropic, context editing: https://platform.claude.com/docs/en/build-with-claude/context-editing
- Anthropic, compaction: https://platform.claude.com/docs/en/build-with-claude/compaction
- Model Context Protocol documentation: https://modelcontextprotocol.io/docs
- Agent Skills open standard: https://agentskills.io/

Comparative and research sources:

- OpenAI, Codex skills: https://developers.openai.com/codex/skills
- OpenAI, Codex memory: https://developers.openai.com/codex/customization/memories
- OpenAI, tool search: https://developers.openai.com/api/docs/guides/tools-tool-search
- LangMem conceptual guide: https://langchain-ai.github.io/langmem/concepts/conceptual_guide/
- A-MEM, agentic memory for LLM agents: https://arxiv.org/abs/2502.12110
- Mem0, production-ready long-term memory: https://arxiv.org/abs/2504.19413
- LongMemEval: https://arxiv.org/abs/2410.10813
- LoCoMo: https://arxiv.org/abs/2402.17753

Local evidence:

- `/Users/bernardchase/.claude/CLAUDE.md`
- `/Users/bernardchase/.claude/settings.json`
- `/Users/bernardchase/.claude/.claude/settings.local.json`
- `/Users/bernardchase/.claude/statusline-command.sh`
- Structural and usage metadata from `/Users/bernardchase/.claude/projects/**/*.jsonl`
- Sanitized structural keys from `/Users/bernardchase/.claude.json`
- `claude --version`, `claude mcp list`, `claude plugin list`, `claude agents --json`

## Delegated review conclusions

Three independent delegated tracks completed: a local architecture audit, public state-of-the-art research, and a target-architecture critique.

### Strong convergence

All three tracks agreed that:

1. long-lived active context is the largest demonstrated token mechanism;
2. cache reuse is strong but does not reduce context occupancy or attention dilution;
3. raw transcript persistence is not equivalent to durable learned knowledge;
4. the global `CLAUDE.md` is wrongly scoped and should be reduced to true cross-project guidance;
5. skills, path-scoped rules, and subagents are the highest-value native progressive-disclosure mechanisms;
6. MCP should be introduced selectively with deferred tool discovery and strict result budgets;
7. generated memory needs provenance, freshness, contradiction handling, and evaluation;
8. the first retrieval implementation should be lexical/FTS-first, with embeddings added only if measured recall requires them.

### Important qualifications

- The approximately 370-token cost of the global `CLAUDE.md` is an estimate based on file size and characters, not a tokenizer measurement. Its behavioral scope error matters more than its direct token cost.
- `alwaysThinkingEnabled` plausibly adds avoidable reasoning use on simple tasks, but the local logs do not isolate its marginal cost. Change it through an A/B test rather than treating the causal effect as measured.
- Mem0 and A-MEM report promising benchmark gains, but those results are author evaluations and may not transfer to private coding and operations workloads.
- MCP standardizes discovery and transport; it does not supply memory ranking, truth maintenance, retention, or trust policy.
- The live Claude directory changed during inspection. Session counts and token totals are a timestamped snapshot, not stable configuration facts.

### Recommended order of operations

1. Upgrade and fix global instruction scope.
2. Establish session/context discipline and task-sensitive reasoning presets.
3. Verify native project memory; add a few narrow rules and skills.
4. Build asynchronous evidence capture and a local FTS index.
5. Add budgeted, provenance-rich retrieval.
6. Add selected MCP integrations only after output and security policies exist.
7. Evaluate before adding embeddings, learned retrieval, automatic skill synthesis, or a cross-agent Hermes bridge.
