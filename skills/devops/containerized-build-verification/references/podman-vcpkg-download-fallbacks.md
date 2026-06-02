# Podman + vcpkg download fallbacks

Use this when a rootless Podman build fails inside vcpkg on a specific port download or archive fetch.

What to check first
- Identify the first port that fails, not the last package in the dependency list.
- Read the exact URL vcpkg tried to fetch.
- Verify whether the source is GitHub-hosted, GitLab-hosted, or another upstream archive.

Practical fallbacks
- Prefer codeload.github.com for GitHub archive URLs when the normal `github.com/.../archive/*.tar.gz` path is flaky in containerized builds.
- If the port is pinned to a specific commit/tag and the archive URL is stable, pre-seed the matching tarball into vcpkg's downloads cache before the manifest install.
- Always verify the cached tarball against the port's expected SHA512 before relying on it.
- If a portfile uses an alternate mirror or hosting provider and that fallback is known-good for the pinned version, keep the mirror patch in the image/build recipe so the build remains deterministic.

Verification pattern
1. Re-run the build once after applying the smallest download-path fix.
2. Confirm the failing port now reports a successful download or extraction.
3. Keep any cache seeding narrowly scoped to the exact pinned archive used by the port.

Notes
- This is a build/download workaround pattern, not a general rule to bypass integrity checks.
- Do not widen the cache seed beyond the exact pinned artifact unless the port version changes.
