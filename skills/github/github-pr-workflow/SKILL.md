---
name: github-pr-workflow
description: "GitHub PR lifecycle: branch, commit, open, CI, merge."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [GitHub, Pull-Requests, CI/CD, Git, Automation, Merge]
    related_skills: [github-auth, github-code-review]
---

# GitHub Pull Request Workflow

Complete guide for managing the PR lifecycle. Each section shows the `gh` way first, then the `git` + `curl` fallback for machines without `gh`.

## Prerequisites

- Authenticated with GitHub (see `github-auth` skill)
- Inside a git repository with a GitHub remote

### Quick Auth Detection

When the user explicitly asks to verify that a build completed successfully via GitHub Actions, treat Actions as the source of truth. Do not summarize from local test output alone. The report must include the workflow run URL and the verified `headSha` from the run JSON, plus the terminal `status` and `conclusion`.

### Evidence standard for remote build verification

When Actions is the proof source, the final answer should be anchored to one exact run:
- workflow run URL
- verified `headSha`
- terminal `status`
- terminal `conclusion`
- a short note on the required jobs that mattered (especially for matrix builds)

Never call the build successful if any required job is still running, even if another job has already turned green. If the run is incomplete, say so plainly and keep polling the same run id.


```bash
# Determine which method to use throughout this workflow
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  AUTH="gh"
else
  AUTH="git"
  # Ensure we have a token for API calls
  if [ -z "$GITHUB_TOKEN" ]; then
    if [ -f ~/.hermes/.env ] && grep -q "^GITHUB_TOKEN=" ~/.hermes/.env; then
      GITHUB_TOKEN=$(grep "^GITHUB_TOKEN=" ~/.hermes/.env | head -1 | cut -d= -f2 | tr -d '\n\r')
    elif grep -q "github.com" ~/.git-credentials 2>/dev/null; then
      GITHUB_TOKEN=$(grep "github.com" ~/.git-credentials 2>/dev/null | head -1 | sed -E 's|https://[^:]+:([^@]+)@.*|\1|')
    fi
  fi
fi
echo "Using: $AUTH"
```

### Extracting Owner/Repo from the Git Remote

Many `curl` commands need `owner/repo`. Extract it from the git remote:

```bash
# Works for both HTTPS and SSH remote URLs
REMOTE_URL=$(git remote get-url origin)
OWNER_REPO=$(echo "$REMOTE_URL" | sed -E 's|.*github\.com[:/]||; s|\.git$||')
OWNER=$(echo "$OWNER_REPO" | cut -d/ -f1)
REPO=$(echo "$OWNER_REPO" | cut -d/ -f2)
echo "Owner: $OWNER, Repo: $REPO"
```

---

## 1. Branch Creation

This part is pure `git` — identical either way:

```bash
# Make sure you're up to date
git fetch origin
git checkout main && git pull origin main

# Create and switch to a new branch
git checkout -b feat/add-user-authentication
```

Branch naming conventions:
- `feat/description` — new features
- `fix/description` — bug fixes
- `refactor/description` — code restructuring
- `docs/description` — documentation
- `ci/description` — CI/CD changes

## 2. Making Commits

Use the agent's file tools (`write_file`, `patch`) to make changes, then commit:

```bash
# Stage specific files
git add src/auth.py src/models/user.py tests/test_auth.py

# Commit with a conventional commit message
git commit -m "feat: add JWT-based user authentication

- Add login/register endpoints
- Add User model with password hashing
- Add auth middleware for protected routes
- Add unit tests for auth flow"
```

Commit message format (Conventional Commits):
```
type(scope): short description

Longer explanation if needed. Wrap at 72 characters.
```

Types: `feat`, `fix`, `refactor`, `docs`, `test`, `ci`, `chore`, `perf`

## 3. Pushing and Creating a PR

### Push the Branch (same either way)

```bash
git push -u origin HEAD
```

### Create the PR

**With gh:**

```bash
gh pr create \
  --title "feat: add JWT-based user authentication" \
  --body "## Summary
- Adds login and register API endpoints
- JWT token generation and validation

## Test Plan
- [ ] Unit tests pass

Closes #42"
```

