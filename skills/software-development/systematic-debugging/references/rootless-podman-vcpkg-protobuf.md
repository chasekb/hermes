# Rootless Podman + vcpkg protobuf build failures

When a container build under rootless Podman fails deep inside vcpkg while compiling protobuf, the first symptom may be a generic `BUILD_FAILED` after multiple retries. In the trade repo this surfaced while building `protobuf:x64-linux` during `podman-compose build`.

Observed pattern:
- build runs far into the vcpkg graph
- protobuf fails in the `cmake --build . --target install` step
- vcpkg retries the install a few times, then exits `BUILD_FAILED`
- host had limited RAM in the rootless VM, and vcpkg was effectively running with high parallelism (`-j9` in the log)

Practical mitigation:
- cap vcpkg concurrency before the install step, e.g. `export VCPKG_MAX_CONCURRENCY=1` as the safe default in rootless Podman VMs
- keep the existing retry loop; the concurrency cap is the meaningful change
- if the failure persists, read the package-specific log under `/opt/vcpkg/buildtrees/<pkg>/install-*-out.log` before touching application code
- if you were previously using a smaller cap like 2 and protobuf still failed, drop to 1 before editing app code or the package recipe

Why this belongs here:
- it is a debugging pattern, not a repo-specific one-off
- it applies to other memory-hungry vcpkg packages on rootless Podman VMs, not just protobuf
