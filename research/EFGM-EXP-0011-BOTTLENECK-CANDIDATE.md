# EFGM-EXP-0011 candidate: bottleneck integrity

## Status

Exploratory result only. This note does not modify the canonical EFGM v2
equation, frozen experiment results, or any production classifier.

## Empirical observation

The frozen `EFGM-EXP-0010` synthetic trajectories define the terminal aligned
label as:

```text
progress >= 0.50 and reserve >= 0.08
```

At the 50% checkpoint, the simple conjunctive proxy

```text
B = min(F, E)
```

produced ROC-AUC `0.9967` against terminal A/M. The frozen comparators produced:

| Comparator | ROC-AUC |
|---|---:|
| `F` only | 0.9284 |
| `E` only | 0.7350 |
| frozen trajectory-dynamics score | 0.9548 |
| frozen current-state joint score | 0.9662 |
| candidate `min(F, E)` | 0.9967 |

This is a descriptive re-analysis of the frozen dataset, not a new
preregistered result. The improvement is checkpoint-specific: `min(F, E)` has
AUC `0.9265` at step 6 and `0.8599` at step 18. That pattern is consistent
with a bottleneck becoming informative near the point where both progress and
reserve must be adequate, but it also makes overfitting to the synthetic
terminal rule a serious possibility.

## Mathematical interpretation

The current geometric composite rewards multiplicative sufficiency:

```text
Q = (x1 * ... * xn)^(1/n)
```

The candidate bottleneck statistic instead models conjunctive feasibility:

```text
B = min(x1, ..., xn)
```

`B` is invariant to compensating improvements in one dimension when another
dimension remains limiting. This matches requirements of the form "make enough
progress while retaining enough reserve” better than an average or product.
It is therefore a candidate **diagnostic or gate**, not an unconditional
replacement for the geometric mean.

For differently scaled variables, a future experiment must use normalized
success margins rather than raw values:

```text
B_tau = min(F / tau_F, E / tau_E)
```

with `tau_F` and `tau_E` fixed before evaluation and learned only from
development data if learning is part of the preregistration.

## Required falsification test

A valid EXP-0011 should:

1. use independently generated trajectories whose labels are not defined by
   the proposed bottleneck;
2. preregister `B_tau`, the checkpoint, and all normalization constants;
3. compare against `F`, `E`, the existing geometric joint score, and the frozen
   trajectory score;
4. include additive, geometric, and simple checklist baselines;
5. evaluate across multiple terminal-rule families, including non-conjunctive
   and reserve-independent outcomes;
6. report calibration and false-reassurance/false-alarm trade-offs, not only
   ROC-AUC;
7. use an externally sealed holdout before proposing any v2 or governance
   classifier change.

The candidate should be rejected if its advantage disappears when the label
rule is not a conjunction, or if a simpler independently defined gate matches
it without the EFGM terminology.