Options: `--draft`, `--reviewer user1,user2`, `--label "enhancement"`, `--base develop`

**With git + curl:**

```bash
BRANCH=$(git branch --show-current)

curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/$OWNER/$REPO/pulls \
  -d "{
    \"title\": \"feat: add JWT-based user authentication\",
    \"body\": \"## Summary\nAdds login and register API endpoints.\n\nCloses #42\",
    \"head\": \"$BRANCH\",
    \"base\": \"main\"
  }"
```

The response JSON includes the PR `number` — save it for later commands.

To create as a draft, add `"draft": true` to the JSON body.

## 4. Monitoring CI Status

### Check CI Status

**With gh:**

```bash
# One-shot check
gh pr checks

# Watch until all checks finish (polls every 10s)
gh pr checks --watch
```

### Remote-only verification pattern

When the user wants GitHub Actions to be the source of truth, treat the request as remote-only verification: do not perform local build/test checks first unless the user explicitly asks for them. Commit, push, then verify the workflow run on GitHub Actions.

Verify the exact workflow run created by the latest push by matching both the branch and the commit SHA (`headSha`). If you only see a partially completed run, keep polling that same run until every required job is completed. Never report success while any required job is still running.

For long-running builds, prefer repeated `gh run view <RUN_ID> --json ...` checks over a single watch command; the JSON view is the source of truth because it includes the run `status`, `conclusion`, and job states in one place.

Practical lessons:
- The authoritative signal is `gh run view <run_id> --json status,conclusion,jobs,headSha,url`.
- A run is only done when `status=completed` and `conclusion=success`.
- If some jobs are green but another required job is still running, the workflow is unresolved.
- `gh run watch` is optional convenience; polling `gh run view` on the same run id is the more reliable fallback when watch times out or the API blips.
- If GitHub returns a transient network/API error, retry the same run id rather than assuming failure.
- When reporting the result, include the run URL and the exact headSha you verified so there is no ambiguity about which build passed.
- If a workflow is a matrix build, require every required job to reach a terminal success state before declaring the run successful; do not equate a single passing lane with overall success.
- When the user asks to "use GitHub Actions to verify build completed successfully," answer with the final run URL, the verified `headSha`, and the terminal `status`/`conclusion` from the run JSON.

See `references/remote-build-verification-runbook.md` for the compact checklist and command set.
See `references/remote-build-verification-with-github-actions.md` for a worked example of remote-only build verification after a push.
See `references/remote-build-verification-session-notes.md` for a real-world note on matching the exact run, polling matrix jobs, and reporting the verified `headSha`.
See `references/github-actions-matrix-remote-proof.md` for the exact matrix-build proof pattern: match branch + `headSha`, require every required job to finish, and do not treat early frontend success as overall success.
See `references/remote-build-proof-bundle.md` for the minimal evidence bundle to include in a final success report.
See `references/docker-build-validation-matrix-debugging.md` for a concrete matrix-debugging session where the backend failure moved from linker errors to ONNX export smoke-test failures.
See `references/ci-linkage-drift.md` for a concrete linker-failure pattern where a shared source file needed additional target link libraries.
See `references/no-workflow-no-run-verification.md` for the case where `gh run list` is empty and workflow inventory is zero.
See `references/github-actions-verification-evidence.md` for the minimal proof bundle to capture when a user explicitly wants CI verification as evidence.

### Verify a long-running GitHub Actions build

For long remote builds, prefer querying the workflow run directly instead of depending on a long live watch. This gives you a clean success/failure signal and a stable place to re-check progress.

Extra reliability rules learned in the field:
- Match the exact workflow run created by the push: verify both branch and `headSha` before treating a run as authoritative.
- If a workflow is still in progress, keep polling the same run id; do not infer failure from an intermediate state.
- Do not report success until every job in the run is completed with `conclusion=success`.
- If one or more jobs are still running while others are green, treat the workflow as unresolved, not successful.
- `gh run watch` is optional convenience, not the source of truth; a polling loop around `gh run view` is the fallback when watch times out or is inconvenient.
- When the user explicitly asks for remote-only verification, skip local build/test verification and move straight to commit/push + Actions monitoring.
- If `gh`/GitHub API calls time out briefly, retry the same run id rather than assuming the build failed.

