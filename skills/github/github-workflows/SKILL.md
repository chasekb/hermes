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

This umbrella replaces narrower standalone skills for GitHub auth, repository management, pull request workflow, code review, issue triage, and push-triggered build verification.

This skill absorbs the narrower GitHub workflow skills that used to be split apart:
- GitHub auth setup
- Repository creation, fork, and remote management
- Pull request lifecycle and CI monitoring
- PR / local code review
- Issue creation and triage
- Push-triggered build verification for the exact commit SHA

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

This section absorbs the former `github-actions-remote-build-verification` skill; the exact-SHA run check stays here so users do not have to look in two places.

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

When a workflow looks “mostly done” but the run is still `in_progress`, keep polling the exact run instead of assuming success from partial job completion. In Docker matrices, frontend and manifest/publish jobs may complete while backend jobs remain active for several more minutes.

For long-running push builds, avoid a blanket `cancel-in-progress: true` if a later push would routinely kill a still-valid backend build. Prefer canceling pull request runs, but let protected branch push runs finish so GitHub Actions can produce a real source-of-truth result.

Reference: `references/remote-build-monitoring.md` for the matrix-run polling checklist and safe generated-artifact cleanup notes, `references/remote-build-verification-session-note.md` for the compact push→run→proof sequence, and `references/ci-workflow-auth.md` for workflow-file push auth scope and SSH fallback notes.

If you need to keep waiting without blocking the turn, use a background `gh run watch <run_id> --exit-status` watcher and then confirm the final state with `gh run view <run_id> --json status,conclusion,headSha,url,name,updatedAt` before reporting success. If `gh run watch` times out, keep polling the exact run id with `gh run view` until GitHub returns a final conclusion; the timeout itself is not proof of failure.

Important nuance from a live run: `gh run watch` is a convenience for monitoring, not proof. The proof is the exact run object for the pushed SHA. If a sibling PR run exists on the same commit, do not use it as evidence for the push run.

If duplicate runs on the same SHA are clogging the queue, it can be appropriate to cancel only the stale duplicates that are blocking the intended verification path, then continue tracking the push run by id until GitHub marks it complete.

Reference: `references/remote-build-monitoring.md` for the matrix-run polling checklist and safe generated-artifact cleanup notes. See also `references/remote-build-monitoring-session-notes.md` for session-derived reminders about exact-SHA verification and duplicate-run triage.

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
- When a workflow edit only changes `.github/workflows/*`, re-check GitHub auth scope and be ready to push over SSH if the HTTPS token lacks workflow-file permissions.
- For long-running backend Docker matrices, do not blanket-cancel branch pushes; cancel PR reruns only and let push builds finish so the real source-of-truth run can complete.
- If a frontend Docker build succeeds in the builder stage but fails while copying `.next/standalone` into the runner image with a `BlobNotFound`/missing blob error from `productionresultssa*.blob.core.windows.net`, treat it as a flaky GitHub Actions cache artifact failure. Disable the `gha` cache path or rerun without cache before chasing app-code changes.
- When the workspace has generated caches or local state files, inspect `git status` before staging and commit only the files that are meant to be tracked; do not let incidental cache churn ride along with a docs/code change.

## Reference files

- `references/ci-workflow-auth-and-long-runs.md` — workflow-file auth scope and safe long-run CI cancellation notes.
- `references/docker-build-cache-blob-failure.md` — BuildKit cache-blob failure pattern and cache-free workaround for frontend image builds.

## Verification

- `gh auth status` or equivalent token/SSH check succeeds.
- Repo/remote operations affect the intended repository.
- PR or issue actions appear in GitHub exactly where expected.
- Actions verification cites the exact run URL and head SHA.
- Review comments land on the intended lines.
