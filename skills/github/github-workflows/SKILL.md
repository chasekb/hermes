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
- `gh run view <run_id> --json status,conclusion,headSha,url,name,updatedAt` to verify the exact run.
- `gh run watch <run_id> --exit-status` is useful, but if it times out, fall back to polling `gh run view --json status --jq '.status'` until the run completes.

If a push is rejected because the remote moved, rebase onto the remote branch first and push again. Do not treat the first push as the source of truth when GitHub shows a newer remote head.

Reference: `references/ci-verification.md` for a compact checklist and command sequence.

## 4. Reviews and issues

Use this lane for:
- reviewing local diffs before push
- reviewing someone else's PR on GitHub
- leaving inline review comments
- opening, labeling, assigning, and closing issues
- triage and bug report templates

Separate "pre-commit review of my changes" from "PR review of someone else's changes" even though both are review workflows.

## 5. Practical verification pattern

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

## Verification

- `gh auth status` or equivalent token/SSH check succeeds.
- Repo/remote operations affect the intended repository.
- PR or issue actions appear in GitHub exactly where expected.
- Actions verification cites the exact run URL and head SHA.
- Review comments land on the intended lines.
