# Entropy-Flow Governance Model (EFGM) White Paper

## Status

**Status:** Experimental governance and measurement research framework  
**Canonical baseline:** EFGM v2 decision-integrity model (`0.2.0`, unreleased research baseline)  
**Experimental extension:** EFGM v0.3 Governed Agentic Flow  
**Purpose:** Evaluate whether AI-assisted reasoning, software-delivery decisions, operational workflows, and autonomous-agent activity remain coherent, grounded, calibrated, traceable, bounded, and recoverable under degradation pressure.

EFGM is not a proven scientific law, compliance standard, autonomous approval engine, or production-ready risk engine. It is an executable research prototype intended for controlled, falsification-oriented validation.

---

# 1. Executive Summary

The Entropy-Flow Governance Model (EFGM) is a governance and measurement framework for evaluating whether a decision process preserves useful coherent flow while facing uncertainty, contradiction, incomplete information, behavioral pressure, operational disruption, and—experimentally for autonomous agents—governance boundary pressure.

The original EFGM concept used a simple coherent-flow relationship:

```text
T × E → Et → F ± e → A|M
```

and later the v1 compatibility equation:

```text
F = (T × E × Fq) / (1 + e)
```

Those expressions remain part of EFGM's conceptual lineage, but they are **not the current canonical research model**.

The canonical EFGM v2 baseline is a decision-integrity model that separates input disorder, output degradation, positive decision-quality factors, behavioral and operational entropy, decision quality, coherence recovery, hidden information, and eventual outcome quality.

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

The central v2 research question is:

> Given the evidence available at decision time, how coherent, grounded, calibrated, traceable, and operationally reliable was the decision process?

EFGM v0.3 adds a separate experimental question for autonomous agents:

> Can high coherent task flow coexist with weak governance integrity, and can that condition be measured without treating agency itself as inherently unsafe?

---

# 2. Why EFGM Exists

Modern AI-assisted and operational workflows can remain active and apparently productive while degrading underneath. Common patterns include:

- internally coherent but unsupported AI output;
- conflicting requirements or evidence;
- confidence that is disproportionate to evidence;
- context decay across long tasks;
- repeated retries or tool failures;
- stale or fragmented operational knowledge;
- pressure to preserve a prior decision despite contrary evidence;
- autonomous execution that remains effective while moving outside governing intent.

Traditional process governance often verifies whether required steps occurred. EFGM adds a complementary question:

> Is the decision or system state coherent and governed enough to proceed responsibly?

EFGM is intended to expose the evidence and degradation drivers behind that judgment rather than produce an opaque approval score.

---

# 3. Canonical EFGM v2 Decision-Integrity Model

## 3.1 Positive factors

| Symbol | Meaning |
|---|---|
| `T` | Observation maturity / sequence continuity |
| `C` | Capability suitability for the assessed objective |
| `Fq` | Flow quality |
| `G` | Grounding |
| `U` | Uncertainty calibration |

The positive-factor composite is:

```text
Q = (T × C × Fq × G × U)^(1/5)
```

The geometric mean is a research hypothesis, not an established natural law. It is retained in the frozen v2 baseline for reproducible comparison against alternatives.

## 3.2 Input entropy

```text
Ei = w1*IC + w2*IA + w3*IG + w4*MC + w5*H
```

Input entropy describes disorder presented to the decision process:

- input contradiction (`IC`);
- input ambiguity (`IA`);
- input goal conflict (`IG`);
- missing context (`MC`);
- hidden-information load (`H`).

Input entropy does not directly penalize v2 decision quality. It provides the reference state used to measure recovery.

## 3.3 Output entropy

```text
Eo = w1*OC + w2*UM + w3*GD + w4*RI + w5*CD
```

Output entropy measures degradation introduced or retained by the decision process:

- output contradiction (`OC`);
- uncertainty mismatch (`UM`);
- goal drift (`GD`);
- reasoning instability (`RI`);
- context decay (`CD`).

