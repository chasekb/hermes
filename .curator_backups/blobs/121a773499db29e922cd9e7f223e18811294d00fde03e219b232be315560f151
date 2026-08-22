# Verified Kanban board/worktree bootstrap

For each project id, use this sequence:

1. Verify the repository path exists and is a Git repository:
   `git -C <repo> rev-parse --show-toplevel`
2. Create/reuse the board with slug and name equal to the project id.
3. Create/reuse the Hermes project with the repository as `--primary` and bind it with `--board <project>`.
4. Run `hermes project bind-board <project> <project>`.
5. Run `hermes kanban boards set-default-workdir <project> <repo>`.
6. Create new cards with `--project <project>` or `--workspace worktree`.
7. Verify with `hermes project show <project>`, `hermes kanban boards list --json`, and board stats.

The live rollout used these project/repository pairs:

- `arhida` -> `.../chasecapitalmanagement/arhida`
- `cohida` -> `.../chasecapitalmanagement/cohida`
- `db` -> `.../chasecapitalmanagement/db`
- `hermes` -> `/Users/bernardchase/.hermes`
- `market` -> `.../chasecapitalmanagement/market`
- `mlx-stack` -> `.../chasecapitalmanagement/mlx-stack`
- `trade` -> `.../chasecapitalmanagement/trade`
- `transform` -> `.../chasecapitalmanagement/transform`

When reconciling project ids, compare the canonical shared backlog export with the Hermes legacy snapshot if the request uses the `project_id` field. Preserve the union rather than silently dropping older project scopes. Closed/archived backlog items should not be recreated as active cards. Existing running or queued scratch tasks should remain untouched; apply worktree behavior to new project-linked tasks unless an explicit migration plan exists.
