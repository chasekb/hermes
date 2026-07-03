---
name: github-remote-build-verification
description: Verify push-triggered GitHub Actions builds as the source of truth for branch completion, including matching the workflow run to the pushed commit SHA.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [GitHub, Actions, CI, verification, release]
---

# GitHub Remote Build Verification

Use this skill when the user wants a push-triggered GitHub Actions run to be the source of truth for completion, release readiness, or branch closeout.

## Trigger conditions

- The user asks to commit and push so a remote build runs.
- The user says GitHub Actions is the source of truth.
- The user asks for build verification completed successfully.
- A branch/worktree task should not be considered done until CI proves the pushed commit.

## Core workflow

1. Commit the changes locally.
2. Push the branch to trigger GitHub Actions.
3. Record the pushed commit SHA immediately after push.
4. Use `gh run list --branch <branch>` to locate the push-triggered run.
5. Use `gh run view <run_id> --json status,conclusion,headSha,url,name,createdAt,updatedAt` for final proof.
6. Treat the build as verified only if:
   - `status` is `completed`
   - `conclusion` is `success`
   - `headSha` exactly matches the pushed commit SHA
   - the workflow run URL is from the push you just made

See `references/remote-build-monitoring.md` for the exact command flow and how to avoid mistaking an in-progress or unrelated run for the pushed commit’s proof.

## What to report back

Always include:
- commit SHA
- workflow run URL
- run status and conclusion
- whether the run was triggered by the pushed SHA

If the user asked for completion proof, the final answer should cite the exact GitHub Actions run URL and the verified head SHA.

## Recommended commands

```bash
git commit -m "<message>"
git push origin <branch>
git rev-parse HEAD
gh run list --branch <branch> --limit 10
```

For final proof:

```bash
gh run view <run_id> --json status,conclusion,headSha,url,name
```

## Pitfalls

- `gh run watch` is useful for live progress, but do not use it as final proof if it exits early or loses annotations.
- Do not trust a successful run on the same branch unless its `headSha` matches the pushed commit SHA.
- If several runs exist on the branch, only the push-triggered run for the exact commit counts.
- Do not infer success from local tests when the user asked for GitHub Actions proof.

## Relation to branch-finishing workflows

This skill complements branch-finish workflows:
- finish the code change
- push it
- verify the GitHub Actions run
- then close out backlog or branch status

## Verification checklist

- [ ] Branch pushed
- [ ] Commit SHA recorded
- [ ] GitHub Actions run located
- [ ] Run status is completed
- [ ] Run conclusion is success
- [ ] Run head SHA matches the pushed commit
- [ ] Run URL saved for reporting