```bash
# Find the latest run for the branch or commit
gh run list --branch <branch> --limit 10 --json databaseId,status,conclusion,workflowName,headSha,displayTitle,url,createdAt

# Inspect run + job/step progress
gh run view <RUN_ID> --json status,conclusion,jobs,url,workflowName,headSha,displayTitle

# Optional live log stream when you want it
gh run watch <RUN_ID> --exit-status
```

Rules of thumb:
- Use `gh run view` as the authoritative source for final verification.
- If a run is still in progress, re-run the same `gh run view` command later rather than assuming failure.
- `gh run watch` is useful for interactive log viewing, but for long or matrix-heavy builds a polling loop around `gh run view` is more reliable and easier to reason about.
- Treat temporary `gh`/GitHub API timeouts as transient noise: retry the same run id later instead of concluding the workflow failed.
- If one job is still running, do not report the workflow as successful yet even if other jobs have finished.
- When the user explicitly asks for a remote build only, do not perform local build/test verification first. Commit and push the change, then verify the workflow run on GitHub Actions.
- Verify the exact run created by that push by matching both branch and `headSha` before declaring success; this avoids confusing the intended run with an older or unrelated run on the same branch.
- Do not claim success until the run is `completed` with `conclusion=success`.
- For matrix workflows, capture the job list from `gh run view --json ... ,jobs` and require every required job to reach a terminal success state before reporting completion.
- When a newer push lands on the same branch, keep verifying the intended `headSha`; the latest branch run is not automatically the right run for the question being asked.

See `references/remote-build-verification-runbook.md` for the compact runbook, `references/long-running-build-polling.md` for a resilient polling pattern, and `references/remote-build-verification-session-notes.md` for a concise field note from a real matrix-build verification session.

**With git + curl:**

```bash
# Get the latest commit SHA on the current branch
SHA=$(git rev-parse HEAD)

# Query the combined status
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/commits/$SHA/status \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f\"Overall: {data['state']}\")
for s in data.get('statuses', []):
    print(f\"  {s['context']}: {s['state']} - {s.get('description', '')}\")"

# Also check GitHub Actions check runs (separate endpoint)
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/commits/$SHA/check-runs \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
for cr in data.get('check_runs', []):
    print(f\"  {cr['name']}: {cr['status']} / {cr['conclusion'] or 'pending'}\")"
```

### Poll Until Complete (git + curl)

```bash
# Simple polling loop — check every 30 seconds, up to 10 minutes
SHA=$(git rev-parse HEAD)
for i in $(seq 1 20); do
  STATUS=$(curl -s \
    -H "Authorization: token $GITHUB_TOKEN" \
    https://api.github.com/repos/$OWNER/$REPO/commits/$SHA/status \
    | python3 -c "import sys,json; print(json.load(sys.stdin)['state'])")
  echo "Check $i: $STATUS"
  if [ "$STATUS" = "success" ] || [ "$STATUS" = "failure" ] || [ "$STATUS" = "error" ]; then
    break
  fi
  sleep 30
done
```

## 5. Auto-Fixing CI Failures

When CI fails, diagnose and fix. This loop works with either auth method.

### Step 1: Get Failure Details

**With gh:**

```bash
# List recent workflow runs on this branch
gh run list --branch $(git branch --show-current) --limit 5

# View failed logs
gh run view <RUN_ID> --log-failed
```

**With git + curl:**

```bash
BRANCH=$(git branch --show-current)

# List workflow runs on this branch
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/$OWNER/$REPO/actions/runs?branch=$BRANCH&per_page=5" \
  | python3 -c "
import sys, json
runs = json.load(sys.stdin)['workflow_runs']
for r in runs:
    print(f\"Run {r['id']}: {r['name']} - {r['conclusion'] or r['status']}\")"

# Get failed job logs (download as zip, extract, read)
RUN_ID=<run_id>
curl -s -L \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/actions/runs/$RUN_ID/logs \
  -o /tmp/ci-logs.zip
cd /tmp && unzip -o ci-logs.zip -d ci-logs && cat ci-logs/*.txt
```

