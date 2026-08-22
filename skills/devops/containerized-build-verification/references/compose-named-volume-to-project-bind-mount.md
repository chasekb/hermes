# Compose named volume to project-local bind mount

Use this note when a repo asks to make container volumes live inside the project directory rather than Docker/Podman-managed named volumes.

## Pattern

1. Inspect all compose files and docs for the named volume and mount target.
   - Search for `volumes:`, the named volume key, and the container target path.
   - Check README/ops docs for backup/restore commands that still reference the named volume.

2. Convert only the intended persistent service volume.
   - Example: replace `qdrant-storage:/qdrant/storage` with `./data/qdrant:/qdrant/storage`.
   - Remove the now-unused top-level named-volume declaration.
   - Preserve existing bind mounts like `./logs`, `./config`, and read-only model mounts unless the user asked for a broader rewrite.

3. Protect the project-local runtime data from git.
   - Add the specific runtime path to `.gitignore`, e.g. `data/qdrant/`.
   - Do not ignore a broad `data/` directory without checking whether the repo tracks source/model artifacts there.

4. Update operational docs.
   - Backup commands should mount the project directory path, preferably read-only for backup: `-v "$PWD/data/qdrant":/source:ro`.
   - Restore commands should target the bind mount path: `-v "$PWD/data/qdrant":/target`.
   - If examples include database connection environment variables, use placeholders such as `<password>` rather than copying live credentials into docs.

5. Verify without deleting or migrating data unless explicitly asked.
   - Create or verify the bind-mount directory with `mkdir -p data/qdrant`.
   - Render compose config and confirm it resolves to `type: bind`, source under the project root, and the original target path.
   - Confirm the path is gitignored with `git check-ignore -v data/qdrant/`.

## Pitfalls

- Do not remove an existing named Docker/Podman volume or copy data from it unless the user explicitly asks for migration. Data movement/destruction needs separate approval.
- Do not treat generated runtime state as a build artifact during cleanup.
- If docs mention both Docker and Podman, update the storage examples in provider-neutral terms unless the command syntax is provider-specific.
