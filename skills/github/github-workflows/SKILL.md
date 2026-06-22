---
name: github-workflows
description: "Use when working across GitHub auth, repositories, pull requests, reviews, issues, and Actions verification."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [GitHub, auth, repositories, pull-requests, code-review, issues, actions, CI]
    related_skills: []
---

# GitHub Workflows

Use this umbrella when the task spans the GitHub lifecycle end to end: authentication, repository setup, pull requests, code review, issue triage, release flows, and GitHub Actions verification.

This skill absorbs the narrower GitHub workflow skills that used to be split apart:
- GitHub auth setup
- Repository creation, fork, and remote management
- Pull request lifecycle and CI monitoring
- PR / local code review
- Issue creation and triage

## Core rule

Prefer `gh` when it is available and authenticated. Fall back to `git` + `curl` only when you need portability or the CLI is unavailable.

## 1. Authenticate first

- Check whether `gh` is installed and logged in.
- If not, set up either:
  - HTTPS PAT credentials for `git` + API calls, or
  - SSH keys for Git transport.
- Confirm the chosen auth method before attempting repo or PR work.

## 2. Repository operations

Use this lane for:
- clone
- create
- fork
- sync remotes
- update repository settings
- manage releases and tags

Rule of thumb: if the task starts with "get the repo into the right shape," this is the section to follow.

## 3. Pull requests and CI

Use this lane for:
- branch creation and commits
- PR creation and metadata
- monitoring GitHub Actions
- verifying the exact run created by the latest push
- waiting for matrix jobs to finish before declaring success
- merging when checks are green

Always match the workflow run against the pushed commit SHA, not just the newest run on the branch.

### Remote build verification pattern

When the user asks to "push and verify" or "use GitHub Actions to verify":
1. Commit and push the local changes.
2. Resolve the exact workflow run created by that push.
3. Verify the run by SHA, URL, and final conclusion.
4. Report the run URL and head SHA back to the user.

Preferred commands:
- `gh run list --branch <branch> --limit <n>` to find the candidate run.
- Prefer the newest run on the branch and verify its `headSha` matches the commit you just pushed.
- `gh run view <run_id> --json status,conclusion,headSha,url,name,updatedAt` to verify the exact run.
- `gh run watch <run_id> --exit-status` is useful, but if it times out, fall back to polling `gh run view --json status,conclusion,headSha,url,name,updatedAt` (optionally with short sleeps) until the run completes.
- If a newer push starts a new run while you are watching an older one, switch to the newest run and verify that SHA instead.

If the repository has no existing GitHub Actions workflows, add a minimal verification workflow first, push it, and then verify the run it creates. In that case, the workflow file itself becomes part of the proof chain.

For large Docker/build matrices, verify both the overall run and the individual jobs; one job can still be running after other jobs and publish steps complete. Report the run URL and pushed head SHA together as the source-of-truth proof.

If a push is rejected because the remote moved, rebase onto the remote branch first and push again. Do not treat the first push as the source of truth when GitHub shows a newer remote head.

Reference: `references/ci-verification.md` for a compact checklist and command sequence. See also `references/ci-verification-no-workflow.md` for the "bootstrap a workflow, then verify it" case. For long-running push verifications, see `references/remote-build-monitoring.md` (stop local builds first, then verify the exact run for the pushed SHA). If the workflow list is empty, inspect `.github/workflows/` in the repo before assuming GitHub auth or Actions is broken.

## 4. Reviews and issues

Use this lane for:
- reviewing local diffs before push
- reviewing someone else's PR on GitHub
- leaving inline review comments
- opening, labeling, assigning, and closing issues
- triage and bug report templates

Separate "pre-commit review of my changes" from "PR review of someone else's changes" even though both are review workflows.

## 5. Practical verification pattern

When a repository has no workflow yet, bootstrap one before trying to verify the push. The proof chain is: workflow file in the push, run created by that push, run URL, head SHA, final success.

1. Auth is valid.
2. Remote and branch state are known.
3. The diff or PR scope is explicitly identified.
4. The relevant GitHub side effect is performed.
5. The result is re-checked from GitHub's source of truth.

## Common pitfalls

- Assuming a local git state implies GitHub state is correct.
- Treating a PR title as proof of the underlying run.
- Missing the distinction between repo setup, PR workflow, and review workflow.
- Forgetting that issue search can return PRs unless you filter them out.
- Using `git add -u` when the user asked to commit "all changes": it stages tracked modifications and deletions only, so new skill files/directories remain untracked. Use `git add -A` (or explicitly add new paths) when the request includes new files.
- When the workspace has generated caches or local state files, inspect `git status` before staging and commit only the files that are meant to be tracked; do not let incidental cache churn ride along with a docs/code change.

## Verification

- `gh auth status` or equivalent token/SSH check succeeds.
- Repo/remote operations affect the intended repository.
- PR or issue actions appear in GitHub exactly where expected.
- Actions verification cites the exact run URL and head SHA.
- Review comments land on the intended lines.
