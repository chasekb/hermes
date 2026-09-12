# Hermes configuration control plane

This repository is the configuration and operations policy plane for the installed Hermes Agent at `/home/kahlil/.hermes/hermes-agent`.

The Hermes implementation is maintained separately by upstream `NousResearch/hermes-agent`. `chasekb/hermes.git` is not a forked implementation branch and must not contain Hermes runtime modules, source tests, plugins, packaging, release machinery, or source CI.

Repository contents

- `config.yaml` — sanitized installation-local settings and safety policy.
- `SOUL.md` — operator identity and behavior policy.
- `skills/` — curated reusable skills and workflow documentation.
- `notes/` — sanitized project notes and research supporting configuration decisions.
- `backlog/` — durable intake, decision memory, and Kanban workflow records.
- `CONTROL_PLANE_MANIFEST.md` — retained/removed boundary and classification record.

The repository may document or configure behavior around the installed checkout, but it does not implement Hermes. Keep credentials, runtime databases, sessions, caches, logs, generated artifacts, and machine-specific overlays outside version control. Use `$HERMES_HOME` or explicit local environment/configuration overlays for installation-specific paths; never commit secrets or private `.env` contents.

The canonical architecture and Kanban scope are documented in `notes/Projects/hermes/Hermes Agent Decision Plane.md`.
