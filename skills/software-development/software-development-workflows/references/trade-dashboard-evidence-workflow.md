# Trade Dashboard Evidence Workflow

This reference captures the reusable workflow discovered while turning the trade dashboard verification work into backlog items.

## When to use
- You need to verify a live dashboard tab with real UI evidence before drafting backlog items.
- The task is to create one recommendation per calculation or per widget.
- The final backlog items need execution and closeout criteria that match the observed UI.

## Reusable workflow
1. Open the dashboard tab in a real browser session.
2. Exercise the frontend or API path long enough to populate the relevant widgets.
3. Capture the live values from the DOM, including table rows for widgets that render lists.
4. Write a short evidence note/report with:
   - the reproduction path
   - the observed values
   - the visible widget/table rows
   - any fallback or activation path needed to make the data appear
5. Split backlog recommendations so each one targets exactly one calculation or one widget.
6. For each recommendation, include:
   - a title that names the calculation/widget
   - a summary that states the test intent
   - execution criteria that describe the input shape, formula, or normalization boundary
   - closeout criteria that describe the expected passing state
   - a link to the evidence note/report

## Checklist template
- [ ] Open the live dashboard tab
- [ ] Produce enough activity to populate the target widgets
- [ ] Capture the observed values from the DOM or API payload
- [ ] Write a durable evidence note/report
- [ ] Create one backlog recommendation per calculation/widget
- [ ] Attach execution criteria and closeout criteria to each item
- [ ] Link each item to the evidence report

## Session note
In the trade dashboard session, the simulated trading tab was verified by letting the live session run until the following widgets had visible rows/values:
- simulated trading summary cards
- open positions table
- recent trades table
- order book signals table

The resulting evidence report lives at:
- `docs/reports/simulated-trading-tab-evidence-2026-06-21.md`
