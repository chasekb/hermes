# CI workflow auth and long-run build notes

Session takeaways:

## Workflow-file push auth
- A repository may accept normal HTTPS git pushes but still reject workflow-file updates because the OAuth/token context lacks GitHub Actions workflow scope.
- If `git push` fails only after editing `.github/workflows/*`, check SSH auth and use an SSH remote push when the SSH key is already trusted.
- Verify auth with `gh auth status` and `ssh -T git@github.com` before assuming the repo is blocked.

## Long-running Docker matrix builds
- For long backend builds, avoid blanket `cancel-in-progress: true` on branch pushes.
- Prefer canceling PR reruns while letting protected-branch push builds finish, so a valid backend run is not killed by a later push.
- Verify the exact run by SHA and URL after each push: `gh run list --branch <branch>` then `gh run view <run_id> --json status,conclusion,headSha,url,updatedAt`.
- If `gh run watch` hits an API 500, fall back to polling `gh run view` until `status == completed`.
