# EFGM-EXP-0011B — Superseding Fresh Holdout for Coupled-State Early Coherence

Status: PREREGISTERED — superseding prospective holdout; no scientific scoring authorized

## Supersedes

EFGM-EXP-0011 produced a fresh holdout that failed the preregistered class-balance validity gate before any scientific AUC/comparator scoring was exposed. Its minority terminal class was 35/240 = 0.1458333333, below the frozen 0.15 minimum. EXP-0011 therefore remains PRE-EXECUTION INVALID, not FALSIFIED.

EXP-0011B does not modify or rescue that holdout. It preregisters a new prospective holdout design informed only by the observed validity failure, not by any scientific score.

## Historical anchor

The preserved original EFGM expression remains unchanged:

`T × E = Et ~ F ± e = A|M`

## Research question

On a fresh, broader deterministic disturbance distribution, does the preregistered coupled current state `(E, Et, F, e)` provide early discriminative information about eventual terminal Alignment (A) versus Misalignment (M) beyond any single component?

## Scientific contract carried forward unchanged

The following EXP-0011 scientific elements are carried forward unchanged:

- checkpoints: steps 6, 12, 18;
- terminal label evaluated only at step 24;
- measurements: `T`, `E`, `Et`, `F`, `e`;
- geometric, weighted-linear, harmonic, and equal-additive aggregation formulas;
- no parameter fitting on the holdout;
- H1: each coupled scheme AUC >= 0.92 at step 12;
- H2: each coupled scheme exceeds `best_single` by >= 0.02 AUC at step 12;
- H3: exact aggregation-scheme ranking identity across steps 6, 12, 18 using the same numerical tie tolerance and lexical tie-break;
- coupling-value diagnostic threshold: >= 0.01 AUC over equal-additive at step 12;
- early-detection diagnostic benchmark: >= 0.9651 AUC at step 6;
- minority-class validity minimum: >= 0.15;
- validity failure yields `INVALID`, not `FALSIFIED`.

No threshold above is weakened because EXP-0011 failed its validity gate.

## Superseding fresh holdout design

The only prospective design change is to broaden the deterministic disturbance distribution before generation so the evaluation population includes a stronger high-disturbance regime.

Frozen design:

- **288 new scenarios**;
- **24 ordered steps** per scenario;
- scenario seeds exactly **120001 through 120288 inclusive**;
- checkpoints exactly **6, 12, 18**;
- capability levels unchanged: `0.30, 0.42, 0.54, 0.66, 0.78, 0.90`;
- transfer-policy levels unchanged: `0.45, 0.62, 0.79, 0.96`;
- entropy/disturbance bands: `0.10, 0.25, 0.40, 0.55, 0.70, 0.82`;
- exactly **2 deterministic replicates** per capability × transfer-policy × entropy-band cell;
- same noise construction family, transient-pulse construction family, state update equations, normalization conventions, and terminal A/M rule as EXP-0011;
- no EXP-0010 or EXP-0011 seed may appear in this holdout;
- no scientific aggregation/comparator output may influence generation.

This produces a complete 6 × 4 × 6 × 2 factorial grid = 288 scenarios. The new `0.82` entropy band is fixed prospectively to extend the stress range rather than selecting scenarios based on terminal labels.

## Fresh dataset custody

The dataset SHA-256 is intentionally unknown at preregistration time.

After implementation:

1. generate the 288-scenario dataset exactly once without computing AUC or coupled/comparator scores;
2. record only dataset identity and validity metadata: generator identity, implementation commit, seed interval, scenario/observation counts, checkpoints, class counts, minority fraction, and canonical SHA-256;
3. if minority class is below 0.15 or any other validity rule fails, stop and record EXP-0011B as PRE-EXECUTION INVALID;
4. if validity passes, commit an implementation/dataset freeze declaration before any scientific evaluation;
5. only after that freeze may the first scientific AUC/comparator evaluation be authorized.

## Aggregation schemes

### Equal-weight geometric

`C_geometric = (E × Et × F × (1-e))^(1/4)`

### Weighted linear

`C_linear = 0.30×E + 0.35×Et + 0.20×F + 0.15×(1-e)`

### Harmonic

`C_harmonic = 4 / (1/E + 1/Et + 1/F + 1/(1-e))`

Exact zero input yields harmonic score `0.0`.

### Equal-additive diagnostic baseline

`C_additive = 0.25×E + 0.25×Et + 0.25×F + 0.25×(1-e)`

`best_single = max(AUC_E, AUC_Et, AUC_F, AUC_1_minus_e)` at the same checkpoint.

## Exact H3 ranking rule

For each checkpoint, order `geometric`, `harmonic`, `linear` by descending AUC. Exact numerical ties use `abs(delta) <= 1e-12` and lexical tie-break `geometric < harmonic < linear`.

H3 passes iff:

`rank_6 == rank_12 == rank_18`

## Validity criteria

A scientific evaluation is authorized only if all are true:

- exactly 288 scenario IDs;
- seeds exactly 120001..120288, each once;
- exactly 24 steps per scenario;
- checkpoints exactly 6, 12, 18;
- no seed overlap with EXP-0010 or EXP-0011;
- terminal labels independent of all composite/comparator outputs;
- minority terminal class >= 0.15;
- all required measurements finite;
- canonical dataset SHA matches the pre-execution freeze declaration;
- deterministic regeneration reproduces the same canonical SHA;
- no post-generation change to formulas, coefficients, thresholds, checkpoints, ranking rule, label rule, or validity criteria.

## Classification

If the holdout validity gate fails before scoring: `PRE-EXECUTION INVALID`.

If validity passes and scientific evaluation is later authorized:

- `SURVIVED` iff H1, H2, and H3 all pass at step 12;
- otherwise `FALSIFIED`.

Secondary diagnostics cannot rescue the primary classification.

## Scope exclusions

EXP-0011B must not modify:

- original EFGM notation;
- canonical EFGM v1/v2 equations, weights, thresholds, or provenance semantics;
- Agent Governance v0.3;
- AE/CUE definitions or detector criteria;
- EXP-0008, EXP-0009, EXP-0010, or the preserved EXP-0011 invalid record;
- any frozen baseline;
- autonomous-agent authorization or containment state.

## Interpretation boundary

A later SURVIVED result would support only this coupled-state operationalization on this prospectively broadened synthetic holdout. It would not establish the historical EFGM expression as a universal law.