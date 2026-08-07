# EFGM Experiment Runner v0.1

The experiment runner executes reproducible pairwise comparisons against the frozen EFGM v0.2 baseline lineage.

## Frozen comparison baseline

```text
b717f611a0d09bd8e52bc1b0be5ee178eecacf25
```

A permanent reference branch is maintained at:

```text
baseline/efgm-v0.2-frozen
```

Research branches may evolve; this baseline pointer must not.

## Command

```bash
efgm-experiment --benchmark v0.1 --sensitivity-trials 100 --perturbation 0.10 --format markdown
```

The command compares:

```text
v1
v2
g_plus_u
linear
independent_checklist
```

and reports overall, development, validation, per-family, and perturbation-sensitivity results.

## Pairwise interpretation

For every benchmark pair, the externally supplied benchmark label identifies one preferred case and one controlled mutation. A model receives:

- win: preferred score > mutated score;
- tie: equal scores;
- loss: preferred score < mutated score.

The runner reports both strict win rate and tie-adjusted accuracy. Ties receive 0.5 only in the tie-adjusted descriptive metric; they remain ties in the raw counts.

## Sensitivity analysis

For each pair and trial, the runner independently perturbs normalized metric/checklist observations by a uniform amount within the requested +/- bound, clips values to `[0, 1]`, rescoring all comparison models with a deterministic seed.

The primary robustness measure is the probability that the preferred case remains ranked above the controlled mutation under perturbation.

Sensitivity is a measurement-noise stress test, not evidence that the original observations are statistically distributed in this way.

## V1 projection

V1 cannot represent several v2 constructs. The runner therefore uses a fixed documented projection:

```text
T(v1) = T(v2)
E(v1) = C(v2)
flow quality = same four flow-quality metrics
contradiction density = mean(input contradiction, output contradiction)
uncertainty variance = mean(input ambiguity, uncertainty mismatch)
memory fragmentation = mean(missing context, output context decay)
recursion instability = output reasoning instability
context decay = output context decay
```

Grounding, uncertainty calibration, behavioral entropy, operational entropy, outcome quality, and the explicit Ei/Eo distinction cannot be directly represented in v1. This is a substantive limitation of the comparison and is not hidden.

## Scientific status

Experiment Runner v0.1 is research infrastructure. Its first benchmark is controlled and synthetic. Results can support claims about construct responsiveness, blind spots, regression behavior, and sensitivity under the specified perturbation model. They cannot establish external predictive validity without independent labels, scorers, domains, and sealed holdout evaluation.
