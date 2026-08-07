# Legacy EFGM v1 Model Summary

This document records the historical v1/coherent-flow model for compatibility and research comparison. It is **not** the canonical EFGM v2 decision-integrity specification.

## Historical conceptual model

```text
T × E → Et → F ± e → A|M
```

## Historical operational model

The original prototype used a raw product expression:

```text
F = (T × E × Fq) / (1 + e)
```

The implemented v1 compatibility model later changed the positive composite to a geometric mean:

```text
Q = (T × E × Fq)^(1/3)
F = Q / (1 + e)
```

Historical meanings:

- `T`: time / iteration continuity / observation maturity;
- `E`: capability / tooling / operational capacity;
- `Fq`: flow quality;
- `e`: aggregate entropy load;
- `F`: coherent-flow score.

V1 remains executable to support prior examples and direct v1-v2 ablation studies. New decision-integrity research should use the canonical v2 specification.
