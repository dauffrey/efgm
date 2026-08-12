# EFGM-EXP-0004 Development Cases

These 12 synthetic case specifications are visible to the research/tuning loop and are intentionally EFGM-aware.

They test:

- six configured candidate prerequisite paths with complete sparse collapse (`0.00`);
- three low non-prerequisite observations that must not become prerequisite breaches;
- three prerequisite-path observations just above the candidate threshold (`0.45`) to expose threshold sensitivity.

The executable source of the case specifications is `efgm.exp0004_sparse_governance`. `cases.json` is a reviewable materialization and is checked against the runner source in tests.

These cases are **not holdout evidence** and must not be used to claim generalization.
