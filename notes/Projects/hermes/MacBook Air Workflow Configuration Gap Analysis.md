---
project_id: hermes
note_type: configuration-gap-analysis
updated_at: 2026-09-04T00:00:00Z
---
# Hermes Configuration Gap Analysis — MacBook Air workflow

## Scope and provenance

This review compares the remote `workflow/macbook-air-m5` branch with `workflow/linux-arch` in `chasekb/hermes` and checks the live Hermes Agent configuration and `hermesagent` Kanban board.

- Repository: `https://github.com/chasekb/hermes`
- MacBook Air branch: `workflow/macbook-air-m5`
- Linux/Arch delivery branch: `workflow/linux-arch`
- Reviewed Mac branch HEAD: `45642bd5b138dd7d563b0ddd7185afaa76f45750`
- Linux/Arch base at review: `origin/workflow/linux-arch`
- Live board: `hermesagent`

## Findings

| Area | Evidence | Gap | Risk |
| --- | --- | --- | --- |
| Host portability | Both branch configs contain `/path/to/hermes/...` hook commands, MCP filesystem/state paths, and shell snippets sourcing `/path/to/hermes/Documents/...`. | Configuration is not portable to Linux/Arch and can fail closed or invoke the wrong local resource. | High |
| Hook installation | `hooks_auto_accept: true` is committed while every hook command points at a machine-local path. | A missing hook target is not represented as a validated installation prerequisite. | High |
| MCP database access | PostgreSQL MCP entries source project `.env` files and set `DB_READ_ONLY=true`, but paths and ports are embedded in the committed config. | Read-only intent is good, but deployment/path resolution is machine-specific and needs explicit environment/project indirection. | High |
| Workflow verification | `.github/workflows/verification.yml` triggers on `main` only. | Pushes to `workflow/macbook-air-m5` and `workflow/linux-arch` do not receive automatic verification. | High |
| Cross-branch drift | The Mac branch adds routing/delegation and broad config changes; the Linux branch has a different Kanban config shape and also retains the same host paths. | There is no required cross-platform configuration contract or branch parity check. | Medium |
| Durable checkpoints | `checkpoints.enabled` is `false`; the prior harness analysis already records this as a gap. | Long-running workflow recovery remains dependent on external session/Kanban state. | Medium |
| Safety defaults | `security.redact_secrets: true`, `security.tirith_fail_open: false`, `approvals.mode: manual`, and database snippets set `DB_READ_ONLY=true`. | These are strong defaults, but their preservation is not asserted by CI. | Medium |

## Recommendations

1. **Remove host-specific paths from tracked configuration.** Use `$HERMES_HOME`, `${HERMES_PROJECT_ROOT}`, explicit profile/project environment variables, or a generated local overlay. Keep credentials and `.env` files untracked.
2. **Add a fail-closed configuration contract checker.** Validate YAML, reject absolute paths owned by another machine, require hook targets to be declared/installed, and assert the safety invariants (`redact_secrets`, `tirith_fail_open`, manual approvals, and read-only database access).
3. **Make CI branch-aware.** Run verification on `main`, `workflow/macbook-air-m5`, and `workflow/linux-arch`; include the configuration contract checker and report the exact SHA and complete job matrix.
4. **Separate portable base config from machine overlays.** Document the overlay loading order and provide Linux/Arch and macOS examples without committing secret-bearing values.
5. **Add a cross-platform smoke matrix.** Exercise config resolution on Linux and macOS fixtures, including absent hook targets and absent optional project `.env` files; expected failures must be typed and fail closed.
6. **Enable checkpoints selectively for long-running workflows.** Define retention and rollback boundaries first; do not enable them globally without reviewing disk/secret implications.
7. **Require independent review before closeout.** The implementation lane must be followed by fresh tester and reviewer evidence against the exact pushed SHA; no local build substitutes for remote CI.

## Recommended execution order

- First: portable path/overlay contract and invariant checker.
- Second: branch-aware CI plus Linux/macOS fixture coverage.
- Third: migrate the committed config and hook/MCP entries to the portable contract.
- Fourth: checkpoint policy and selective enablement.
- Final: independent verification and security/configuration review.

## Current conclusion

The MacBook Air workflow branch is feature-rich but not self-contained: it carries host-specific paths and lacks branch-triggered CI. The Linux/Arch branch shares the path defect, so it is a suitable delivery branch for the analysis and branch metadata, but not evidence that the configuration gap is closed. The Kanban implementation graph records the remaining work and acceptance gates.
