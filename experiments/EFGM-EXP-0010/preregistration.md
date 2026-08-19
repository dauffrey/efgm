# EFGM-EXP-0010 — Trajectory Coherence and Early Transition Detection

Status: PREREGISTERED — execution not yet interpreted

## Historical anchor

The preserved original EFGM expression remains unchanged:

`T × E = Et ~ F ± e = A|M`

This experiment does not claim that the notation is a conventional algebraic equation. It tests a narrower implication suggested by EFGM-EXP-0009: whether trajectory dynamics involving flow and entropy contain reproducible information about an eventual A/M transition before terminal realized flow makes the destination obvious.

## Research question

Can frozen EFGM-inspired trajectory measurements describe and detect movement toward terminal Alignment (A) versus Misalignment (M) before terminal outcome, and do they add predictive information beyond contemporaneous Flow alone?

## Why this follows EXP-0009

EFGM-EXP-0009 was valid and FALSIFIED because terminal realized Flow alone discriminated A/M better than the frozen joint static proxy. EXP-0010 therefore does not retune that proxy. It changes the scientific question from static terminal discrimination to preregistered early trajectory detection.

## Design

- deterministic, non-autonomous synthetic trajectories only;
- 240 trajectories generated from one frozen deterministic schedule;
- 24 ordered steps per trajectory;
- terminal A/M labels generated only from terminal synthetic progress and reserve;
- no EFGM score or detector participates in label generation;
- prediction checkpoints frozen at steps 6, 12, and 18 (25%, 50%, 75% of trajectory);
- terminal step 24 is used only for outcome labeling and descriptive analysis;
- all trajectory factors and labels are generated before any detector comparison is interpreted.

## Frozen measurements

At each checkpoint the experiment records only information available up to that step:

- `T`: elapsed fraction of the trajectory;
- `E`: current normalized operational reserve;
- `Et`: cumulative normalized capability/resource transfer into attempted work;
- `F`: realized cumulative productive flow/progress;
- `e`: cumulative normalized disturbance/entropy burden.

The experiment also derives preregistered trajectory features from the observed history:

- recent Flow slope over the latest quarter-window;
- recent entropy slope over the latest quarter-window;
- Flow recovery after the largest observed disturbance so far;
- reserve drawdown from initial state;
- transfer efficiency `F / max(Et, epsilon)`;
- entropy-adjusted Flow margin `F - e`.

These are experiment-only operational measurements. They do not rewrite the original EFGM formula and are not candidate canonical EFGM v1/v2 equations.

## Comparators

At each checkpoint compare ROC-AUC for terminal A versus M using:

1. `F` alone — primary simple comparator;
2. `E` alone;
3. `e` alone;
4. current-state joint variables (`E`, `Et`, `F`, `e`);
5. frozen trajectory-dynamics score using the preregistered history features above.

No coefficients may be fit on the evaluation trajectories. Any composite score coefficients must be fixed in source before the first scientific execution.

## Primary hypothesis

The original-EFGM-inspired trajectory interpretation survives only if all validity criteria pass and, at the 50% checkpoint (step 12):

- H1: trajectory-dynamics ROC-AUC >= 0.75;
- H2: trajectory-dynamics ROC-AUC exceeds Flow-only ROC-AUC by >= 0.05;
- H3: trajectory-dynamics ROC-AUC exceeds the best single-variable comparator among E, F, and e by >= 0.03.

The 25% and 75% checkpoints are secondary preregistered diagnostics and cannot rescue failure of the step-12 primary hypothesis.

## Early-warning criterion

To support the stronger claim that EFGM describes a trajectory rather than merely an outcome, the trajectory-dynamics score must additionally achieve ROC-AUC >= 0.70 at step 6 (25%) while using no future information.

This criterion is reported separately. Failure does not invalidate the primary step-12 test, but it falsifies the stronger early-warning claim.

## Validity criteria

- exactly 240 trajectories;
- exactly 24 steps per trajectory;
- minority terminal class >= 15%;
- no missing/non-finite measurement values;
- labels demonstrably independent of EFGM detector/comparator outputs;
- deterministic rerun produces the same canonical dataset identity and scientific result;
- no post-execution coefficient, threshold, factor, label, checkpoint, or criterion changes.

## Classification

Primary classification:

- `SURVIVED` only if every validity criterion and H1-H3 pass at step 12;
- otherwise `FALSIFIED` for this operationalization.

Early-warning classification:

- `SUPPORTED` only if the step-6 AUC criterion passes;
- otherwise `NOT SUPPORTED`.

A FALSIFIED result does not falsify the historical EFGM expression as a universal theory. It falsifies this preregistered trajectory operationalization in this synthetic environment.

## Scientific custody

The first valid execution is authoritative. Negative results must be preserved. Any implementation defect discovered after execution may be corrected only if the original execution identity/result remains recorded and the correction demonstrably does not alter the scientific hypothesis, labels, factors, coefficients, or criteria.

## Scope exclusions

This experiment must not modify:

- original EFGM notation;
- EFGM v1/v2 equations, weights, thresholds, or provenance semantics;
- Agent Governance v0.3;
- AE/CUE definitions or detector criteria;
- EXP-0008;
- any frozen baseline;
- autonomous-agent authorization or containment state.
