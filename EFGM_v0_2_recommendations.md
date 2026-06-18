# EFGM v0.2 Consolidated Recommendations

## Status

These recommendations update the original EFGM v0.1 scoring model.

The original operational equation was:

```text
F = (T × E × Fq) / (1 + e)
```

The recommended direction is to keep the original model as a lightweight compatibility mode, but add a v0.2 decision-integrity model for AI governance, incident review, release readiness, and agentic workflow evaluation.

---

## 1. Replace raw product scoring with a geometric mean

### Problem

Raw multiplication collapses scores too aggressively when several positive factors are strong but imperfect.

### Update

```text
Q = (T × E × Fq)^(1/3)
F = Q / (1 + e)
```

For the v0.2 decision model:

```text
Q = (T × C × Fq × G × U)^(1/5)
DQ = Q / (1 + Eo + Be + Oe)
```

---

## 2. Rename capability from E to C in v0.2

`E` is now overloaded because EFGM uses entropy symbols such as `Ei` and `Eo`.

Use:

```text
C = Capability / correct tool or rule set
```

Keep old `E` in v0.1 compatibility mode.

---

## 3. Split entropy into input entropy and output entropy

### Input Entropy

```text
Ei = w1IC + w2IA + w3IG + w4MC + w5H
```

| Symbol | Meaning |
|---|---|
| IC | Input contradiction |
| IA | Input ambiguity |
| IG | Input goal conflict |
| MC | Missing context |
| H | Hidden-information load |

### Output Entropy

```text
Eo = w1OC + w2UM + w3GD + w4RI + w5CD
```

| Symbol | Meaning |
|---|---|
| OC | Output contradiction |
| UM | Uncertainty mismatch |
| GD | Goal drift |
| RI | Reasoning instability |
| CD | Context decay |

---

## 4. Add Coherence Recovery Capacity

```text
CRC = (Ei - Eo) / max(Ei, ε)
```

Interpretation:

| CRC | Meaning |
|---:|---|
| High positive | System reduced entropy |
| Near zero | System did not reduce entropy |
| Negative | System added disorder |

This was the strongest measurable signal from the Gemini contradiction tests.

---

## 5. Add grounding as a standalone multiplier

Coherence is not enough.

The warehouse test produced a coherent but invented answer: "Superpositional Liability." That exposed the need to separate internal coherence from real-world validity.

```text
G = w1RS + w2EV + w3TR + w4FC + w5DC
```

| Symbol | Meaning |
|---|---|
| RS | Rule support |
| EV | Evidence validity |
| TR | Traceability |
| FC | Factual consistency |
| DC | Domain calibration |

---

## 6. Add uncertainty calibration

```text
U = uncertainty calibration
```

This measures whether the system expresses confidence proportional to the evidence.

High confidence with weak evidence should reduce the decision-quality score.

---

## 7. Add behavioral entropy

Roulette exposed behavioral degradation patterns that are not ordinary semantic entropy.

```text
Be = w1CH + w2OB + w3SC + w4FP + w5OCF
```

| Symbol | Meaning |
|---|---|
| CH | Chasing behavior |
| OB | Outcome bias |
| SC | Sunk-cost pressure |
| FP | False pattern detection |
| OCF | Overconfidence feedback |

---

## 8. Add operational entropy

Operational failure matters even when reasoning is good.

```text
Oe = w1TO + w2RI + w3TF + w4LP + w5WI
```

| Symbol | Meaning |
|---|---|
| TO | Timeout rate |
| RI | Retry instability |
| TF | Tool failure rate |
| LP | Latency pressure |
| WI | Workflow interruption |

---

## 9. Separate decision quality from outcome quality

The casino tests repeatedly showed:

```text
Good decision ≠ good outcome
Bad decision ≠ bad outcome
```

### Decision Quality

```text
DQ = Q / (1 + Eo + Be + Oe)
```

### Outcome Quality

```text
OQ ∈ [0,1]
```

### Outcome Divergence

```text
OD = OQ - DQ
```

Interpretation:

| OD | Meaning |
|---:|---|
| Positive | Lucky or favorable variance |
| Near zero | Outcome aligned with decision |
| Negative | Bad variance or hidden information punished a good decision |

---

## 10. Add outcome confidence

Hidden information should not automatically punish decision quality. It should reduce confidence in the outcome.

```text
OutcomeConfidence = DQ × (1 - H)
```

This is useful for poker, incident response, releases, investigations, and agentic AI workflows.

---

## Recommended v0.2 formula set

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

---

## Recommended classification model

| Classification | Condition |
|---|---|
| Coherent and grounded | High DQ, high G, low Eo |
| Coherent but weakly grounded | High Q/Fq, low G |
| High recovery | High CRC |
| Outcome-chasing risk | High Be |
| Good decision, bad variance | High DQ, low OQ, high H |
| Lucky outcome | Low/medium DQ, high OQ |
| Degraded | Low DQ, high Eo |
| Operational failure | High Oe |

---

## Practical meaning

The updated EFGM model measures whether an AI system preserves coherent, grounded, calibrated decision-making under entropy, uncertainty, and feedback pressure.

It is still not a proven scientific law or production-ready risk engine, but it is now a more testable governance framework.
