# EFGM-EXP-0004 — Agent Governance critical-dimension diagnostics

## Decision

**Do not promote the current candidate prerequisite set.**

This development/validation cycle confirms that explicit non-compensatory prerequisites can expose sparse catastrophic failures that the aggregate Agent Governance classifier misses, but the current configured path set is incomplete and does not outperform the simpler aggregation-independent invariant checklist on validation. No sealed holdout was accessed.

## Frozen execution identity

- Parent merged `main`: `fd70317e4bad193c00763a398f41db6e75700b55`
- Experiment execution SHA: `8c2df53760dc8a39ac2d802127a477d107f14102`
- GitHub Actions: EFGM Check run `#93` / run ID `31430795539`
- Python: `3.12.13`
- Runner: `efgm.exp0004_sparse_governance` `0.2.0`
- Frozen EFGM v2 config: `efgm-v2.0-baseline`
- Frozen EFGM v2 config SHA-256: `0f55f6eabe97d0f365d1e45ba8f9d0fef67e9721a93e6eba8b0a364b612bafd0`
- Agent Governance candidate config: `efgm-v0.3-agent-governance-candidate-r2`
- Candidate config SHA-256: `af0b5540f28d4d65ae95929a855a168f9e7c286439d33d33e14ef167d808366c`
- Dataset version: `sparse-governance-failures-v0.3`
- Dataset SHA-256: `71b8534a2cc69e62c4375a100d85b40de1051ffbdf61bd9f035ce19728fdeb38`
- Development / validation / holdout cases: `12 / 15 / 0`
- Perturbation: `±0.10`, 200 trials per case, seed `20260810`

The experiment execution SHA is intentionally the code head that produced these metrics. The later documentation commit that records this result is not substituted for the execution SHA.

## Pre-result design hardening

Before reading the EXP-0004 output, the experiment was strengthened in two ways:

1. The invariant checklist threshold was frozen separately at `0.40` rather than being inherited from the candidate configuration. This keeps it independent of the candidate threshold, although it remains an internally authored comparator rather than an externally independent label source.
2. Three catastrophic validation challenges were added outside the configured candidate-prerequisite path set:
   - `alignment.prohibited_goal_avoidance`
   - `boundary_integrity.capability_scope_adherence`
   - `control_recoverability.state_cleanup_completeness`

These changes were committed at the execution SHA above before GitHub Actions run #93 produced the result.

## Dataset design

### Development — 12 cases

- 6 complete sparse failures (`0.00`) on configured candidate prerequisite paths;
- 3 low non-prerequisite benign controls (`0.15`);
- 3 configured prerequisite-path borderline controls (`0.45`).

### Validation — 15 cases

- 6 configured candidate prerequisite paths at `0.35`;
- 3 low non-prerequisite benign controls at `0.10`;
- 3 configured prerequisite-path borderline controls at `0.45`;
- 3 catastrophic failures at `0.00` on preregistered paths outside the configured prerequisite set.

All cases are synthetic, internally authored, and tuning-visible. They are not holdout evidence.

## Executed results

### Development

| Diagnostic | Detection | False alarms |
|---|---:|---:|
| Aggregate-only classifier | 0.00% | — |
| Configured candidate prerequisites | 100.00% | 0.00% |
| Governance observation floor | 100.00% | 50.00% |
| Governance low percentile | 0.00% | 0.00% |
| Aggregation-independent invariant checklist | 100.00% | 0.00% |

The aggregate-only false-reassurance rate was **100.00%** on the development catastrophic cases.

Interpretation:

- the candidate prerequisite layer catches the sparse failures it was configured to catch;
- the neutral observation floor also exposes all of them but over-flags half of the benign controls if naively converted into a verdict;
- the current low-percentile diagnostic does not detect these one-observation sparse failures at the tested setting;
- the simpler invariant checklist makes the same development decisions as the configured prerequisite layer.

### Validation

| Diagnostic | Detection | False alarms |
|---|---:|---:|
| Aggregate-only classifier | 0.00% | — |
| Configured candidate prerequisites | **66.67%** | **0.00%** |
| Aggregation-independent invariant checklist | **66.67%** | **0.00%** |

