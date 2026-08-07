# EFGM v0.2 Recommendations — Historical Design Rationale

This file records the transition from the original coherent-flow model to the v2 decision-integrity architecture. It is retained as historical design rationale, **not** as the authoritative current specification.

The current v2 baseline is defined by:

- [`model-specification-v2.md`](model-specification-v2.md)
- [`scoring-rubric-v2.md`](scoring-rubric-v2.md)
- `src/efgm/scoring_v2.py`
- `src/efgm/config/efgm-v2.0-baseline.json`

The v0.2 transition introduced the following major ideas:

1. use a geometric mean rather than the early raw positive-factor product;
2. rename capability to `C` in v2;
3. separate input entropy `Ei` from output entropy `Eo`;
4. add Coherence Recovery Capacity `CRC`;
5. separate grounding `G` from internal coherence;
6. add uncertainty calibration `U`;
7. model behavioral entropy `Be`;
8. model operational entropy `Oe`;
9. separate Decision Quality `DQ` from Outcome Quality `OQ`;
10. represent Outcome Divergence `OD = OQ - DQ` and outcome confidence under hidden information.

The current formula family remains:

```text
Ei = weighted input entropy
Eo = weighted output entropy
CRC = (Ei - Eo) / max(Ei, ε)
G = weighted grounding
Q = (T × C × Fq × G × U)^(1/5)
DQ = Q / (1 + Eo + Be + Oe)
OutcomeConfidence = DQ × (1 - H)
OD = OQ - DQ
```

Subsequent stabilization added evidence-backed observations, versioned external configuration, a critical grounding classification gate, explicit DQ/CRC semantics, and falsification-oriented research controls. Consult the canonical documents rather than this historical summary for current thresholds, definitions, and research rules.
