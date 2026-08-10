# Executive Summary: Entropy-Flow Governance Model (EFGM)

## Purpose

The **Entropy-Flow Governance Model (EFGM)** is an experimental governance and measurement framework for evaluating whether AI-assisted reasoning, operational decisions, software-delivery workflows, and autonomous-agent activity remain coherent, grounded, calibrated, traceable, and governed under degradation pressure.

EFGM is not a proven scientific law, compliance standard, or production-ready risk engine.

## Current Model Authority

The canonical research baseline is **EFGM v2 decision integrity**. The earlier coherent-flow equation:

```text
F = (T × E × Fq) / (1 + e)
```

belongs to the historical v1 compatibility model. It remains useful for explaining EFGM's conceptual origin, but it is **not the current operational research equation**.

The canonical v2 formula family is:

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

Where:

| Symbol | Meaning |
|---|---|
| `T` | Observation maturity / sequence continuity |
| `C` | Capability suitability |
| `Fq` | Flow quality |
| `G` | Grounding |
| `U` | Uncertainty calibration |
| `Ei` | Input entropy |
| `Eo` | Output entropy |
| `Be` | Behavioral entropy |
| `Oe` | Operational entropy |
| `H` | Hidden-information load |
| `CRC` | Coherence Recovery Capacity |
| `DQ` | Decision Quality |
| `OQ` | Outcome Quality |
| `OD` | Outcome Divergence |

## Core Distinctions

EFGM v2 intentionally separates:

- input disorder from output degradation;
- internal coherence from external grounding;
- uncertainty from uncertainty calibration;
- decision quality from outcome quality;
- decision quality from coherence recovery;
- missing evidence from measured low values.

A successful outcome does not prove that the decision was good, and a poor outcome does not prove that the decision was bad.

## Evidence Discipline

Research-grade scoring uses auditable `MetricObservation` records with:

```text
value
status
rationale
evidence_refs
scorer_id
scorer_type
confidence
```

Canonical observation states are:

- `observed`;
- `inferred`;
- `unknown`;
- `not_applicable`.

`unknown` is never silently interpreted as safe or as numeric zero.

## Experimental Agent-Governance Extension

EFGM v0.3 — Governed Agentic Flow is an **experimental candidate**, not part of the frozen v2 baseline.

Its core hypothesis is:

> High coherent task flow can coexist with weak governance integrity.

The candidate measures:

- objective alignment;
- boundary integrity;
- observability;
- environmental-memory governance;
- coordination governance;
- control recoverability;
- agency amplification.

Agentic Governance Integrity is denoted `GI` to avoid collision with v2 Grounding (`G`).

The current experimental risk decomposition distinguishes:

```text
AE  = A_a × (1 - GI)
CUE = F_T × AE
```

`AE` measures **Agency Exposure**: consequential agency that is insufficiently governed.

`CUE` measures **Coherent Unsafe Execution**: effective task flow operating through that exposure.

These formulas are hypotheses under test, not validated risk probabilities.

## Known Limitation

Current falsification work has shown that aggregate means can hide a single catastrophic dimension. Strong neighboring scores can dilute a zero or extreme value and still produce a reassuring aggregate classification.

EFGM therefore now treats non-compensatory prerequisite floors, veto diagnostics, soft-min diagnostics, and independent invariant checklists as explicit research candidates rather than silently patching the frozen model.

## Governance Loop

```text
Detect entropy → Protect verified flow → Restore coherence → Reassess
```

For autonomous-agent research, the loop also tests whether governance can regain control after intervention:

```text
Observe → Detect deviation → Constrain / revoke → Clean residual state → Verify recovery
```

## Current Maturity

EFGM is currently:

- executable;
- versioned;
- evidence-traceable;
- falsification-oriented;
- benchmarked on controlled synthetic cases;
- suitable for research, critique, and controlled pilots.

It is not currently:

- externally validated;
- independently replicated;
- a production autonomous-governance engine;
- a security approval mechanism;
- a substitute for existing enterprise governance or accountable human review.

## Immediate Research Priorities

1. Maintain one unambiguous canonical v2 definition across the repository.
2. Preserve the frozen v2 baseline for comparison.
3. Test critical-dimension prerequisite and veto diagnostics without changing continuous scores prematurely.
4. Evaluate `AE` and `CUE` against simpler independent governance checks.
5. Add temporal state-transition and intervention/recovery experiments.
6. Validate inter-rater consistency and construct separation.
7. Use externally sealed holdouts only after candidates are frozen.

The current defensible positioning is:

> **EFGM is an experimental, evidence-traceable framework for studying decision integrity, entropy recovery, and governed autonomous flow.**