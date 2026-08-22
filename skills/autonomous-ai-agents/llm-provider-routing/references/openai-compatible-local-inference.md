# OpenAI-Compatible Local Inference (absorbed note)

Preserved details from the former `openai-compatible-local-inference` skill.

## Core principle
Separate the public client contract from the backend serving contract:
- Public aliases are what clients use (`local-mlx`, `fast`, `quality`, `default`).
- Backend model ids are what the serving backend accepts (`models/local-mlx`, an artifact path, a Hugging Face id, a GGUF path, or a backend-specific id).
- A proxy mapping is correct only if it preserves the public alias externally while forwarding an id/path the target server actually accepts.

## Debugging workflow
1. Capture client, proxy, and backend errors.
2. Query backend `/v1/models` and proxy `/v1/models` separately.
3. Send tiny direct and proxied chat/completion requests.
4. Compare model id/path at each boundary.
5. Patch source-of-truth config defaults plus generated runtime config/tests where the repo expects them.
6. Restart only the config-consuming component unless the backend config changed too.

## Failure interpretation
- Direct backend succeeds with artifact path but proxy fails with alias -> mapping is wrong.
- Logs show local alias treated as a Hugging Face repo -> backend received alias instead of local id/path.
- Proxy lists alias but calls return “no deployments available” -> check whether prior 404/5xx put deployment into cooldown.

## Pitfalls
- Do not assume `/v1/models` ids are interchangeable between proxy and backend.
- Do not interpret proxy 429 cooldown as root cause before checking earlier backend 404/5xx.
- Do not claim model health from `/v1/models`; verify one tiny generation request.
