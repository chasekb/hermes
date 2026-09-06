---
name: plugin-compatibility-migrations
description: "Use when plugin import paths are deprecated."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [plugins, compatibility, migrations, imports, debugging]
---

# Plugin Compatibility Migrations

Use this class-level workflow when a Hermes plugin compatibility report identifies imports or symbols that will stop resolving after a compatibility window. The goal is a real runtime migration, not merely a clean static diff.

## Procedure

1. Capture the reported runtime context.
   - Save the relevant tmux pane or log tail when the warning came from an interactive process.
   - Run `hermes plugins compat` and record the complete affected-plugin table, removal state, and exit code.
   - Preserve unrelated working-tree changes; compatibility work must stay scoped to the listed plugin files.

2. Establish the two source roots.
   - Locate the active plugin copy under the Hermes home and the canonical Hermes checkout used by the running interpreter.
   - Read the replacement module and its package layout before editing.
   - Verify importability with the same virtualenv and source path used by Hermes. A replacement that exists only in a nested checkout is a source-root issue, not a reason to add a shim.

3. Trace every hit.
   - Search the affected plugin tree for the old module and symbol, including dynamic imports and attribute access.
   - Search sibling plugins for the canonical import pattern.
   - Distinguish actual deprecated symbol references from intentional imports of a facade that remains part of the public plugin seam.

4. Migrate to the canonical definition.
   - Replace deprecated imports with the defining sibling module named by the compatibility report.
   - For moved symbols, import the defining module/function/class directly rather than retaining a facade re-export.
   - Keep deliberate test seams and cache slots only when they do not preserve the deprecated path; changing a patch seam can silently invalidate behavioral tests.
   - Do not edit core compatibility machinery to silence an external-plugin report, and do not create per-plugin aliases for removed paths.

5. Verify the real load path.
   - Run canonical-module import smoke tests in Hermes's virtualenv, loading each touched plugin through its normal package path.
   - Run `python scripts/check_compat_pointers.py` from the Hermes checkout.
   - Run `hermes plugins compat` again and require zero enabled-plugin hits scheduled for removal.
   - Compile or syntax-check each touched plugin and run the narrowest relevant tests; report any gateway restart requirement separately from source verification.

## Pitfalls

- Capture before changing files because the pane often contains the exact old/new path table and removal deadline needed to scope the migration.
- Never infer the import root from the repository's current directory; Hermes can execute a nested checkout while discovering user-home plugins, so a direct import test from the wrong interpreter gives a false failure.
- Do not copy a newer in-tree plugin wholesale over a user plugin just to remove warnings; migrate the reported symbols and preserve local behavior.
- Treat a zero-warning CLI result as necessary but not sufficient: import the touched plugins through the runtime environment because static compatibility scanning cannot prove the new path loads.
- Do not claim a gateway is current solely because restart was requested; source compatibility and live-process version verification are separate checks.

## Reference

See `references/plugin-compatibility-migration.md` for the reusable command sequence and source-root decision table.
