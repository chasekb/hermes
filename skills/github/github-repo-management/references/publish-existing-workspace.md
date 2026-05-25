# Publishing an Existing Workspace to GitHub

Use this when the user says “create a git repository and commit and push” for a directory that already has files.

## Standard flow

1. Inspect the tree and status first.
   - `git status --short`
   - `git remote -v`
   - `git branch --show-current`
2. Screen for secrets, large artifacts, and generated files before the first commit.
   - Add a `.gitignore` before `git add .` if the repo is meant to be public or shared.
3. If the workspace is not yet a repo:
   - `git init`
   - choose/rename the initial branch if needed
4. Create the remote and push in one step when possible:
   - `gh repo create <name> --public|--private --source . --remote origin --push`
5. If `gh` is unavailable:
   - create the repo via API or web UI
   - `git remote add origin <url>`
   - `git add . && git commit -m "Initial commit"`
   - `git push -u origin main`
6. Verify the result:
   - `git remote -v`
   - `git status --short`
   - `gh repo view` or open the repo URL

## Public repo hygiene

- If the repo is public, do not rush to publish without a quick allowlist-style review of obvious secrets, caches, and build artifacts.
- If the repo already contains a tracked `data/` tree, do not ignore the whole directory by reflex; prefer narrow ignore rules for runtime-only generated subpaths.

## Common branch-name pitfall

If the default branch is not `main`, push the correct branch and set upstream explicitly:

```bash
git push -u origin HEAD
```

or rename the branch before the first push if that is the project convention.
