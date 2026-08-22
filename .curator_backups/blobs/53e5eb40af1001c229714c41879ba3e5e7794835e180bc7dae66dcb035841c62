# vcpkg release-only host-triplet pattern

Session takeaway for rootless Podman / compose builds that use an overlay triplet:

- If `vcpkg install` still lists large debug host packages, set `VCPKG_DEFAULT_HOST_TRIPLET` to the same overlay triplet used for `--triplet`.
- Mark the overlay triplet as release-only with `set(VCPKG_BUILD_TYPE release)` so vcpkg does not build debug variants for that triplet.
- Re-run the exact same container build and check the install plan before changing source code.

Why it matters:
- This can remove the extra debug host package set that keeps protobuf/libtorch builds alive too long on constrained builders.
- The first verification signal is the package count dropping and the host-debug packages disappearing from the printed install plan.
