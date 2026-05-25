# Push, rebase, and CI verification notes

Use this when a push is rejected or CI needs to be verified after a GitHub push.

## SSH push gotcha

If `git push` seems to time out over SSH, it may actually be waiting on an interactive host-key or confirmation prompt. Prefer a non-interactive push command that pre-accepts the host key:

```bash
GIT_SSH_COMMAND='ssh -o StrictHostKeyChecking=accept-new -o UserKnownHostsFile=$HOME/.ssh/known_hosts -o ConnectTimeout=20' git push origin <branch>
```

For GitHub over SSH port 443:

```bash
ssh-keyscan -p 443 ssh.github.com >> ~/.ssh/known_hosts
orig=$(git remote get-url origin)
git remote set-url origin ssh://git@ssh.github.com:443/<owner>/<repo>.git
GIT_SSH_COMMAND='ssh -o StrictHostKeyChecking=accept-new -o UserKnownHostsFile=$HOME/.ssh/known_hosts -o ConnectTimeout=20' git push origin <branch>
git remote set-url origin "$orig"
```

## If push is rejected as non-fast-forward

1. `git fetch origin`
2. `git rebase origin/<branch>`
3. Resolve conflicts, then `git rebase --continue`
4. Push again

When deleting a large subtree, rebase can surface `modify/delete` conflicts on a remaining file inside the removed tree. If the file should stay deleted, remove the leftover path (`rm` or `git rm`) and continue the rebase.

## CI verification

After the push, verify the workflow run rather than assuming the push alone was enough:

```bash
gh run list --branch <branch> --limit 5
gh run watch <run_id> --exit-status
```

If `gh` loses API connectivity, query the run again later; do not treat a transient API timeout as a failed workflow.
