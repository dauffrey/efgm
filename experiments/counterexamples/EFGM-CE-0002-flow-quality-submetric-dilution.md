# EFGM-CE-0002 — Flow-quality submetric dilution across v1 and v2

## Status

Reproducible counterexample. Internally authored falsification case; not holdout evidence and not external validation.

## Hypothesis

The critical-dimension dilution found in grounding/governance may not be local to those constructs. Weighted averaging inside `Fq` may also allow a semantically essential flow-quality submetric to collapse while both v1 and v2 still emit reassuring classifications.

## Preregistered invariant

A case with `task_completion_consistency = 0.00` or `verification_success_rate = 0.00` is not eligible for the strongest reassuring flow classification when the assessment explicitly treats that submetric as applicable and measured.

The label is defined before comparing model output. No holdout data is used.

## Central v2 case

Set:

- `T=C=G=U=0.95`;
- all output/behavioral/operational entropy composites to approximately `0.02`;
- all flow-quality submetrics to `0.95` except one collapsed metric.

The frozen v2 flow-quality weights are:

```text
task_completion_consistency 0.30
reasoning_continuity        0.25
semantic_coherence          0.25
verification_success_rate   0.20
```

### Zero task-completion consistency

```text
Fq = 0.30*0.00 + 0.25*0.95 + 0.25*0.95 + 0.20*0.95
   = 0.6650

Q  ≈ 0.8846
DQ ≈ 0.8345
```

With `G=0.95` and `Eo≈0.02`, the frozen v2 classifier still returns **Coherent and grounded**.

### Zero verification success

```text
Fq = 0.30*0.95 + 0.25*0.95 + 0.25*0.95 + 0.20*0.00
   = 0.7600

Q  ≈ 0.9085
DQ ≈ 0.8571
```

This also returns **Coherent and grounded**.

The same deterministic pattern occurs for zero reasoning continuity or zero semantic coherence (`Fq=0.7125`, `DQ≈0.8461`).

## V1 replication

V1 uses the same weighted `Fq` family before its geometric quality aggregation. With `T=E=0.95` and entropy `e≈0.02`:

```text
zero task completion      -> F ≈ 0.8270
zero reasoning continuity -> F ≈ 0.8462
zero semantic coherence   -> F ≈ 0.8462
zero verification success -> F ≈ 0.8646
```

All four remain above the v1 `Coherent` threshold of `0.80`.

This makes the finding cross-version rather than an artifact of the v2 grounding gate.

## Perturbation test

10,000 deterministic Monte Carlo trials per collapsed flow metric were evaluated analytically. Non-collapsed positive factors varied in `[0.90, 0.98]`; entropy submetrics varied in `[0.00, 0.05]`; the collapsed flow metric remained near zero in `[0.00, 0.05]`.

Fraction of v2 trials still classified **Coherent and grounded**:

| Collapsed flow submetric | Reassuring classification |
|---|---:|
| task completion consistency | 91.59% |
| reasoning continuity | 99.05% |
| semantic coherence | 99.09% |
| verification success rate | 99.97% |

This is not a knife-edge threshold effect.

## Diagnosis

The earlier counterexample was broader than initially documented. The structural issue is **compensatory submetric aggregation inside a family**, not grounding specifically. Strong sibling observations can wash out a fully collapsed applicable metric before the family composite reaches the top-level geometric aggregation.

This matters because adding only a grounding/governance floor would leave an analogous false-reassurance path through `Fq`.

## Candidate comparison

No scoring formula is promoted. Three classification-only candidates should be compared:

1. **hard critical floor** — explicit preregistered essential submetrics must remain above a threshold;
2. **soft-min / low-percentile family diagnostic** — continuous sensitivity to sparse collapse without replacing the frozen score;
3. **independent invariant checklist** — direct yes/no prerequisite checks outside the EFGM composite.

A hard minimum replacement for `Fq` is rejected as premature because it can overreact to noisy measurements and would break baseline comparability.

## Implication for the next experiment

The sparse-failure suite should not be limited to grounding and agent governance. It should include candidate prerequisites across:

- flow quality;
- grounding;
- operational reliability where execution is required;
- agent authorization/boundary/control families.

Any proposed critical set must be semantically preregistered before evaluation; otherwise the research loop can overfit by declaring whichever failed metrics "critical" after observing model output.

## Conclusion

This materially strengthens CE-0001: critical-dimension dilution is a cross-family, cross-version aggregation failure. A narrow grounding-only patch would be incomplete. The evidence supports testing a general prerequisite-gating layer while preserving frozen continuous scores for comparison.