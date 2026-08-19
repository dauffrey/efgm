## Recommended v0.2 Scoring Direction

The original EFGM conceptual formulation predates the v1 scoring prototype and is preserved separately in [`original-efgm-formula.md`](original-efgm-formula.md):

```text
T × E = Et ~ F ± e = A|M
```

The early v1 operational prototype equation was intentionally lightweight:

```text
F = (T × E × Fq) / (1 + e)
```

This operational equation was a later formalization of the broader concept; it should not be described as the exact original EFGM formula.

Based on scenario testing, the recommended v0.2 direction was to separate coherence, grounding, entropy recovery, decision quality, and outcome quality.

### Geometric Mean Update

The positive quality factors should use a geometric mean rather than a raw product:

```text
Q = (T × E × Fq)^(1/3)
F = Q / (1 + e)
```

For the expanded decision-integrity model:

```text
Q = (T × C × Fq × G × U)^(1/5)
DQ = Q / (1 + Eo + Be + Oe)
```

This prevents strong-but-imperfect positive factors from collapsing the score too aggressively.

### Expanded v0.2 Formula Set

```text
Ei = w1IC + w2IA + w3IG + w4MC + w5H

Eo = w1OC + w2UM + w3GD + w4RI + w5CD

CRC = (Ei - Eo) / max(Ei, ε)

G = w1RS + w2EV + w3TR + w4FC + w5DC

Q = (T × C × Fq × G × U)^(1/5)

DQ = Q / (1 + Eo + Be + Oe)

OutcomeConfidence = DQ × (1 - H)

OD = OQ - DQ
```

Where:

| Symbol | Meaning |
|---|---|
| `Ei` | Input entropy |
| `Eo` | Output entropy |
| `CRC` | Coherence Recovery Capacity |
| `C` | Capability / correct tool or rule set |
| `G` | Grounding / verification integrity |
| `U` | Uncertainty calibration |
| `Be` | Behavioral entropy |
| `Oe` | Operational entropy |
| `DQ` | Decision quality |
| `OQ` | Outcome quality |
| `OD` | Outcome divergence |
| `H` | Hidden-information load |

The key governance distinction is:

> EFGM should evaluate decision integrity at the time the decision was made, not only whether the final outcome succeeded.
