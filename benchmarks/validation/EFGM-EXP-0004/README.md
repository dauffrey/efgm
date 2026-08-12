# EFGM-EXP-0004 Validation Cases

These 15 synthetic validation case specifications are separated from the development variants but remain internally authored and EFGM-aware.

They test:

- the same six configured candidate prerequisite paths at a near-threshold value (`0.35`);
- three different low non-prerequisite observations;
- three different configured prerequisite-path observations just above the candidate threshold (`0.45`);
- three preregistered catastrophic challenge paths **outside** the configured candidate prerequisite set.

The uncovered challenge paths are:

- `alignment.prohibited_goal_avoidance`;
- `boundary_integrity.capability_scope_adherence`;
- `control_recoverability.state_cleanup_completeness`.

Those cases are included specifically to test whether a candidate that succeeds on its configured paths still has a semantic coverage gap.

The validation split is intended to detect brittle threshold/path behavior before any promotion proposal. It is not sealed-holdout evidence.

The executable source of the case specifications is `efgm.exp0004_sparse_governance`. `cases.json` is a reviewable materialization and is checked against the runner source in tests.
