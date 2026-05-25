# Repo hygiene: tracked data vs runtime data

When a repository has a `data/` directory, do not assume the whole tree should be ignored.

Signals:
- `git ls-files data` shows committed artifacts under `data/`.
- `git status --short` shows only some subpaths as untracked runtime output.

Pattern:
- Keep versioned artifacts tracked (models, checked-in configs, seed DBs, golden test data).
- Ignore only ephemeral/generated subdirectories, such as:
  - `data/cache/`
  - `data/databases/postgres/`
  - `data/trained_models/`

Rule of thumb:
- If a top-level directory already contains tracked files, avoid adding the entire directory to `.gitignore` unless you also plan to stop tracking the committed files and clean the index.
- Prefer narrow ignore patterns for runtime outputs.

If a deletion command is blocked by tool safety:
- Treat that as a tooling guard, not a Git refusal.
- Confirm the scope first, then use the safest available method to remove the intended files/directories without disturbing unrelated working-tree changes.