## 3.4 Behavioral and operational entropy

`Be` captures behavioral distortion such as chasing behavior, outcome bias, sunk-cost pressure, false-pattern detection, and overconfidence feedback.

`Oe` captures execution degradation such as timeouts, retry instability, tool failures, latency pressure, and workflow interruption.

Whether all operational entropy belongs inside decision quality remains an explicit research question.

## 3.5 Decision quality

```text
DQ = Q / (1 + Eo + Be + Oe)
```

`DQ` is the integrity of the resulting decision under the evidence and conditions available at decision time.

## 3.6 Coherence Recovery Capacity

```text
CRC = (Ei - Eo) / max(Ei, ε)
```

`CRC` is intentionally separate from `DQ`.

- Positive `CRC` indicates entropy reduction.
- Near-zero `CRC` indicates little net recovery.
- Negative `CRC` indicates entropy amplification.

The frozen v2 ratio is not bounded to `[-1, 1]`. Bounded alternatives are research candidates and must not be silently substituted.

## 3.7 Outcome separation

EFGM explicitly rejects the assumption that a good outcome proves a good decision.

```text
Good decision != guaranteed good outcome
Bad decision != guaranteed bad outcome
```

`OQ` is outcome quality observed after the fact.

```text
OD = OQ - DQ
OutcomeConfidence = DQ × (1 - H)
```

This separation reduces outcome leakage and allows EFGM to study luck, hidden information, and possible model misspecification.

---

# 4. Evidence and Missing-Data Discipline

Every research-grade applied metric is represented as a `MetricObservation`:

```text
(value, status, rationale, evidence_refs, scorer_id, scorer_type, confidence)
```

The canonical observation states are:

| State | Meaning |
|---|---|
| `observed` | Directly supported by evidence |
| `inferred` | Estimated from indirect evidence or reviewer judgment |
| `unknown` | Evidence is insufficient to score the observation |
| `not_applicable` | The construct genuinely does not apply |

These states are not interchangeable.

```text
0.00           = measured numeric value
unknown        = no completed score may silently assume a value
not_applicable = excluded according to the model's aggregation rules
```

Research-grade runs require rationale, evidence references for applied numeric values, scorer identity/type, positive confidence, and no unresolved `unknown` values.

The core rule is:

> UNKNOWN != SAFE

---

# 5. Reproducibility and Falsification

EFGM advances through falsification-oriented research rather than confirmation-oriented tuning.

Required controls include:

- versioned scoring configurations;
- canonical input and configuration SHA-256 hashes;
- code commit SHA in experiment records;
- development and validation partitions;
- externally sealed holdout contents and labels;
- independent comparators as well as EFGM-derived ablations;
- sensitivity and perturbation testing;
- explicit counterexample retention;
- rejected-candidate retention;
- no rewriting gold labels because EFGM disagrees;
- human approval before promotion of a candidate baseline.

A candidate is not accepted because it raises EFGM scores. It must demonstrate useful behavior against independently defined evidence and simpler alternatives.

---

# 6. Known Structural Limitation: Compensatory Aggregation

Current falsification work has demonstrated that aggregate means can hide sparse catastrophic failures. A single critical grounding, flow-quality, entropy, or agent-governance observation can be diluted by strong neighboring observations.

This is a material known limitation of the current frozen equations and experimental agent aggregation.

The current research direction is therefore to compare the existing continuous scores with non-compensatory diagnostic layers such as:

- preregistered prerequisite floors;
- extreme-degradation veto diagnostics;
- soft-min or low-percentile diagnostics;
- independent invariant checklists.

No such diagnostic is canonical until it survives development, validation, independent comparison, and sealed-holdout evaluation.

---

# 7. Experimental EFGM v0.3: Governed Agentic Flow

EFGM v0.3 is not part of the frozen v2 baseline. It is an experimental extension for autonomous agents.

