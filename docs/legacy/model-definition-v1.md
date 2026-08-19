# Legacy EFGM v1 Model Summary

This document records the historical v1/coherent-flow model for compatibility and research comparison. It is **not** the original EFGM conceptual formulation and is **not** the canonical EFGM v2 decision-integrity specification.

The original EFGM conceptual expression predates this v1 implementation lineage and is preserved separately in [`../original-efgm-formula.md`](../original-efgm-formula.md):

```text
T × E = Et ~ F ± e = A|M
```

## Later v1-lineage conceptual restatement

A later narrative restatement used arrow notation:

```text
T × E → Et → F ± e → A|M
```

This arrow form is useful as a conceptual interpretation, but it must not be presented as the exact original notation.

## Historical operational model

The early v1 prototype used a raw product expression:

```text
F = (T × E × Fq) / (1 + e)
```

The implemented v1 compatibility model later changed the positive composite to a geometric mean:

```text
Q = (T × E × Fq)^(1/3)
F = Q / (1 + e)
```

Historical v1 operational meanings:

- `T`: time / iteration continuity / observation maturity;
- `E`: capability / tooling / operational capacity;
- `Fq`: flow quality;
- `e`: aggregate entropy load;
- `F`: coherent-flow score.

These operational meanings are later formalizations and must not be projected backward onto the original symbols as though they were identical definitions from inception.

V1 remains executable to support prior examples and direct v1-v2 ablation studies. New decision-integrity research should use the canonical v2 specification.
