# EFGM Comparison Baselines

EFGM v2 must be compared against simpler alternatives so added complexity is justified empirically.

Two baseline categories are required because a baseline derived from EFGM's own composites is useful for ablation but is not fully independent evidence.

## 1. EFGM-derived ablation baselines

These consume EFGM observations/composites and test whether the full v2 aggregation adds value beyond simpler use of the same information:

1. **Threshold checklist** — simple pass/fail checks over EFGM composites.
2. **Grounding + calibration** — deliberately small model using only `G` and `U`.
3. **Weighted linear** — transparent linear combination of the same major EFGM composites.
4. **EFGM v1** — compatibility model where equivalent inputs can be constructed without outcome leakage.
5. **Frozen EFGM v2 baseline** — `efgm-v2.0-baseline`.
6. **Candidate model/configuration** — only after its hypothesis is recorded.

These are aggregation/construct ablations, not independent ground truth.

## 2. Independent comparators

At least one serious validation benchmark should also use a comparator established **without consuming EFGM composite scores**.

The code includes a minimal five-criterion independent checklist:

```text
evidence_supported
internally_consistent
uncertainty_appropriate
scope_aligned
execution_reliable
```

Benchmark authors establish those ratings before or independently of EFGM scoring. External human/expert labels and task-specific statistical metrics are preferred where available.

A candidate should be rejected or simplified if a materially simpler baseline performs equivalently on validation/holdout evidence and EFGM provides no independent diagnostic advantage.

Baseline implementations, criteria, label sources, and exact formulas must be versioned before formal comparison.