### Step 2: Fix and Push

After identifying the issue, use file tools (`patch`, `write_file`) to fix it:

```bash
git add <fixed_files>
git commit -m "fix: resolve CI failure in <check_name>"
git push
```

### Step 3: Verify

Re-check CI status using the commands from Section 4 above.

### Auto-Fix Loop Pattern

When asked to auto-fix CI, follow this loop:

1. Check CI status → identify failures
2. Read failure logs → understand the error
3. Use `read_file` + `patch`/`write_file` → fix the code
4. `git add . && git commit -m "fix: ..." && git push`
5. Wait for CI → re-check status
6. Repeat if still failing (up to 3 attempts, then ask the user)

See `references/push-and-ci-rebase.md` for the push/rebase/host-key pattern and the CI verification flow.

## 6. Merging

**With gh:**

```bash
# Squash merge + delete branch (cleanest for feature branches)
gh pr merge --squash --delete-branch

# Enable auto-merge (merges when all checks pass)
gh pr merge --auto --squash --delete-branch
```

**With git + curl:**

```bash
PR_NUMBER=<number>

# Merge the PR via API (squash)
curl -s -X PUT \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER/merge \
  -d "{
    \"merge_method\": \"squash\",
    \"commit_title\": \"feat: add user authentication (#$PR_NUMBER)\"
  }"

# Delete the remote branch after merge
BRANCH=$(git branch --show-current)
git push origin --delete $BRANCH

# Switch back to main locally
git checkout main && git pull origin main
git branch -d $BRANCH
```

Merge methods: `"merge"` (merge commit), `"squash"`, `"rebase"`

### Enable Auto-Merge (curl)

```bash
# Auto-merge requires the repo to have it enabled in settings.
# This uses the GraphQL API since REST doesn't support auto-merge.
PR_NODE_ID=$(curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['node_id'])")

curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/graphql \
  -d "{\"query\": \"mutation { enablePullRequestAutoMerge(input: {pullRequestId: \\\"$PR_NODE_ID\\\", mergeMethod: SQUASH}) { clientMutationId } }\"}"
```

## 7. Complete Workflow Example

```bash
# 1. Start from clean main
git checkout main && git pull origin main

# 2. Branch
git checkout -b fix/login-redirect-bug

# 3. (Agent makes code changes with file tools)

# 4. Commit
git add src/auth/login.py tests/test_login.py
git commit -m "fix: correct redirect URL after login

Preserves the ?next= parameter instead of always redirecting to /dashboard."

# 5. Push
git push -u origin HEAD

# 6. Create PR (picks gh or curl based on what's available)
# ... (see Section 3)

# 7. Monitor CI (see Section 4)

# 8. Merge when green (see Section 6)
```

## Useful PR Commands Reference

| Action | gh | git + curl |
|--------|-----|-----------|
| List my PRs | `gh pr list --author @me` | `curl -s -H "Authorization: token $GITHUB_TOKEN" "https://api.github.com/repos/$OWNER/$REPO/pulls?state=open"` |
| View PR diff | `gh pr diff` | `git diff main...HEAD` (local) or `curl -H "Accept: application/vnd.github.diff" ...` |
| Add comment | `gh pr comment N --body "..."` | `curl -X POST .../issues/N/comments -d '{"body":"..."}'` |
| Request review | `gh pr edit N --add-reviewer user` | `curl -X POST .../pulls/N/requested_reviewers -d '{"reviewers":["user"]}'` |
| Close PR | `gh pr close N` | `curl -X PATCH .../pulls/N -d '{"state":"closed"}'` |
| Check out someone's PR | `gh pr checkout N` | `git fetch origin pull/N/head:pr-N && git checkout pr-N` |
