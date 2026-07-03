# Purging a tracked generated tree

Use this when a generated/runtime directory (for example `data/`) is already tracked and the user wants it fully ignored.

## Key rule
Adding the path to `.gitignore` is not enough if files are already in git history or currently tracked.

## Safe sequence
1. Confirm the tree really is generated/runtime content and not intended source data.
2. Add the directory to `.gitignore` for future protection.
3. Commit that ignore rule if the repo should preserve it.
4. Rewrite history to remove the tree from all commits and branches.
   - `git filter-repo --path <dir>/ --invert-paths` is preferred when available.
   - `git filter-branch --index-filter 'git rm -r --cached --ignore-unmatch <dir>' --prune-empty --tag-name-filter cat -- --all` works as a fallback, but is slower and leaves refs/original cleanup behind.
5. Force-push rewritten branches that were shared remotely.
6. Delete rewrite backups and stale refs locally:
   - backup branch used for safety
   - `refs/original/*`
   - reflogs if needed
7. Verify:
   - `git ls-files <dir>` returns nothing
   - `git status --short` is clean except for intended untracked runtime dirs
   - remote branch SHA matches the rewritten history after force-push

## Pitfalls
- Do not try to rewrite history before the working tree is clean; commit or stash first.
- Do not force-push until you’ve confirmed the rewritten branch is the one you want to keep.
- If the repo has protected branches or CI gates, warn the user that remote history will change.
- Removing the tree from history can invalidate old SHAs in open PRs and cached builds; mention that explicitly.
