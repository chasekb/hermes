---
project_id: hermes
note_type: routing-strategy
updated_at: 2026-07-03T09:37:26Z
---
# Prompt Structuring and Free-Model Delegation Strategy

This note captures the reusable strategy for deciding when Hermes should keep a task on the frontier model, delegate parts of it to free models, or use the multi-agent evaluation router for comparisons.

## Surfaces reviewed
- `skills/autonomous-ai-agents/hermes-agent/SKILL.md`
- `skills/autonomous-ai-agents/hermes-agent/references/openrouter-free-model-selection.md`
- `skills/autonomous-ai-agents/opencode/SKILL.md`
- `skills/autonomous-ai-agents/multi-agent-evaluation-router/SKILL.md`
- `skills/autonomous-ai-agents/mixture-of-agents/SKILL.md`
- `skills/software-development/software-development-workflows/SKILL.md`
- `config.yaml`
- `backlog/backlog.json`
- `backlog/decision-memory.json`

## Current Hermes routing surfaces
- Frontier/default main agent: `model.default = gpt-5.4-mini` with `provider = openai-codex`.
- Prompt compression: `auxiliary.compression.provider = opencode` with `opencode/deepseek-v4-flash-free`.
- OpenRouter discovery: `openrouter.min_coding_score = 0.65`.
- Memory / evaluation routing: the memory manager can fan context into provider tools, and the evaluation-router skill already persists compact routing records.
- Checkpointing exists but is disabled in `config.yaml`, so long-running prompt-class experiments should keep their own evidence artifacts.

## Evaluation set
Use a small durable prompt set with one representative example per class:
- repo-local implementation task
- bugfix / refactor with exact edits
- broad synthesis or research summary
- prompt-comparison / routing analysis
- compression / condensation pass

For each prompt class, keep the input text and expected output shape stable enough to rerun later.

## Scoring rubric
Score each answer from 0-2 on each dimension:
- instruction adherence
- factual precision
- tool-choice quality
- edit safety / change locality
- synthesis completeness
- follow-up robustness

Treat the score as a comparison signal, not an absolute truth.

## Routing matrix

| Prompt class | Preferred lane | Why |
| --- | --- | --- |
| Repo-critical implementation | Frontier main agent | Needs exact edits, repo awareness, and stable tool use. |
| Bugfix / refactor with files to touch | Frontier main agent, with optional free-model summary support | Exactness matters more than savings. |
| Broad synthesis, summary, or note drafting | Free model first pass (`openrouter/owl-alpha` or similar) | Good enough for drafting and compression when exact edits are not required. |
| Coding-heavy free-model experiment | `qwen/qwen3-coder:free` | Best fit when the task is code-centric and still needs free-model economics. |
| General reasoning / broad free-model comparison | `openai/gpt-oss-120b:free` or `nvidia/nemotron-3-super-120b-a12b:free` | Useful for synthesis and comparison when code specialization is not the goal. |
| Multi-model comparison / routing research | Codex + at least two OpenCode free-model lanes + independent reviewers | Keep generation and scoring separate so the comparison is durable. |
| Compression / condensation | `opencode/deepseek-v4-flash-free` | Already wired as the auxiliary compression provider in config. |

## Decision rule
- Use free models to reduce cost or to generate a second opinion.
- Do not let a free model become the authoritative source for repo-critical implementation unless it is being verified by the frontier agent or a separate reviewer lane.
- Use the multi-agent evaluation router whenever the question is "which model class should handle this prompt class?"
- Persist the prompt class, lane metadata, score, and final recommendation in decision memory so the result can be replayed later.

## Closeout summary
- The routing strategy now distinguishes exact implementation from low-risk summary/compression work.
- Free-model delegation is treated as a comparison and assist path, not a blanket replacement for the frontier agent.
- The reusable evaluation shape is durable enough to rerun after model or provider changes.