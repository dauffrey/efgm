# EFGM-EXP-0011 — Coupled State Early Coherence Detection

Status: PREREGISTERED — implementation and execution not yet authorized

## Historical context

EFGM-EXP-0010 tested whether trajectory-history derivatives (flow slope, entropy slope, recovery-after-peak) added discriminative power beyond contemporaneous flow. The primary hypothesis FALSIFIED at step 12 (only 0.0264 AUC improvement over F-only, below the preregistered 0.05 threshold).

However, a preregistered comparator in EXP-0010 — a simple current-state joint of `(E, Et, F, e)` using equal-weight geometric composition — outperformed the trajectory-dynamics score at all three checkpoints:

- Step 6: joint 0.9533 vs trajectory 0.9056
- Step 12: joint 0.9662 vs trajectory 0.9548
- Step 18: joint 0.9835 vs trajectory 0.9651

This is **development evidence only**. Because EXP-0011 is motivated by an observed EXP-0010 result, EXP-0010 trajectories may not be reused as confirmatory evidence.

## Research question

Does a coherent coupling of normalized reserve, transfer, flow, and entropy complement provide discriminative early-detection capability for terminal Alignment (A) versus Misalignment (M), and is this capability robust across multiple aggregation schemes on a fresh deterministic holdout?

## Why this follows EXP-0010

EXP-0010 falsified its trajectory-history primary hypothesis and exposed a stronger current-state comparator. EXP-0011 does not retry, modify, or reinterpret EXP-0010. It preregisters a new prospective test of the narrower follow-on hypothesis that **coupled current state may carry early coherence information beyond any single state variable**.

Because this hypothesis was motivated by an observed comparator, independent validation is mandatory.

## Fresh deterministic holdout

EXP-0011 must use a fresh holdout that was not inspected in EXP-0010.

Frozen holdout construction:

- **240 new scenarios**;
- **24 ordered steps** per scenario;
- deterministic scenario seeds **110001 through 110240 inclusive**;
- checkpoints fixed at steps **6, 12, and 18**;
- terminal label evaluated only at step 24;
- scenario seeds/IDs used by EXP-0010 are forbidden;
- the same synthetic generator family, variable definitions, normalization conventions, and terminal A/M label rule used by EXP-0010 must be preserved unless a required implementation incompatibility is discovered before any scientific execution;
- no coefficient, threshold, aggregation scheme, comparator, or success criterion may influence holdout generation.

The fresh dataset SHA-256 is **not known at preregistration time**. After implementation, the dataset must be generated once without evaluating any AUC/comparator output. Its canonical SHA-256, generator identity, implementation commit, seed interval, row count, class balance, and checkpoint set must then be committed in an **implementation/dataset freeze declaration**. Only after that freeze commit may the first scientific evaluation run.

If the implementation cannot produce the specified fresh holdout without changing the scientific design, execution must stop and this preregistration must be superseded explicitly rather than silently amended.

## Frozen measurements

At checkpoints 6, 12, and 18, use only information available at or before that checkpoint:

- `T` — elapsed trajectory fraction;
- `E` — normalized operational reserve;
- `Et` — cumulative normalized capability/resource transfer;
- `F` — realized cumulative productive flow/progress;
- `e` — cumulative normalized disturbance/entropy burden.

Prediction target: terminal `A` versus `M`, using the same terminal outcome rule as EXP-0010 and no detector/composite output in label generation.

## No parameter fitting

All aggregation coefficients are preregistered below. No coefficient, transform, threshold, feature, scheme, or checkpoint may be tuned using the EXP-0011 holdout.

## Three preregistered aggregation schemes

### Scheme 1: Equal-weight geometric mean

```text
C_geometric = (E × Et × F × (1-e))^(1/4)
```

Rationale: multiplicative proportional coupling; all four normalized state terms contribute symmetrically.

### Scheme 2: Weighted linear

```text
C_linear = 0.30×E + 0.35×Et + 0.20×F + 0.15×(1-e)
```

Rationale: a preregistered asymmetric composition emphasizing transfer and reserve. Coefficients sum to 1.0 and are frozen.

### Scheme 3: Harmonic mean

```text
C_harmonic = 4 / (1/E + 1/Et + 1/F + 1/(1-e))
```

For exact zero-valued inputs, the harmonic score is defined as `0.0`. No epsilon choice may be introduced after execution.

Rationale: bottleneck-sensitive coupling; one weak component suppresses the composite.

## Comparators

At each checkpoint compute ROC-AUC for:

1. `E` alone;
2. `Et` alone;
3. `F` alone;
4. `1-e` alone;
5. `C_geometric`;
6. `C_linear`;
7. `C_harmonic`;
8. additive baseline:

```text
C_additive = 0.25×E + 0.25×Et + 0.25×F + 0.25×(1-e)
```

`best_single` is defined exactly as `max(AUC_E, AUC_Et, AUC_F, AUC_1_minus_e)` at the same checkpoint.

## Primary hypotheses — step 12 only

At the 50% checkpoint:

