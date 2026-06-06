# Footer surfaces in Hermes

Hermes has at least two different "footer" concepts, and user requests can refer to either one:

1. Gateway runtime footer on final replies
   - Toggled by `/footer [on|off]`.
   - This is delivery-facing metadata appended to assistant replies in gateway contexts.

2. TUI status/footer chrome
   - Implemented in `ui-tui/src/components/appChrome.tsx` and related status-bar code.
   - This is the on-screen status line in the CLI/TUI, where duration, usage, cost, model, cwd, and other live indicators can be shown or hidden by width.

When a user asks to add fields like timestamp, query runtime, or token usage to the footer:
- First confirm which surface they mean if the wording is ambiguous.
- If they mean the TUI status line, inspect the status-rule rendering and the available session/usage fields before changing layout.
- If they mean the gateway footer, keep the change isolated to that output path so it does not affect the TUI chrome.

Current session metadata already exposes token-related usage fields via `types.ts` (`Usage`), and the status chrome already has duration/usage-aware segment logic. The common pitfall is assuming "footer" means one shared renderer when Hermes actually has more than one.