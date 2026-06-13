# Hermes debugging capability selection note

Session note: when a user asks to "install debugging toolset" on Hermes, first verify whether the current build actually exposes a `debugging` toolset.

Observed behavior on this session:
- `hermes tools enable debugging` returned `Unknown toolset 'debugging'`.
- `hermes skills search debugging --json` surfaced debugging-related skills instead of a toolset.
- The useful debugging capability on this build is skill-based, not a dedicated toolset.

Practical guidance:
1. Check `hermes tools list` before assuming a toolset exists.
2. If `debugging` is absent, treat the request as a skill discovery/install question.
3. Prefer class-level debugging skills such as `systematic-debugging` for general workflow, and specialized skills like `python-debugpy`, `node-inspect-debugger`, or `debugging-hermes-tui-commands` when the target stack is specific.
4. Avoid retrying `hermes tools enable debugging` once the CLI has already reported the toolset is unknown.

This note is intentionally narrow: it records the Hermes capability-discovery pitfall, not a general build/install rule.