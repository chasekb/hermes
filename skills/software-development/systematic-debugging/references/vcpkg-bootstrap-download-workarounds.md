# vcpkg bootstrap and GitHub archive download workarounds

Use this when a rootless Podman build gets deep into vcpkg and then fails while bootstrapping a toolchain dependency or downloading source archives.

Observed pattern in the trade repo
- `podman-compose build` runs far into the vcpkg dependency graph.
- A package build fails after retries with a generic `BUILD_FAILED` or a download/bootstrap-related error.
- The failure is often not the application code itself; it is the build image’s toolchain or archive-fetch path.

Practical fixes that worked here
- Preinstall the exact CMake version expected by the build image instead of letting vcpkg bootstrap its own copy.
- For GitHub source archives, prefer `codeload.github.com` first and keep `github.com/archive` as a fallback.
- Keep any already-working mirror or preseeded archive workarounds in place (for example, cpuinfo/LMDB mirrors) so the new fix does not regress earlier success paths.

Why this matters
- It turns a flaky network/bootstrap path into a deterministic image-level dependency.
- It avoids repeated vcpkg retries that waste time and obscure the real cause.

Verification
- Re-run the same `TAG=dev podman-compose build` after the image/toolchain change.
- Confirm the build proceeds past the previous bootstrap/download step instead of failing on the same archive fetch.
