# Rootless Podman + vcpkg concurrency workaround

This note captures a build-stabilization pattern observed in a rootless Podman environment where a C++ image build was failing inside vcpkg/protobuf.

## Symptom

- The compose run reached the C++ backend build stage, then failed during a heavy vcpkg/protobuf build.
- The failure was not a source-code bug; the build was simply too aggressive for the constrained rootless Podman VM.

## Workaround

- Lower `VCPKG_MAX_CONCURRENCY` before changing source or dependency versions.
- In this case, reducing concurrency from 4 to 2 was enough to let the protobuf/vcpkg step progress.

## Verification

- Re-run the exact same `podman-compose up --no-build` command after the change.
- Confirm the log advances past the prior protobuf/vcpkg failure point.
- If the workflow is mirrored in CI, keep monitoring the GitHub Actions run until the full workflow completes; do not infer success from a partially green matrix.

## Notes

- Treat this as a resource-pressure workaround, not a universal fix.
- If the same failure returns under different hardware or runner limits, re-evaluate the concurrency setting rather than assuming the application is broken.
