# Rootless Podman + vcpkg host-triplet failures

Use this when a rootless Podman build gets deep into vcpkg installation and the failure appears in host-side debug packages (for example protobuf) rather than your target code.

Signals
- vcpkg install list includes both target triplet and host/debug host packages.
- Build advances far past dependency resolution, then fails in a host dependency package.
- The rendered compose may still be building host tools even if the target triplet is custom.

Checks
1. Confirm the rendered build args and triplets, not just the Dockerfile intent.
2. If the host triplet is still the default (often x64-linux), set VCPKG_DEFAULT_HOST_TRIPLET to the same custom triplet as the target when the build only needs release host tools.
3. For overlay triplets that are intended to be release-only, add VCPKG_BUILD_TYPE release to the triplet file so debug host packages stop getting built.
4. Keep VCPKG_MAX_CONCURRENCY low under rootless Podman if the build is resource-sensitive.

Verification
- Re-run the build and inspect the vcpkg install list; the debug host package set should disappear or shrink materially.
- If the previous failure package is gone from the install plan, the triplet alignment is likely correct.

Related: see references/rootless-podman-compose-triage.md and references/rootless-podman-vcpkg-protobuf.md.
