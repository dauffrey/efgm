# Legacy EFGM v1 Metric Summary

This document records the v1 metric families for compatibility and historical comparison. It is not the current v2 scoring rubric.

## Aggregate entropy metrics

V1 used a single aggregate entropy load derived from:

- Contradiction Density
- Uncertainty Variance
- Memory Fragmentation
- Recursion Instability
- Context Decay

A typical equal-weight form was:

```text
e = (CD + UV + MF + RI + CX) / 5
```

## Flow-quality metrics

V1 flow quality used:

- Task Completion Consistency
- Reasoning Continuity
- Semantic Coherence
- Verification Success Rate

A typical equal-weight form was:

```text
Fq = (TCC + RC + SC + VSR) / 4
```

V2 retains some of these constructs but separates input entropy, output entropy, grounding, uncertainty calibration, behavioral entropy, operational entropy, decision quality, and outcome quality. See `../model-specification-v2.md` and `../scoring-rubric-v2.md`.
