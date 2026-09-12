# Hermes Agent decision plane

Status: canonical architecture for the `hermesagent` Kanban board.

## Repository roles

`chasekb/hermes.git` is the personal Hermes configuration and operations repository for the installed Hermes Agent under `/home/kahlil/.hermes/hermes-agent`.

The installed source checkout remains separate:

- Installation/source: `/home/kahlil/.hermes/hermes-agent`
- Upstream source remote: `NousResearch/hermes-agent`
- Configuration/operations repository: `chasekb/hermes.git`
- Current configuration-repository checkout: `/home/kahlil/work/hermes`

The configuration repository is not a forked implementation branch. Its purpose is to describe and maintain installation-local configuration choices, profiles, skills, operator workflows, Kanban policy, and sanitized documentation that are applied around the installed upstream checkout.

## Kanban decision rule

The `hermesagent` board is a Hermes-local configuration decision plane. A task may reference `chasekb/hermes.git` only when the requested change is configuration or operating policy for the `/home/kahlil/.hermes/hermes-agent` installation.

Allowed task scope includes:

- profile, SOUL, skill-discovery, gateway, approval, and redaction configuration;
- Kanban board/project metadata, routing policy, operator scripts, and workflow artifacts;
- sanitized installation documentation and configuration validation that does not implement Hermes source behavior.

Disallowed task scope includes:

- changes to Hermes implementation modules, tests, plugins, CI workflows, or release code;
- fork-branch feature work, bug fixes, or pull requests against `chasekb/hermes.git`;
- source worktrees or branch-based implementation tasks whose acceptance depends on modifying the repository's Python, TypeScript, or other product source;
- changes to `/home/kahlil/.hermes/hermes-agent` source files unless a separate user request explicitly names that repository and action.

## Enforcement

Before dispatching a repository-related card, verify all of the following:

1. The card states the installation/configuration target, not a source implementation target.
2. The requested files are configuration, policy, skills, operator artifacts, or documentation.
3. The workspace is not being used as an implicit source-implementation worktree.
4. The card does not request a branch, pull request, source CI, or source-code tests.
5. If any check fails, archive the card as misrouted history and create a replacement card with the configuration-only scope. Do not mutate the old card into a different architectural meaning.

Completed historical source cards remain archived for auditability; they are not evidence that source implementation work is still an accepted responsibility of this board.
