# Profile fleet readiness checklist

Use this matrix before refreshing Kanban workers.

| Boundary | Command/evidence | Pass condition |
|---|---|---|
| Profile roster | `hermes profile list` | Every intended role is present |
| Profile details | `hermes profile show <name>` | Concrete model/provider is reported |
| Config file | `<profile>/config.yaml` existence check | Role profiles have explicit config |
| Assignee mapping | `hermes kanban assignees` | Board assignees are on-disk/spawnable |
| Config parsing | `hermes -p <name> config check` | Exit code 0; no config errors |
| Runtime health | `hermes doctor` | No missing-profile-config findings |
| Board routing | `hermes kanban dispatch --dry-run --json` | No unexpected non-spawnable/unassigned skips |
| Worker liveness | Task DB + `ps` | PID exists and heartbeat is fresh |
| Completion protocol | Task events/runs | Worker calls `kanban_complete` or `kanban_block` |
| Service boundary | `hermes gateway status` | Gateway state is evaluated independently |

## Safe evidence rules

- Record model/provider names and status fields, not credential contents.
- Do not print `.env`, `auth.json`, request dumps, or full gateway logs.
- A dry-run is a routing check, not a worker smoke test.
- Reclaim only expired or PID-less claims; verify the post-reclaim state.
- If a worker exits cleanly without a terminal Kanban call, classify it as a protocol failure and do not report it as refreshed.
