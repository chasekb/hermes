# All-by-default pagination refactors

Use this pattern when changing a collector/API from a capped default to an unbounded default.

## When to apply
- A function currently defaults to a top-N or capped page count.
- The product requirement changes to "fetch all available" by default.
- Existing call sites should stop passing a magic cap and rely on the default.

## Recommended checks
1. Identify all call sites that pass the old cap explicitly.
2. Update the API signature/comment so the default sentinel is documented clearly.
3. Preserve explicit positive-count behavior for backwards compatibility.
4. Update logging so default-all and explicit-top-N modes are distinguishable.
5. Rewrite the test from "returns the first page/capped subset" to "returns every page until exhaustion".
6. Validate the integration path, not just the leaf client, so downstream managers inherit the new default.

## Good test shape
- Build synthetic pagination with more than the old cap.
- Make each page deterministic and distinct.
- Assert total item count, first item, and last item.
- Add a downstream integration assertion that the manager/aggregator includes the new items.

## Pitfalls
- Don't leave a stale explicit cap at the integration layer; it masks the API change.
- Don't only test the leaf client; downstream code may still hard-code the old limit.
- Don't rename the test to something vague; make the new behavior obvious in the name.
- If the production code uses a sentinel value for "all", document it in the public header/API contract.
