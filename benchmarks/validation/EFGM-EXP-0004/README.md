# EFGM-EXP-0004 Validation Cases

These 12 synthetic validation case specifications are separated from the development variants but remain internally authored and EFGM-aware.

They test:

- the same six preregistered semantic prerequisite paths at a near-threshold value (`0.35`);
- three different low non-prerequisite observations;
- three different prerequisite-path observations just above the candidate threshold (`0.45`).

The validation split is intended to detect brittle threshold/path behavior before any promotion proposal. It is not sealed-holdout evidence.

The executable source of the case specifications is `efgm.exp0004_sparse_governance`. `cases.json` is a reviewable materialization and is checked against the runner source in tests.
