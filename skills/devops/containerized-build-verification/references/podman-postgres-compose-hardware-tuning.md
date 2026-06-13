# Podman Postgres compose tuning on 16 GB Apple Silicon

Session note: the host was a 10-core Apple M5 with 16 GiB RAM, and the rootless Podman machine had 8 CPUs / 16 GiB memory. The compose file was tuned successfully for that footprint.

Practical adjustments that verified cleanly:
- Postgres: `shared_buffers=512MB`, `effective_cache_size=1536MB`, `maintenance_work_mem=128MB`, `max_connections=25`
- Postgres: keep `work_mem=4MB`, `wal_buffers=16MB`, `checkpoint_completion_target=0.9`, `huge_pages=off`
- Postgres healthcheck: use `CMD-SHELL` with `pg_isready -U "$POSTGRES_USER"` so it stays aligned with the container env rather than hardcoding the user
- Metabase healthcheck: probe `http://localhost:3000/api/health` inside the container, not the published host port
- Shorter healthcheck intervals/start periods make startup failures visible sooner on local dev stacks

Verification used in this session:
- `podman compose -f compose.yaml config` rendered successfully after the changes

Caution:
- These are hardware-footprint heuristics, not universal defaults. Re-evaluate if the Podman VM memory/CPU allocation changes or the database workload grows significantly.