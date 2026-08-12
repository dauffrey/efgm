# EFGM-EXP-0007 — Canonical EFGM v2 sparse-failure diagnostic comparison

## Decision

**Do not promote the narrow v2 prerequisite-plus-extreme-veto candidate.**

The experiment preserves frozen EFGM v2 `DQ` and compares only post-score diagnostic/classification alternatives. The current v2 aggregate classifier falsely reassured on every catastrophic development and validation case in this deliberately sparse adversarial suite. The narrow candidate repaired its covered cases but failed preregistered validation paths outside its semantic membership. A broader aggregation-independent invariant checklist performed better on validation.

No sealed holdout was accessed.

## Frozen execution identity

- Parent merged `main`: `fd70317e4bad193c00763a398f41db6e75700b55`
- Experiment execution SHA: `2b00dd9a9dbe964dc293e953937ee661de49cb3c`
- GitHub Actions: EFGM Check run `#95` / run ID `31431745557`
- Python: `3.12.13`
- Runner: `efgm.exp0007_v2_sparse_failure` `0.1.0`
- Frozen v2 config: `efgm-v2.0-baseline`
- Frozen v2 config SHA-256: `0f55f6eabe97d0f365d1e45ba8f9d0fef67e9721a93e6eba8b0a364b612bafd0`
- Dataset version: `v2-sparse-failure-controls-v0.2`
- Dataset SHA-256: `799329f4b257a44461ca1004a616dd47373e19339612332033207b7d1783ffb2`
- Development / validation / holdout cases: `16 / 20 / 0`
- Perturbation: `±0.10`, 200 trials per case, seed `20260810`
- Frozen DQ preserved: `True`

The result-record commit is intentionally separate from the execution SHA. The execution SHA above remains the identity of the code and preregistered case set that produced the reported metrics.

## Pre-result candidate definitions

### Narrow candidate

Positive prerequisite threshold: `0.40` over:

```text
flow_quality.task_completion_consistency
flow_quality.verification_success_rate
grounding.rule_support
grounding.evidence_validity
```

Extreme-degradation veto: any base observation in output, behavioral, or operational entropy `>= 0.80`.

### Observation floor + extreme maximum

- minimum of all flow-quality and grounding base observations `< 0.40`; or
- maximum output/behavioral/operational entropy base observation `>= 0.80`.

### Soft-percentile diagnostic

- 20th percentile of positive base observations `< 0.40`; or
- 90th percentile of penalty base observations `>= 0.80`.

### Aggregation-independent invariant checklist

The broader checklist uses all four flow-quality base observations plus grounding rule support, evidence validity, traceability, and factual consistency at threshold `0.40`, plus the same generic extreme-penalty rule. It is independent of EFGM aggregation/composite values, but it is **not externally independently labeled ground truth**.

### Preregistered validation challenges outside the narrow candidate

```text
flow_quality.reasoning_continuity
flow_quality.semantic_coherence
grounding.traceability
grounding.factual_consistency
```

These challenge paths were committed before execution specifically to test semantic path-set completeness.

## Dataset design

### Development — 16 cases

- 4 complete positive-control collapses on narrow candidate paths;
- 5 sparse maximal output/behavioral/operational entropy failures;
- 1 low non-critical grounding control;
- 3 positive borderline controls;
- 3 moderate single-penalty controls.

### Validation — 20 cases

- 4 narrow-candidate prerequisite paths at `0.35`;
- 4 catastrophic positive-control paths outside the narrow candidate at `0.00`;
- 4 different near-maximal penalty cases at `0.95`;
- 1 low non-critical grounding control;
- 4 positive borderline controls;
- 3 moderate penalty controls.

All case labels are internally authored and tuning-visible after this run.

## Executed results

### Development

| Diagnostic | Detection | False alarms |
|---|---:|---:|
| Frozen aggregate-only v2 classifier | 0.00% | — |
| Narrow prerequisite + extreme veto | **100.00%** | **0.00%** |
| Observation floor + extreme max | **100.00%** | **14.29%** |
| Soft-percentile diagnostic | **0.00%** | **0.00%** |
| Aggregation-independent invariant checklist | **100.00%** | **0.00%** |

