# Time-series / spectral-analysis backlog intake notes

Use this when a backlog request asks for analysis of time-series tables, Fourier/spectral methods, or derived analytical tables.

## Intake shape
- Name the canonical source tables explicitly.
- Separate primary data from derived tables by lineage.
- Record the sampling interval, windowing, and any resampling or alignment step.
- State whether analysis is on raw values, returns, normalized series, or aggregated windows.
- Include one negative-control case that should fail or mislead under naive spectral use.
- Require a reproducible report, query, or notebook as closeout evidence.

## Good execution criteria
- Inventory source and derived tables and confirm freshness / sparsity / timestamp regularity.
- Define preprocessing before any transform is run.
- Compare results across representative symbols and multiple windows, not just one cherry-picked slice.
- Capture at least one counterexample where the method is inappropriate or unstable.
- Record which downstream tables or analyses would consume the derived spectral features, if any.

## Good closeout criteria
- Another reviewer can rerun the analysis from the documented queries or notebook.
- The report lists the lineage and preprocessing rules table by table.
- The recommendation is explicit about where the method is useful, where it is not, and why.
- The evidence includes a repeatable rerun with the same dominant conclusion.

## Pitfalls
- Treating derived tables as independent signals before tracing lineage.
- Skipping irregular-sampling / sparsity checks and then overclaiming frequency structure.
- Writing a recommendation that is only exploratory and has no falsifiable closeout evidence.
