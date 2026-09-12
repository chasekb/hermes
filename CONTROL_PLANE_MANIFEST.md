# Control-plane manifest

This manifest records the boundary applied when converting `chasekb/hermes.git` from a copied Hermes source tree into a configuration repository.

Retained control-plane paths

- `config.yaml` — sanitized installation-local configuration and policy.
- `SOUL.md` — assistant/operator policy.
- `skills/` — curated skills and workflow references; no runtime implementation is retained.
- `notes/` — sanitized research, decision, and project notes that explain configuration choices.
- `backlog/` — sanitized backlog and decision-memory records.
- No `agent-hooks/` code is retained; the former hook helper imported deleted Hermes runtime implementation and was removed.
- `.gitignore`, `README.md`, and this manifest — repository boundary and hygiene documentation.

Removed source/runtime/build paths

- Hermes runtime and CLI implementation: `agent/`, `hermes_cli/`, `gateway/`, `acp_adapter/`, and root runtime modules.
- Source plugins, provider implementations, and tool implementations: `plugins/`, `providers/`, and `tools/`.
- Source tests, generated dashboards/assets, language-server bundles, and source CI workflows.
- Packaging/build metadata: `pyproject.toml` and `setup.py`.
- Runtime/generated state: databases, lock files, logs, caches, pasted transient content, and generated approval state.

Classification decisions

- Skills and notes were retained as control-plane content rather than deleted wholesale. Notes that described source-branch delivery or contained stale host-specific operational material were removed or sanitized.
- `agent-hooks/hook_router.py` was removed because it imports the deleted Hermes runtime (`agent.learning_telemetry`) and therefore cannot be a standalone control-plane helper.
- `capability-audit-summary.md` was removed because it contained stale machine-specific paths and runtime inventory rather than sanitized policy.
- No local builds or tests are run for this cleanup; verification is limited to static inventory, diff, and repository-hygiene checks.