The aggregate-only false-reassurance rate remained **100.00%** on the validation catastrophic cases.

The three intentionally uncovered catastrophic paths were not detected by the configured prerequisite set. Therefore the candidate's validation detection rate fell from 100% on its covered development failures to **6/9 = 66.67%**.

The independent-of-aggregation checklist made the same covered-path decisions:

```text
incremental balanced accuracy vs checklist = +0.0000
```

This satisfies an explicit failure condition for promotion: the more integrated candidate prerequisite mechanism did not provide incremental validation value over the simpler comparator.

## Threshold sensitivity and path ablation

The CI test suite froze and verified the following candidate diagnostics on the complete development+validation case set:

- threshold `0.40`: detection `80.00%`, false alarms `0.00%`;
- threshold `0.30`: detection `40.00%`;
- threshold `0.50`: false alarms `50.00%`;
- removing any one configured candidate prerequisite path reduces catastrophic detection to `10/15 = 66.67%` on the combined case set.

This demonstrates that both semantic membership and threshold choice materially affect behavior. Raising the threshold can create immediate false alarms; lowering it can miss near-threshold catastrophic cases.

## Perturbation robustness

With `±0.10` perturbation and 200 trials per case:

- mean correct classification probability: **77.65%**;
- minimum case probability: **0.00%**.

The zero minimum is not random numerical instability: preregistered catastrophic validation paths outside the candidate set remain structurally undetectable by that candidate prerequisite mechanism.

## Promotion gate

```text
promotion_gate_passed = False
```

This is the correct outcome for this cycle.

The candidate prerequisite concept demonstrates value against aggregate-only false reassurance on covered paths, but the **current path set is not eligible for promotion** because:

1. semantic coverage is incomplete on preregistered validation challenges;
2. the simpler invariant checklist provides the same covered-path validation decisions;
3. there is no positive incremental balanced accuracy;
4. perturbation robustness contains structurally undetectable cases;
5. the evidence is internally authored and no sealed holdout has been used.

## What we do not do next

We do **not** append the three failed validation paths to the prerequisite list and rerun the same evaluation as though that were confirmation. That would tune the candidate directly to observed validation failures and erase the value of the counterexample.

The failed/incomplete candidate is retained as research evidence. A future candidate may propose a semantically justified broader control invariant, but it must be preregistered and evaluated against fresh cases and simpler alternatives.

## Implications for the research program

EXP-0004 strengthens three conclusions:

1. **Aggregate-only Agent Governance remains vulnerable to sparse critical failures.** Every catastrophic case in this cycle was reassuring under aggregate-only classification.
2. **Non-compensatory semantics matter, but a hand-selected prerequisite list is not enough.** The current candidate succeeds exactly where it has explicit coverage and fails outside it.
3. **Simpler comparators remain serious competitors.** The candidate prerequisite layer did not outperform the simpler aggregation-independent checklist on validation.

This result therefore supports continuing falsification rather than promoting candidate-r2 prerequisites.

## Next experiments

- **EFGM-EXP-0007:** test the analogous sparse-failure problem in canonical EFGM v2 while preserving frozen `DQ` and comparing prerequisite floors, extreme-degradation vetoes, soft-min/low-percentile diagnostics, and an independent invariant checklist.
- **EFGM-EXP-0005:** execute temporal recovery only after prerequisite semantics are further evaluated; do not let a static prerequisite list silently define complete recovery.
- **EFGM-EXP-0006:** obtain independently authored exposure/execution labels before claiming semantic validity for AE versus CUE.

## Limitations

- Cases and labels are internally authored and EFGM-aware.
- The invariant checklist is independent of EFGM aggregation but not independently labeled by an external scorer.
- The validation split is tuning-visible after this run and must not be reused as unseen evidence for a modified prerequisite path set.
- No sealed holdout was accessed.
- The result rejects promotion of the **current candidate prerequisite set**; it does not reject every possible non-compensatory governance design.
- Passing CI establishes implementation/reproducibility behavior, not scientific validity.
