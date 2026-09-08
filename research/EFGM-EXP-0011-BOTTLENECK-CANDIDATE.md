# EFGM-EXP-0011 candidate: bottleneck integrity

## Status

Exploratory result only. This note is a cautionary re-analysis of the frozen
`EFGM-EXP-0010` dataset; it does not modify the canonical EFGM v2 equation,
any frozen experiment result, or any production classifier.

## Empirical observation

The frozen `EFGM-EXP-0010` synthetic trajectories define the terminal aligned
label as:

```text
progress >= 0.50 and reserve >= 0.08
```

A raw conjunctive proxy

```text
B_raw = min(F, E)
```

reaches ROC-AUC `0.9967` at the 50% checkpoint. The frozen comparators are:

| Comparator | ROC-AUC |
|---|---:|
| `F` only | 0.9284 |
| `E` only | 0.7350 |
| frozen trajectory-dynamics score | 0.9548 |
| frozen current-state joint score | 0.9662 |
| raw `min(F, E)` | 0.9967 |

This is not a valid breakthrough candidate because `F` is already a normalized
success margin while `E` is raw reserve. The terminal rule requires reserve to
exceed `0.08`, so the scale-normalized version is `E / 0.08`, not `E`.
Under the comparable normalization,

```text
B_tau = min(F, E / 0.08)
```

the step-12 AUC drops to `0.9284`, matching `F` only. The apparent gain is
therefore an artifact of arbitrary unit choice and not a robust bottleneck
metric. The raw `min(F, E)` should be treated as a descriptive, unnormalized
post-hoc feature only.

## Mathematical interpretation

The current geometric composite rewards multiplicative sufficiency:

```text
Q = (x1 * ... * xn)^(1/n)
```

A true bottleneck gate would instead model conjunctive feasibility using
compatible normalized margins, for example:

```text
B_tau = min(F / tau_F, E / tau_E)
```

with `tau_F` and `tau_E` fixed before evaluation or inferred only from an
explicitly preregistered development procedure. In the frozen EXP-0010 data,
the raw `min(F, E)` improvement disappears once the reserve variable is placed
on the same success scale as the terminal rule. This means the reported gain is
not currently evidence for a canonical bottleneck integrity model and should be
rejected unless a normalized, preregistered experiment shows it again on an
independent dataset.

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
