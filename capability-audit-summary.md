# Hermes capability-audit reconciliation

Scope: /Users/bernardchase/.hermes

## Confirmed state

### Root / global Hermes home
- Hooks are wired in config.yaml to a single router script: /Users/bernardchase/.hermes/agent-hooks/hook_router.py.
- 17 hook events are configured: pre/post tool, pre/post LLM, pre/post API, session start/end/finalize/reset, subagent_stop, pre_gateway_dispatch, pre_approval_request, post_approval_response, and three transform hooks.
- Hook routing is verified working: agent-hooks/hook-events.jsonl shows live pre_tool_call, post_tool_call, pre_llm_call, post_llm_call, pre_api_request, post_api_request, on_session_start, on_session_end, on_session_finalize, on_session_reset, subagent_stop, pre_gateway_dispatch, pre_approval_request, and post_approval_response events.
- MCP servers are configured in root config (13 total): codex, filesystem, github, chrome-devtools, postgres-db, postgres-metabase, postgres-trade, postgres-cohida, sqlite, fetch, sequential-thinking, brave-search, and git.
- LSP is enabled in root config; lsp/package.json and lsp/package-lock.json pin dockerfile-language-server-nodejs, pyright, and yaml-language-server, and lsp/bin/docker-langserver exists.
- Skills are installed globally in the root tree: 100 active skill trees on disk, plus 1 archived tree under .archive/.

### transformorchestrator profile
- The profile-local config is minimal (description only); it does not add local hook or MCP overrides.
- The profile has 90 skill trees on disk.
- The profile is a strict subset of the root skill tree: it has no profile-only skills, and it omits the root-only finance bundle, agent-self-improvement-telemetry, and devops/containerized-build-verification.

## Most important gaps / weak spots
- transformorchestrator depends on the global/root configuration for hooks and MCP; there is no profile-local isolation of those surfaces.
- The root has extra capabilities that are not present in transformorchestrator, especially the finance bundle and agent-self-improvement-telemetry.
- MCP is configured, but this audit did not runtime-test server discovery/auth/tool calls; treat it as configured rather than independently re-verified here.
- The popularity-weighted shortlist from prior audits should be treated as inference unless separately restated from the source audit output.
- Several capability additions remain uncommitted in the working tree, so the repo looks mid-reconciliation rather than fully finalized.

## Working-tree items that reflect the current audit cycle
- Added/updated capability-oriented skill/reference files for kanban-orchestrator, github-pr-workflow, github-repo-management, systematic-debugging, subagent-driven-development, containerized-build-verification, agent-self-improvement-telemetry, and finance.
- lsp/package.json, lsp/package-lock.json, and lsp/bin/docker-langserver are part of the current work and support the new LSP coverage.
