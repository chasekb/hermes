---
name: kanban-remote-ci-verification
description: "Use for Kanban tasks requiring remote-only CI build proof."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [kanban, remote-ci, github-actions, builds, exact-sha, worktrees]
    related_skills: [kanban-orchestrator, kanban-board-worktree-integration, github-workflows]
    created_by: agent
---

# Kanban Remote CI Verification

Use this class-level workflow when Kanban work must not build locally. The task property is durable: new tasks default to remote-only build verification, workers receive the policy in their task context, and a local build is allowed only through an explicit user-authorized override.

## Task policy

1. Treat `remote_ci_required=true` as the default for every task, including child tasks and legacy tasks migrated into the current schema.
2. Do not run local package, application, or container builds when the property is enabled. Reading manifests, inspecting diffs, and static reasoning are allowed; the build proof comes from GitHub Actions.
3. If the task changes a repository, commit and push the changes before claiming completion.
4. Identify the Actions run created for the pushed ref and verify its `headSha` exactly matches the pushed commit.
5. Wait for the relevant build/package job and all required verification jobs to reach a terminal state. Do not infer success from partial logs or a watcher timeout.
6. Record the exact run URL, head SHA, job names, and final conclusions in the task completion evidence.
7. Use a local-build override only when the user explicitly authorizes it; preserve the override in task metadata so the exception is visible.

## Root repository plus nested runtime repository

Some Hermes homes track configuration, skills, boards, and state in the root repository while the executable runtime source is an ignored nested `hermes-agent/` checkout. Treat them as separate repositories:

- Commit and push root-level changes to the Hermes home repository.
- Commit and push runtime code/tests to the nested source repository.
- Never claim that root CI proves nested runtime changes.
- Check each repository's own branch, remote, commit SHA, workflow files, and Actions run.
- If the nested upstream rejects the user's credentials, use a writable fork and a PR or fork-main branch. Do not force-push or modify an unrelated upstream branch.

## Remote build selection

Use the repository's supported build path rather than assuming Python packaging semantics:

- Inspect `pyproject.toml`, `setup.py`, `uv.lock`, and existing workflows first.
- Hermes intentionally rejects wheel/sdist builds; `python -m build --wheel` is not valid proof for the Hermes runtime.
- For Hermes runtime verification, use the pinned workflow-compatible command such as `uv sync --locked --python 3.11 --extra dev`, followed by the focused policy tests or the repository's normal CI test lane.
- Keep package/environment build failures separate from policy-test failures. Diagnose the first failing job from its own log before changing code.

## Exact-SHA verification sequence

```text
inspect repository and workflow metadata
→ commit the requested repository changes
→ push the exact commit
→ locate the run by branch/ref
→ verify run.headSha == pushed SHA
→ wait for completion
→ inspect every relevant build/test job
→ report URL, SHA, and conclusions
```

Preferred commands:

```bash
git rev-parse HEAD
git push -u origin <branch>
gh run list --repo <owner>/<repo> --branch <branch> --limit 10
gh run view <run-id> --repo <owner>/<repo> \
  --json status,conclusion,headSha,url,name,jobs
```

A `gh run watch` timeout is not proof of failure; poll `gh run view` until the exact run is completed. Conversely, a successful older run or an integrity-only job is not build proof for a newer SHA.

## Verification checklist

- [ ] Every task has remote-CI-required metadata unless explicitly overridden.
- [ ] No local build was run under the required policy.
- [ ] All changed repositories were committed and pushed.
- [ ] The selected Actions run URL is for the intended repository/ref.
- [ ] The run head SHA exactly equals the pushed commit SHA.
- [ ] The package/environment build job succeeded.
- [ ] Focused policy tests and required CI checks succeeded.
- [ ] Any warnings, skipped jobs, or unavailable upstream permissions are reported separately from success.

## Pitfalls

- Do not use the root repository's successful CI run as proof for ignored nested runtime code.
- Do not invent a wheel build for a project whose setup explicitly rejects it.
- Do not treat `25 values for 24 columns` or similar schema errors as CI infrastructure failures; read the failed job log and correct the SQL/schema mismatch.
- Do not convert existing running scratch tasks in place merely to apply a new policy; apply the default to new tasks and migrate metadata safely.
- Do not silently turn a failed push to an upstream repository into a claim of success; switch to an authorized fork or stop and report the permission boundary.

## Related references

- `references/remote-ci-kanban-session.md` — condensed session-derived details for the Hermes nested-repository and remote-build workflow.
