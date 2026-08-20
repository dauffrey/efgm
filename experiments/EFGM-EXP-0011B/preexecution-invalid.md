# EFGM-EXP-0011B — Pre-execution holdout validity failure

Status: **PRE-EXECUTION INVALID — SCIENTIFIC EVALUATION NOT AUTHORIZED**

## What happened

The frozen EXP-0011B preregistration required a superseding fresh deterministic holdout using scenario seeds `120001..120288`, exactly 288 scenarios, 24 steps per scenario, checkpoints 6/12/18, the carried-forward EXP-0011 generator/terminal-label family, and a minority terminal class of at least 15%.

The implementation generated that holdout without computing or exposing any scientific AUC/comparator results.

The resulting dataset identity and class balance are:

- scenario count: `288`
- observation count: `864`
- aligned terminal class: `37`
- misaligned terminal class: `251`
- minority-class fraction: `0.1284722222222222`
- required minimum: `0.15`
- canonical dataset SHA-256: `7e4e481f4ab234c6b0ce3eddfe193bae3714542483a89ad2d26ab508e4e75b3c`

Therefore the preregistered validity gate failed before scientific scoring.

## Classification boundary

This is **not** `FALSIFIED`, is not `SURVIVED`, and is not an EXP-0011B scientific result. The preregistration explicitly states that failure of a validity criterion yields `PRE-EXECUTION INVALID`, and that scientific evaluation may occur only after a valid fresh dataset has been frozen.

No ROC-AUC, aggregation-scheme ranking, coupling-value diagnostic, early-detection diagnostic, SURVIVED/FALSIFIED classification, or other scientific comparator output was executed or interpreted for this holdout.

## Custody decision

The seed interval, generator, terminal label rule, 15% validity threshold, checkpoints, aggregation schemes, coefficients, ranking rule, and success criteria are not changed after observing the class balance.

Per the frozen contract, execution stops here. Any successor design must be explicitly preregistered as a new superseding prospective holdout before its dataset is generated.

## Reproducibility boundary

The invalid-result record is bound to the deterministic generator output above. CI must reproduce the exact class counts, minority fraction, dataset dimensions, and canonical dataset SHA-256 while continuing to assert that `scientific_scoring_exposed` is `false`.