- **H1:** each of `C_geometric`, `C_linear`, and `C_harmonic` has ROC-AUC `>= 0.92`;
- **H2:** each of the three coupled schemes exceeds `best_single` by `>= 0.02` ROC-AUC;
- **H3:** aggregation-scheme ranking stability passes the exact rule below.

All H1-H3 must pass. Failure of any one criterion FALSIFIES the primary hypothesis for this operationalization.

## Exact H3 ranking-stability rule

For each checkpoint, construct the ordered triple of scheme names sorted by:

1. descending ROC-AUC;
2. for exact numerical ties (`abs(delta) <= 1e-12`), fixed lexical tie-break order: `geometric < harmonic < linear`.

Let `rank_6`, `rank_12`, and `rank_18` be those ordered triples.

**H3 passes if and only if:**

```text
rank_6 == rank_12 == rank_18
```

No qualitative interpretation, rank-correlation substitute, alternate tolerance, or post-hoc exception is permitted.

## Coupling-value diagnostic

Question: **Does a non-additive coupling scheme add value beyond equal-weight addition?**

At step 12:

- `COUPLING_ADDS_VALUE` if `max(AUC_geometric, AUC_linear, AUC_harmonic) - AUC_additive >= 0.01`;
- otherwise `SIMPLE_ADDITION_SUFFICIENT`.

This is secondary and cannot rescue or falsify the primary H1-H3 classification.

## Early-detection diagnostic

Question: **Can a coupled state identify terminal A/M very early in a fresh trajectory?**

Frozen benchmark from EXP-0010 trajectory dynamics at step 18: `0.9651`.

At step 6:

- `EARLY_DETECTION_ACHIEVED` if at least one of the three coupled schemes has ROC-AUC `>= 0.9651`;
- otherwise `NOT_ACHIEVED`.

This is secondary and cannot rescue or falsify the primary H1-H3 classification.

## Validity criteria

The scientific run is valid only if all are true:

- exactly **240** scenario IDs;
- scenario seeds are exactly **110001..110240**, each used once;
- exactly **24** steps are generated per scenario;
- exactly **3** prediction checkpoints: `6, 12, 18`;
- no EXP-0010 scenario ID or seed appears in the EXP-0011 holdout;
- terminal labels are computed independently of composite/comparator outputs;
- minority terminal class is `>= 15%`;
- all required measurement and AUC values are finite;
- frozen dataset SHA-256 exactly matches the pre-execution implementation/dataset freeze declaration;
- deterministic rerun produces the identical canonical dataset SHA-256 and identical scientific result;
- no post-execution coefficient, scheme, transform, checkpoint, comparator, label rule, threshold, ranking rule, or criterion changes occur.

Failure of a validity criterion yields `INVALID`, not `FALSIFIED`.

## Classification

### Primary

- `SURVIVED` if validity passes and H1, H2, and H3 all pass;
- `FALSIFIED` if validity passes and any of H1, H2, or H3 fails;
- `INVALID` if any validity criterion fails.

### Coupling-value diagnosis

- `COUPLING_ADDS_VALUE` if the frozen step-12 criterion above passes;
- `SIMPLE_ADDITION_SUFFICIENT` otherwise.

### Early-detection diagnosis

- `EARLY_DETECTION_ACHIEVED` if the frozen step-6 criterion above passes;
- `NOT_ACHIEVED` otherwise.

## Required pre-execution freeze sequence

No scientific evaluation may occur until all of the following have happened in order:

1. this preregistration is reviewed and declared frozen;
2. implementation and tests are completed without modifying the frozen scientific contract;
3. the fresh dataset is generated from seeds `110001..110240` **without running or exposing scientific AUC/comparator results**;
4. an implementation/dataset freeze declaration records the exact implementation commit and canonical dataset SHA-256;
5. CI verifies deterministic dataset identity and validity plumbing;
6. only then is the first scientific evaluation authorized.

The first valid scientific evaluation after the freeze declaration is authoritative.

## Scope exclusions

This experiment must not modify:

- original EFGM notation;
- EFGM v1/v2 equations, weights, thresholds, or provenance semantics;
- Agent Governance v0.3;
- AE/CUE definitions or detector criteria;
- EXP-0008, EXP-0009, or EXP-0010;
- any frozen baseline;
- autonomous-agent authorization or containment state.

## Scientific custody

Negative results must be preserved.

Any implementation defect discovered after scientific execution may be corrected only if:

1. the original execution identity and result remain preserved;
2. the defect and correction are explicitly documented;
3. the correction does not alter the frozen schemes, coefficients, checkpoints, seeds, label rule, comparators, thresholds, ranking rule, or success/falsification criteria;
4. human review confirms the correction is necessary and is not an attempt to rescue a FALSIFIED result.

A corrected run is additional evidence; it does not erase the first valid run.

## Interpretation boundary

EXP-0011 is a prospective synthetic test motivated by EXP-0010 development evidence. A SURVIVED result would support this specific coupled-state operationalization on one fresh deterministic holdout. It would not establish the historical EFGM expression as a universal law or modify canonical EFGM v1/v2.
