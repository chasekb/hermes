# Global orchestrator + project-specific clones

This layout came up in a real session and is the recommended pattern when you want one canonical orchestrator and separate project-specific variants.

## Recommended structure

- One canonical profile: `orchestrator-global`
- One cloned profile per project: `project-alpha`, `project-beta`, etc.
- One shared skill source of truth for `kanban-orchestrator`

Example filesystem shape:

```text
~/.hermes/
├── skills/
│   └── (shared skill source or external_dirs target)
└── profiles/
    ├── orchestrator-global/
    │   ├── config.yaml
    │   ├── .env
    │   └── notes.md
    ├── project-alpha/
    │   ├── config.yaml
    │   ├── .env
    │   └── notes.md
    └── project-beta/
        ├── config.yaml
        ├── .env
        └── notes.md
```

## Practical rules

- Treat the global profile as the template, not a shared runtime instance.
- Clone the global profile for each project.
- Keep project-specific overrides local to the clone.
- Use `skills.external_dirs` if you want all profiles to load the same canonical skill source.
- Use kanban board state for live work; use profile clones for policy/configuration.

## Suggested settings for the canonical profile

```yaml
delegation:
  orchestrator_enabled: true
  max_spawn_depth: 2
  max_concurrent_children: 3
  inherit_mcp_toolsets: true

kanban:
  dispatch_in_gateway: true
  auto_decompose: true
```

## Helpful commands

```bash
hermes profile create orchestrator-global --clone --description "Canonical multi-agent orchestrator"
hermes profile create project-alpha --clone-from orchestrator-global --description "Alpha project orchestrator"
hermes profile create project-beta --clone-from orchestrator-global --description "Beta project orchestrator"
```

## Caveat

Profiles are isolated. There is no single live orchestrator instance shared across projects; you get a shared skill policy plus cloned profile state.