# Low-stakes Hermes routing with OpenCode free models

Session-derived notes for using OpenCode free models on Hermes auxiliary paths.

## Recommended scope
- Use OpenCode free models for low-stakes auxiliary work first, especially context compression.
- Keep primary chat, approval, and other high-stakes Hermes paths on their existing providers unless a separate backlog item changes that.

## Model selection pattern
- Refresh the current free shortlist with `opencode models opencode` before pinning anything.
- Prefer a direct `provider/model` pin over a generic router choice when you need a stable default.
- The session-observed free default was `opencode/deepseek-v4-flash-free`.

## Pinning location
- Persist the model in `~/.config/opencode/opencode.jsonc` with a root-level `"model": "provider/model"` entry.
- Use `opencode debug config` after editing the file to confirm the pin took effect.

## Smoke test
- `opencode run 'Respond with exactly: OPENCODE_SMOKE_OK'`
- This is a good verification after login or after changing the pinned free model.

## Fallback guidance
- If the free shortlist changes, re-run the shortlist refresh before updating Hermes routing.
- If OpenCode auth is not available, keep Hermes compression on its existing path instead of silently repointing higher-stakes model usage.
