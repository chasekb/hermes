# Trade stat denominator alignment

Use this pattern when a trade dashboard metric looks wrong and the question is whether the bug lives in model quality, execution logic, or reporting.

## Key lesson
Win rate must be defined over completed outcomes, not over every row in a mixed trade history.

For simulated trading in this repo:
- count winning trades and losing trades in the denominator
- do not let open-leg or zero-P&L rows dilute the win-rate calculation
- keep backend stats and frontend normalization on the same trade population

## Practical checks
1. Compare raw trade rows with the backend stats calculation.
2. Compare backend stats with frontend normalization/derivation.
3. Add a fixture that includes:
   - one winning close
   - one losing close
   - one open or neutral leg
4. Assert all layers agree on:
   - total trades
   - winning trades
   - losing trades
   - win rate
   - total fees / volume

## Good regression shape
Create both sides of the guardrail when the bug spans layers:
- backend unit test for the stats calculator
- frontend test for the normalization helper

## Failure smell
If the UI win rate changes when an open leg is added but the closed-trade outcomes do not change, the denominator is wrong somewhere in the path.