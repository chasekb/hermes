# React / TypeScript shared-shape debugging

Use this note when a React/TypeScript build fails because several sibling components or hooks share the same config/state object.

## Pattern
- Start at the failing type error, then trace the prop/hook type back to the state owner.
- Fix the shared shape in every consumer that depends on it:
  - parent state type
  - child prop type
  - hook return type / parameter type
- Prefer narrow coercion helpers for render values (`getConfigValue`, `Number(...)`, boolean guards) instead of widening the whole config bag to `any`.
- When a fallback object is only partially structured, cast it to the exact partial shape at the boundary instead of threading `unknown` through the tree.
- After one component is fixed, rerun the build; TypeScript often surfaces the next sibling seam immediately.

## Common React lint pitfalls seen in this repo
- Avoid `Date.now()` or other impure fallbacks in render paths.
- Avoid calling `setState` synchronously inside `useEffect`; move the synchronization into event handlers or derived values when possible.
- If an effect only applies a preset or syncs local state from a prop, consider deriving the value directly or using a guarded callback instead.

## Verification
- Re-run the full production build, not just a single file check.
- If the build passes but lint still reports warnings, clean the warnings only if they affect the touched surface.
