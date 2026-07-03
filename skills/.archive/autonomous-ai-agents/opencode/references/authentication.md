# OpenCode authentication notes

Session-derived notes for OpenCode CLI usage inside Hermes.

## Credential model
- `opencode providers list` shows all configured credentials.
- A configured OpenRouter credential does not imply OpenCode-specific auth.
- The provider id `opencode` is the OpenCode-specific credential path.
- `opencode.jsonc` can pin the default model with a root-level `"model": "provider/model"` entry.
- For the current free default, use `opencode/deepseek-v4-flash-free`.

## Login flow
- `opencode providers login --provider opencode` prompts for an API key.
- The CLI points to `https://opencode.ai/auth` during that flow.
- The flow can hand off to GitHub or Google in a browser before returning to the CLI.
- The flow is interactive; run it with a PTY.

## Model pinning
- `opencode models opencode` surfaces the current free models.
- To make the free choice sticky, set `model: "provider/model"` in `~/.config/opencode/opencode.jsonc`.
- Re-run `opencode debug config` after editing the file to confirm the pinned model took effect.

## Smoke test
- `opencode run 'Respond with exactly: OPENCODE_SMOKE_OK'`
- This is a good first verification after login or model/provider changes.

## Operational notes
- Use `opencode providers list` before and after login to confirm state.
- Prefer `opencode run` for simple, bounded tasks.
- Use the interactive TUI only when the task needs iterative back-and-forth.
