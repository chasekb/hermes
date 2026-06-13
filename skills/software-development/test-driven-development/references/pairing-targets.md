# Pairing targets and sibling pipeline modes

Use this pattern when a feature adds a new sibling target, repeated table pair, or an execution mode that should stay in lockstep with an existing loop.

## Pattern
1. Extract the target list or mode selection into a small helper.
2. Write a test that asserts the helper returns the exact ordered set you expect.
3. Add a second test for the new sibling path, especially if it changes ordering, timing, or persistence.
4. Wire the helper into the production loop only after the helper test is green.
5. Keep the helper the single source of truth so future modes don't drift apart.

## Good fit examples
- Adding `--run=all-snapshot` next to `--run=both`
- Adding a new metrics sink alongside an existing per-symbol write path
- Adding a new table pair that should be processed together

## Common pitfall
If you patch the main loop first, it becomes easy to miss the sibling mode in tests. Test the helper before the loop, then reuse it from every execution branch.
