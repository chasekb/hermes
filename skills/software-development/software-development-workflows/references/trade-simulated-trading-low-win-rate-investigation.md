# Trade simulated-trading low win rate investigation

Use this pattern when the Simulated Trading tab shows a low win rate and the question is whether the issue is model quality, strategy execution, or broken reporting.

## Investigation order
1. Verify the metric path first: raw trades -> backend stats -> frontend normalization -> rendered widgets.
2. Measure model calibration next: compare predicted win probability / expected return against realized outcomes.
3. Audit execution logic: thresholds, hold/exit rules, flip rate, fees, and fallback behavior.
4. Add a deterministic regression harness once the root cause class is known.

## Evidence sources to inspect
- Frontend local simulated trading path: `frontend/lib/api.ts`
- Frontend normalization: `frontend/lib/simulatedTradingStats.ts`
- Backend signal generation and persistence: `src/trading/SimulatedTradingService.cpp`
- Backend stats calculation: `src/trading/TradingStatsService.cpp`
- ML prediction endpoint and fallback behavior: `src/api/PredictController.cpp`

## Recommended backlog item template
Each recommendation should be a single root-cause class with its own:
- problem statement
- execution checklist
- closeout checklist
- verification command or evidence artifact

## Execution checklist template
- [ ] Reproduce the issue on a fixed session or fixture.
- [ ] Trace the data path to the exact rendered value or trade rule.
- [ ] Compare the raw source data with the normalized/rendered output.
- [ ] Record whether the observed behavior points to model quality, execution logic, or reporting.

## Closeout checklist template
- [ ] The root-cause class is identified and documented.
- [ ] The issue is reproduced by a deterministic fixture or sample session.
- [ ] The fix or follow-up backlog item is scoped to the correct layer.
- [ ] A regression test or durable evidence note exists.

## Diagnostic split for low win rate
When the win rate is unexpectedly low, separate the work into four questions:
- Is the win-rate metric computed from the right trade set?
- Are the model predictions actually weak or miscalibrated?
- Is the strategy execution logic causing churn, premature exits, or fee drag?
- Is the UI/reporting path misrepresenting the underlying trades?

## Session lesson
For this repo, the most useful backlog recommendations were written as four items:
- metric/data-path verification
- model calibration check
- execution logic audit
- deterministic regression harness

Each item had explicit execution and closeout criteria so the next agent could prove whether the issue was model quality or application behavior.
