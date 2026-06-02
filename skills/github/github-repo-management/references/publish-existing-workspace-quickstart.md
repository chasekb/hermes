# Minimal publish flow for an existing workspace

Use this when the user asks to create a git repository, commit, and push from the current directory.

```bash
git status --short --branch
[ -d .git ] || git init
# Add a .gitignore before the first add if this repo will be shared publicly.
git add .
git commit -m "Initial commit"
git remote get-url origin >/dev/null 2>&1 || git remote add origin <repo-url>
git push -u origin HEAD
git status --short --branch
```

Verification rule:
- The final status should be clean and show the branch tracking `origin/<branch>`.
- If the branch name is not known, `git push -u origin HEAD` avoids guessing.
