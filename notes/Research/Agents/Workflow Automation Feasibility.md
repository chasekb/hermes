---
project_id: hermes
note_type: research-synthesis
updated_at: 2026-07-07T20:44:34Z
---
# Workflow automation feasibility for autonomous coding/CLI agents

## Ranked list: most automatable today

| Rank | Workflow category | Feasibility | What automates well | Main blockers |
|---|---|---:|---|---|
| 1 | Narrow code maintenance, local bugfixes, test generation | 5.0 | Small bug fixes, dependency bumps, formatting, mechanical edits, failing-test repair, unit-test scaffolding | Flaky tests, hidden integration failures, repo context limits, permissions to run/modify privileged systems |
| 2 | PR review and change validation | 4.6 | Diff summarization, lint/test gating, security/style checks, risk flagging, reviewer notes | Needs human signoff for merges, context about product/security intent, false positives/negatives in static checks |
| 3 | Data extraction and document transformation | 4.3 | Structured scraping, schema extraction, CSV/JSON normalization, doc-to-data pipelines | Source variability, OCR/layout ambiguity, auth/paywalls, source freshness, correctness verification |
| 4 | Ticket triage and support automation | 4.0 | Classification, routing, draft replies, asking clarifying questions, retrieving KB answers | Customer-impact risk, policy/compliance, escalation thresholds, account access, tone/brand control |
| 5 | Migration/refactor in well-tested codebases | 3.6 | Mass renames, API signature updates, mechanical refactors, test updates, compatibility shims | Cross-cutting regressions, build matrix complexity, legacy edge cases, rollout/rollback risk |
| 6 | Sales/ops workflow automation | 3.2 | CRM updates, lead enrichment, meeting scheduling, draft outbound, report generation | Permissioning, compliance, personalization quality, external side effects, approval gates |
| 7 | Content generation | 2.8 | Drafting, outlining, repurposing, summarization, variant generation | Subjective quality, factuality, style/voice control, plagiarism/brand risk, weak automatic verification |

## Why code-centric tasks rank highest

Recent public agent-eval guidance says coding agents are the most straightforward to evaluate because software has deterministic checks: does the code run, do tests pass, and do the generated patches fix the issue without breaking others? SWE-bench’s harness is explicitly Docker-based and grades model-generated patches by applying the patch, running the repo test suite, and checking whether the issue is resolved. Anthropic also notes that SWE-bench Verified rose from ~40% to >80% in one year, which is strong evidence that constrained code tasks are highly automatable with current models and harnesses.

## What still blocks full automation

- **Auth / permissions**: agents often cannot or should not hold production credentials, merge rights, payment authority, or customer-data access.
- **Human review / approvals**: merges, customer-facing actions, money movement, security-sensitive edits, and policy exceptions still need a person.
- **Flaky tests / unstable environments**: nondeterministic CI and integration tests make it hard to know whether the agent truly succeeded.
- **Incomplete evals**: many workflows lack a crisp success metric, so automated grading is noisy or incomplete.
- **Integration complexity**: legacy systems, partial APIs, vendor quirks, and cross-service side effects reduce reliability.
- **Cost / latency**: long tool loops, retries, and multi-agent coordination can become expensive fast.
- **Quality control**: style, brand, correctness, and compliance often need rubric-based review or human calibration.

## Evidence-backed notes by workflow

### 1) Code maintenance / bugfixes / test generation
- OpenAI eval guidance: coding agents are best served by trace grading first, then repeatable datasets and eval runs.
- Anthropic eval guidance: unit tests and deterministic graders are natural for coding agents.
- SWE-bench harness: uses Docker containers, patch application, test execution, and grading on reproducible environments.
- Practical sweet spot: small, localized issues in stable repos with good tests.

### 2) PR review
- Strong fit because PR review is mostly read-only: compare diff, run static checks, inspect tests, and generate review comments.
- Best automated when review criteria are explicit: security, correctness, regression risk, style, and change scope.
- Still needs humans for merge intent, product context, and final approval.

### 3) Data extraction
- High automation when the target schema is fixed and the source is structured or semi-structured.
- Exact-match or field-level validation is possible when the desired output is objective.
- Drops sharply when extraction depends on OCR, messy layouts, or source authority judgments.

### 4) Ticket triage / support
- Anthropic explicitly treats conversational agents in support, sales, and coaching as a major eval category.
- Automation is strongest for classification, routing, FAQ retrieval, and draft responses.
- Full autonomy is blocked by escalation policy, account actions, and tone/compliance constraints.

### 5) Migration / refactor
- Good for mechanical transformations with strong tests and compiler feedback.
- Weak when migrations touch many services, schemas, or external integrations.
- Needs staged rollout and rollback safety.

### 6) Sales / ops
- Useful for internal coordination, CRM hygiene, report drafting, and meeting workflows.
- Hard to fully automate because of permissions, legal/compliance review, and high cost of mistakes.

### 7) Content generation
- Easiest to generate, hardest to fully automate safely.
- Quality is subjective and review-heavy; factual claims and brand voice are hard to verify automatically.

## Public evidence used
- OpenAI, *Evaluate agent workflows* — trace grading, datasets, eval runs, coding vs conversational vs research agents.
- Anthropic, *Demystifying evals for AI agents* — coding agents, support/sales conversational agents, research agents, SWE-bench Verified progress.
- SWE-bench, *Evaluation Harness Reference* — Docker-based reproducible patch/test harness.
- Anthropic cookbook, *Coordinator pattern: big models for planning, small models for execution* — shows cost partitioning and planner/worker split for long-horizon tasks.
