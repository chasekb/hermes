---
name: hermes-profile-fleet-operations
description: "Audit Hermes profiles, Kanban assignees, and dispatch."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [hermes, profiles, kanban, dispatcher, gateway, configuration]
    related_skills: [hermes-agent, kanban-orchestrator, hermes-orchestrator-layout, llm-provider-routing]
---

# Hermes Profile Fleet Operations

## When to Use

Use when auditing, configuring, or recovering a Hermes profile fleet, Kanban assignee roster, gateway dispatcher, or stale worker claims.

Use this class-level skill when Hermes has multiple profiles, role aliases, Kanban assignees, or a dispatcher/gateway that must route work reliably. The goal is to prove both profile readiness and worker-dispatch readiness without exposing credentials or claiming success from configuration alone.

## Core model

Treat these as separate boundaries:

1. **Roster** — profiles and aliases that exist on the machine.
2. **Profile configuration** — each profile's explicit model/provider/endpoint and runtime limits.
3. **Credential availability** — the provider auth method the selected profile actually uses.
4. **Kanban routing** — task assignees resolving to spawnable on-disk profiles.
5. **Dispatcher/service health** — the gateway or standalone dispatcher that claims and spawns workers.
6. **Worker protocol health** — a spawned worker heartbeats and terminates through `kanban_complete` or `kanban_block`.

A green result at one boundary does not prove the others.

## Audit workflow

### 1. Discover the live roster

Run:

```bash
hermes profile list
hermes kanban assignees
hermes kanban boards list
```

For every configured profile, inspect:

```bash
hermes profile show <profile>
```

Do not read or print `.env`, `auth.json`, or credential-pool contents. It is enough to record whether the file exists and whether Hermes reports a configured model/provider.

### 2. Detect incomplete profiles

A profile is incomplete when it has an alias or profile directory but `hermes profile show` reports no model/provider or the profile lacks its own `config.yaml`. Do not assume global inheritance is sufficient for dispatcher-spawned work.

For each incomplete role, configure the intended route explicitly:

```bash
hermes -p <profile> config set model.default <model>
hermes -p <profile> config set model.provider <provider>
hermes -p <profile> config set model.base_url <endpoint>
hermes -p <profile> config set model.api_mode <mode>
hermes -p <profile> config set agent.max_turns <n>
hermes -p <profile> config set agent.reasoning_effort <level> --force
```

Use role-appropriate limits rather than copying an arbitrary profile wholesale. For a Codex-backed fleet, use the already authenticated `openai-codex` route only after verifying that the selected model and auth method are intended.

### 3. Verify every profile without spending model calls

Run `hermes -p <profile> config check` for every profile and then:

```bash
hermes doctor
```

The profile section should report a concrete model for every profile. Configuration checks validate parsing and required surfaces; they do not validate generation quality.

### 4. Verify Kanban routing before spawning

Inspect the current board:

```bash
hermes kanban list
hermes kanban stats
hermes kanban dispatch --dry-run --max <n> --json
```

The dry-run result must not contain `skipped_nonspawnable`, `skipped_unassigned`, or unexpected profile-cap skips for the tasks being refreshed. It proves assignee resolution only; it does not prove that a worker process will stay alive.

### 5. Refresh stale workers safely

For each running task, compare the last heartbeat and claim expiry with the current time, then check the recorded worker PID. Reclaim only tasks whose lease is expired or whose worker process is absent:

```bash
hermes kanban reclaim <task_id> --reason "stale worker: expired heartbeat/lease and absent PID"
```

After reclaiming, run a bounded dispatcher pass. Verify the resulting task status, current run id, PID, heartbeat, claim expiry, and process liveness. If the worker exits without `kanban_complete` or `kanban_block`, reclaim the resulting stale claim and report a worker-protocol failure rather than calling it healthy.

### 6. Keep service health separate

The Kanban dispatcher normally runs in the gateway. Verify the service independently with:

```bash
hermes gateway status
```

If a service wrapper or launchd/systemd definition contains an argument rejected by the installed CLI, classify that as an installation/service-boundary issue. Do not claim that profile configuration fixed the gateway. Avoid repeated service restart loops; capture the exact wrapper command and error, then use the supported service-install or update path.

## Role-routing defaults

These are starting points, not universal mandates:

- architect: high reasoning, long turn budget, analysis/design work
- implementer: high reasoning, longest turn budget, code/tool execution
- engineering: high reasoning, broad implementation/integration work
- reviewer: medium-to-high reasoning, bounded review budget
- tester: medium reasoning, deterministic test/verification budget
- debugger: high reasoning, diagnostic/tool budget

Tune the model and provider from live auth/catalog evidence. Never claim a model is optimal without workload-based evidence.

## Completion checklist

- [ ] Every configured profile has a concrete model/provider in `profile show`.
- [ ] Every Kanban assignee resolves to an on-disk profile.
- [ ] Every profile passes `config check`.
- [ ] `hermes doctor` has no missing-profile-config findings.
- [ ] Kanban dry-run has no unexpected non-spawnable or unassigned tasks.
- [ ] Refreshed workers have live PIDs and fresh heartbeats.
- [ ] Worker completion follows the Kanban protocol.
- [ ] Gateway/dispatcher health is verified separately.
- [ ] Secrets were not printed or copied into skill artifacts.

## Pitfalls

- An alias, `.env`, skills directory, and `SOUL.md` do not prove that a profile has a usable model configuration.
- A dry-run spawn result does not prove the worker can authenticate, stay alive, heartbeat, or complete.
- A task marked `running` may be a stale database claim; always check lease, heartbeat, and PID.
- Reclaiming stale tasks is not the same as successfully refreshing them.
- Do not patch launchd/systemd files repeatedly when the service installer regenerates a stale template; classify the wrapper/runtime mismatch and preserve the exact evidence.
- Do not print auth files, environment secrets, or full request dumps while auditing profiles.

## Support files

- `references/profile-fleet-readiness-checklist.md` — concise audit matrix and verification fields for profile/alias/assignee checks.
