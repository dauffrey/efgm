# EFGM Comparison Baselines

EFGM v2 must be compared against simpler alternatives so added complexity is justified empirically.

Minimum comparison families:

1. **Checklist baseline** — binary/ordinal checks for evidence, consistency, uncertainty, scope, and execution issues.
2. **Grounding + calibration baseline** — a deliberately small model using only `G` and `U` (or directly observable proxies).
3. **Weighted linear baseline** — a transparent linear combination of the same available metric values.
4. **EFGM v1** — compatibility model where equivalent inputs can be constructed without leaking information.
5. **Frozen EFGM v2 baseline** — `efgm-v2.0-baseline`.
6. **Candidate model/configuration** — only after its hypothesis is recorded.

A candidate should be rejected or simplified if a materially simpler baseline performs equivalently on validation/holdout evidence and EFGM provides no independent diagnostic advantage.

Baseline implementations and exact formulas should be versioned before formal comparison.
