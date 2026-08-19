# EFGM-EXP-0011 — Pre-execution holdout validity failure

Status: **PRE-EXECUTION INVALID — SCIENTIFIC EVALUATION NOT AUTHORIZED**

## What happened

The frozen preregistration required a fresh deterministic holdout using scenario seeds `110001..110240`, exactly 240 scenarios, 24 steps per scenario, checkpoints 6/12/18, the EXP-0010 synthetic generator family and terminal A/M rule, and a minority terminal class of at least 15%.

The implementation generated that holdout without computing or exposing any scientific AUC/comparator results.

The resulting class balance was:

- scenario count: `240`
- minority-class fraction: `0.14583333333333334`
- required minimum: `0.15`
- implied minority scenarios: `35 / 240`

Therefore the preregistered validity gate failed before scientific scoring.

## Classification boundary

This is **not** `FALSIFIED` and is not an EXP-0011 scientific result. The preregistration explicitly states that failure of a validity criterion yields `INVALID`, and that scientific evaluation may occur only after a valid fresh dataset has been frozen.

No ROC-AUC, aggregation-scheme ranking, coupling-value diagnosis, early-detection diagnosis, SURVIVED/FALSIFIED classification, or other scientific comparator output was executed or interpreted for this holdout.

## Custody decision

The seed interval, generator, label rule, 15% validity threshold, checkpoints, aggregation schemes, coefficients and success criteria will not be changed on this preregistration after inspecting the class balance.

Per the frozen contract, execution stops here. Any successor design must be explicitly preregistered as a superseding prospective holdout before its dataset is generated.

## CI identity

The first implementation/preflight attempt was exercised by EFGM Check run `32211854431` on PR #23. The test suite stopped at the preregistered minority-class validity assertion, before the no-scoring manifest step could execute.