Its central proposition is:

> High coherent task flow can coexist with low governance integrity.

The candidate state vector is:

```text
S_t = [F_T, e_c, A, B, O, M_g, S_g, R_c, A_a]
```

Where:

- `F_T` — task/decision flow inherited from v2 `DQ`;
- `e_c` — cognitive/decision entropy summary;
- `A` — objective alignment;
- `B` — boundary integrity;
- `O` — observability;
- `M_g` — environmental-memory governance;
- `S_g` — coordination governance;
- `R_c` — control recoverability;
- `A_a` — agency amplification.

Agentic governance integrity is denoted **`GI`**, not `G`, to avoid collision with v2 Grounding (`G`).

```text
GI = geometric_mean(applicable governance families)
```

Agency amplification is not automatically unsafe. Risk depends on its interaction with governance weakness.

The experimental candidate now distinguishes:

```text
AE  = A_a × (1 - GI)
CUE = F_T × AE
```

Where:

- `AE` = Agency Exposure: consequential capacity that is insufficiently governed;
- `CUE` = Coherent Unsafe Execution: effective task flow operating through that exposure.

The historical v0.3 field `uncontrolled_agency_risk` is retained only as a compatibility alias for the `CUE` candidate during the current research cycle.

---

# 8. Temporal Governance Direction

A static score is not sufficient to characterize autonomous-agent governance.

The v0.3 research program therefore treats state transition as a first-class experimental target:

```text
S_t
 ↓ agent action / environment change
S_t+1
 ↓ governance intervention
S_t+2
 ↓
Did governance regain control?
```

Temporal experiments should evaluate conditions such as:

- authority changes issued mid-task;
- privilege revocation;
- credentials remaining cached after revocation;
- persistent environmental memory;
- peer discovery and delegation;
- incomplete state cleanup;
- rollback effectiveness;
- residual agency after containment;
- recovery latency.

These experiments are intended to turn recoverability from a static reviewer impression into increasingly observable intervention evidence.

---

# 9. Governance Loop

The EFGM governance loop remains:

```text
Detect entropy → Protect verified flow → Restore coherence → Reassess
```

For autonomous agents this expands operationally into:

```text
Observe → Detect deviation → Constrain / revoke → Clean residual state → Verify recovery → Reassess
```

The purpose is not merely to classify degradation. The purpose is to make degradation and recovery measurable enough to support intervention.

---

# 10. Scope and Claim Limits

EFGM must not be represented as:

- proof of objective truth;
- a physical law of intelligence;
- a validated incident-probability model;
- an autonomous compliance engine;
- a substitute for security, privacy, legal, architecture, safety, or regulatory review;
- a replacement for domain expertise or accountable human decision ownership.

A defensible future claim is narrower:

> Under specified tested conditions, a particular version of EFGM demonstrated reproducible measurement and/or predictive value relative to stated baselines.

Stronger claims require independent replication across datasets, scorers, domains, and research teams.

---

# 11. Current Research Priorities

1. Preserve the frozen v2 baseline for reproducible comparison.
2. Eliminate repository terminology and definition drift.
3. Test non-compensatory prerequisite and veto diagnostics against benign controls.
4. Compare `AE` and `CUE` against simpler independent agent-governance checklists.
5. Operationalize temporal state-transition and intervention/recovery experiments.
6. Measure inter-rater agreement for v2 and v0.3 observations.
7. Keep real holdout data externally sealed until candidates are frozen.
8. Test confidence propagation only as an explicit future candidate rather than silently changing scores.

---

# 12. Current Status

EFGM should currently be described as:

> An experimental, evidence-traceable governance and measurement framework for studying decision integrity, entropy recovery, and governed autonomous flow.

The canonical research baseline is EFGM v2. The autonomous-agent model is an experimental v0.3 candidate. Neither is a validated production risk engine.