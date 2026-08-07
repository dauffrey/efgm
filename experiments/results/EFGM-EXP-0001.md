# EFGM-EXP-0001 — Benchmark v0.1 controlled comparison

## Status

**Completed — controlled synthetic internal evidence.**

This experiment was executed by GitHub Actions `EFGM Check` run #46 on Python 3.12 using Experiment Runner v0.1. The benchmark step completed successfully with 100 perturbation trials per pair.

Experiment code head at execution:

```text
bc0c1012c2309c723814e6dbdcfaaaae55b01436
```

Frozen EFGM v0.2 comparison baseline:

```text
b717f611a0d09bd8e52bc1b0be5ee178eecacf25
```

Canonical Benchmark v0.1 SHA-256:

```text
ff6d6cb3243093ab375951f5b75310ca2b5e3341eeccd14ada028b417499bc7e
```

Dataset size:

```text
144 cases
72 controlled preferred/mutated pairs
12 scenario families
96 development cases
48 validation cases
```

## Overall paired ranking

| Model | Wins | Ties | Losses | Strict win rate | Tie-adjusted accuracy | Mean separation |
|---|---:|---:|---:|---:|---:|---:|
| v1 | 42 | 30 | 0 | 0.5833 | 0.7917 | 0.0393 |
| v2 | 72 | 0 | 0 | **1.0000** | **1.0000** | **0.1246** |
| G+U | 48 | 24 | 0 | 0.6667 | 0.8333 | 0.0971 |
| linear | 72 | 0 | 0 | **1.0000** | **1.0000** | 0.0689 |
| independent checklist | 66 | 6 | 0 | 0.9167 | 0.9583 | 0.0931 |

## Validation split

| Model | Wins | Ties | Losses | Strict win rate | Tie-adjusted accuracy |
|---|---:|---:|---:|---:|---:|
| v1 | 14 | 10 | 0 | 0.5833 | 0.7917 |
| v2 | 24 | 0 | 0 | **1.0000** | **1.0000** |
| G+U | 16 | 8 | 0 | 0.6667 | 0.8333 |
| linear | 24 | 0 | 0 | **1.0000** | **1.0000** |
| independent checklist | 22 | 2 | 0 | 0.9167 | 0.9583 |

The development and validation partitions show the same aggregate ranking pattern. This is expected in a deterministic controlled-mutation benchmark and must not be interpreted as an independent holdout result.

## Sensitivity analysis

Uniform independent perturbation of normalized observations:

```text
+/- 0.10
100 trials per pair
seed 20260808
```

| Model | Mean preference probability | Median | Minimum | Pairs >= .95 | Pairs >= .80 |
|---|---:|---:|---:|---:|---:|
| v1 | 0.7110 | 0.6950 | 0.4200 | 18 | 26 |
| v2 | **0.9788** | **1.0000** | **0.8300** | **62** | **72** |
| G+U | 0.7833 | 0.9000 | 0.3700 | 33 | 40 |
| linear | 0.9533 | 0.9750 | 0.7700 | 50 | 69 |
| independent checklist | 0.9343 | 1.0000 | 0.4900 | 56 | 63 |

## Findings

1. **V2 responded to all 72 controlled mutation pairs.** This is evidence that the current v2 construct set and aggregation are responsive across the benchmark's intended scenario families.
2. **The weighted linear baseline also ranked all 72 pairs correctly.** This is a major constraint on any claim that the current nonlinear v2 equation is necessary. On nominal pairwise accuracy, v2 did not outperform the simpler linear comparator.
3. **V2 produced a larger average preferred-vs-mutated score separation than the linear baseline** (`0.1246` versus `0.0689`) and stronger perturbation robustness (`0.9788` versus `0.9533` mean preference probability; minimum `0.83` versus `0.77`). This is a useful hypothesis for further testing, not proof of superior generalization.
4. **The independent five-criterion checklist was strong** (`0.9583` tie-adjusted accuracy) but tied on six behavioral-feedback pairs because that deliberately small checklist has no explicit behavioral-bias criterion.
5. **G+U was insufficient as a complete replacement**: it tied on 24 pairs, demonstrating blind spots for constructs such as output/context degradation, tool execution, and behavioral feedback.
6. **V1 tied on 30 pairs.** Its older input space cannot directly represent grounding, calibration, behavioral entropy, operational entropy, or the Ei/Eo distinction, so the result supports the rationale for the v2 expansion but does not independently validate the v2 formula.
7. **No model produced a nominal reversal/loss** on this controlled benchmark. That is a warning that Benchmark v0.1 is primarily a construct-responsiveness benchmark, not yet a sufficiently adversarial external discriminator.

## Scientific interpretation

The strongest defensible conclusion is:

> On EFGM Benchmark v0.1, EFGM v2 showed complete controlled-mutation responsiveness and the strongest perturbation robustness, but a much simpler weighted linear model achieved the same nominal pairwise ranking accuracy. The result supports continued investigation of v2's construct coverage and robustness while leaving the necessity of its current nonlinear equation unresolved.

This experiment does **not** establish scientific proof or external predictive validity.

## Required next experiment

The next benchmark should be designed specifically to distinguish **v2 from the linear baseline** without selecting cases after observing their scores. It should include independently authored labels and scenarios where aggregation assumptions can disagree, followed by a sealed holdout. Key targets:

- compensatory versus non-compensatory failures;
- one critically weak factor with otherwise strong metrics;
- multiple moderate entropy penalties versus one severe penalty;
- grounding-gate cases near thresholds;
- cases where behavioral/operational entropy interacts with strong positive factors;
- externally authored cases not derived from EFGM terminology;
- blinded human or external benchmark labels.

Until that is done, the linear baseline remains a serious competing explanation for Benchmark v0.1 performance.