The aggregate-only false-reassurance rate was **100.00%** on development catastrophes.

### Validation

| Diagnostic | Detection | False alarms |
|---|---:|---:|
| Frozen aggregate-only v2 classifier | 0.00% | — |
| Narrow prerequisite + extreme veto | **66.67%** | **0.00%** |
| Observation floor + extreme max | **100.00%** | **12.50%** |
| Soft-percentile diagnostic | **0.00%** | **0.00%** |
| Aggregation-independent invariant checklist | **100.00%** | **0.00%** |

The aggregate-only false-reassurance rate remained **100.00%** on validation catastrophes.

The narrow candidate lost coverage because four preregistered positive-control failures were outside its semantic prerequisite set. The broader invariant checklist covered those paths and all sparse extreme penalties.

```text
incremental balanced accuracy vs checklist = -0.1666
```

The narrow candidate is therefore worse than the broader checklist on this validation suite under the reported balanced-accuracy comparison.

## Diagnostic tradeoffs

The observation-floor + extreme-max alternative achieved complete catastrophic detection but introduced false alarms: **14.29%** in development and **12.50%** in validation. This supports EXP-0003's concern that indiscriminate hard extrema can overreact to benign low/high observations.

The tested soft-percentile diagnostic achieved **0%** catastrophic detection in both splits. At the preregistered percentile settings, a one-dimensional sparse failure is still diluted by neighboring observations.

The broader aggregation-independent checklist achieved **100% detection / 0% false alarms** in both splits. This is the strongest comparator in this internally authored cycle. It does not establish external validity, but it blocks promotion of the more complex narrow candidate.

## Perturbation robustness

For the narrow candidate at `±0.10`, 200 trials per case:

- mean correct classification probability: **83.15%**;
- minimum case probability: **0.00%**.

The zero minimum is structural: uncovered positive-control paths remain invisible while candidate semantic membership is unchanged.

## Promotion gate

```text
promotion_gate_passed = False
```

We do **not** add reasoning continuity, semantic coherence, traceability, and factual consistency to the candidate after observing these validation failures and rerun the same split as confirmation. That would convert validation counterexamples into tuning data.

A future broader non-compensatory candidate must be justified by a semantic invariant taxonomy before evaluation and tested against fresh cases, ablations, simpler baselines, and eventually a sealed holdout.

## What this cycle establishes

Under this specified synthetic sparse-failure suite:

1. Frozen v2 aggregate classification remains vulnerable to critical-dimension dilution.
2. The failure occurs for both positive sparse failures and extreme penalty observations while the experiment leaves frozen `DQ` unchanged.
3. A narrow hand-selected prerequisite set is incomplete even when combined with an extreme-penalty veto.
4. A naive all-observation floor/max rule improves detection but introduces false alarms.
5. The tested soft-percentile setting remains too compensatory for one-dimensional sparse failures.
6. A simpler broader invariant checklist outperformed the narrow candidate in validation.

These are scoped experimental findings, not universal claims about every EFGM v2 application.

## Next research consequences

The evidence points away from expanding prerequisite lists one observed failure at a time. Any next candidate should be specified from a semantic invariant taxonomy and evaluated on fresh cases.

For Agent Governance, EXP-0005 can proceed with temporal trajectories, but `verified_recovery` must not rely on the failed assumption that the current candidate prerequisite list is a complete definition of recovery. Candidate-prerequisite absence may remain one necessary check; residual-state evidence and a governed post-state remain independent requirements.

EXP-0006 still requires genuinely independent exposure/execution labels before AE/CUE semantic claims can be made.

## Limitations

- Cases and labels are internally authored and EFGM-aware.
- The invariant checklist is aggregation-independent but not externally independently labeled.
- The validation split is tuning-visible after this run and cannot be reused as unseen evidence for a widened path set.
- No sealed holdout was accessed.
- This result rejects the **narrow candidate**; it does not establish that the broader checklist is production-valid or that every possible non-compensatory layer will work.
- Passing CI establishes execution/reproducibility mechanics, not scientific validity.
