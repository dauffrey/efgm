# Entropy-Flow Governance Model (EFGM) White Paper

## Status

**Status:** Experimental governance and measurement research framework  
**Canonical model:** EFGM v2 — Decision Integrity  
**Python package:** `0.2.0` — unreleased research package  
**Experimental extension:** Agent Governance v0.3  
**Purpose:** Evaluate whether AI-assisted reasoning, software-delivery decisions, operational workflows, and autonomous-agent activity remain coherent, grounded, calibrated, traceable, bounded, and recoverable under degradation pressure.

EFGM is not a proven scientific law, compliance standard, autonomous approval engine, or production-ready risk engine. It is an executable research prototype intended for controlled, falsification-oriented validation.

---

# 1. Executive Summary

The Entropy-Flow Governance Model (EFGM) is a governance and measurement framework for evaluating whether a decision process preserves useful coherent flow while facing uncertainty, contradiction, incomplete information, behavioral pressure, and operational disruption.

The original EFGM concept used:

```text
T × E → Et → F ± e → A|M
```

and later the v1 compatibility equation:

```text
F = (T × E × Fq) / (1 + e)
```

Those expressions remain part of EFGM's conceptual lineage, but they are **not the current canonical research model**.

The canonical EFGM v2 baseline is a decision-integrity model:

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

The central EFGM v2 research question is:

> Given the evidence available at decision time, how coherent, grounded, calibrated, traceable, and operationally reliable was the decision process?

Agent Governance v0.3 adds a separate experimental question for autonomous agents:

> Can high coherent task flow coexist with weak governance integrity, and can that condition be measured without treating agency itself as inherently unsafe?

---

# 2. Why EFGM Exists

Modern AI-assisted and operational workflows can remain active and apparently productive while degrading underneath. Examples include:

- internally coherent but unsupported AI output;
- conflicting requirements or evidence;
- confidence disproportionate to evidence;
- context decay across long tasks;
- repeated retries or tool failures;
- stale or fragmented operational knowledge;
- pressure to preserve a prior decision despite contrary evidence;
- autonomous execution that remains effective while moving outside governing intent.

EFGM adds a complementary governance question:

> Is the decision or system state coherent and governed enough to proceed responsibly?

EFGM is intended to expose evidence and degradation drivers rather than produce an opaque approval score.

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

```text
Q = (T × C × Fq × G × U)^(1/5)
```

The geometric mean is a research hypothesis retained in the frozen EFGM v2 baseline for reproducible comparison.

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

Input entropy does not directly penalize `DQ`; it provides the reference state used to measure recovery.

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

The frozen v2 ratio is not bounded to `[-1, 1]`. Bounded alternatives remain research candidates.

## 3.7 Outcome separation

```text
Good decision != guaranteed good outcome
Bad decision != guaranteed bad outcome
```

`OQ` is outcome quality observed after the fact.

```text
OD = OQ - DQ
OutcomeConfidence = DQ × (1 - H)
```

This separation reduces outcome leakage and allows study of luck, hidden information, and model misspecification.

---

# 4. Evidence and Missing-Data Discipline

Every research-grade applied normalized metric uses `MetricObservation`:

```text
(value, status, rationale, evidence_refs, scorer_id, scorer_type, confidence)
```

Canonical states are:

| State | Meaning |
|---|---|
| `observed` | Directly supported by evidence |
| `inferred` | Estimated from indirect evidence or reviewer judgment |
| `unknown` | Evidence is insufficient to score the observation |
| `not_applicable` | The construct genuinely does not apply |

```text
0.00           = measured numeric value
unknown        = no completed score may silently assume a value
not_applicable = excluded only according to explicit model aggregation rules
```

The core rule is:

> UNKNOWN != SAFE

---

# 5. Reproducibility and Falsification

EFGM advances through falsification-oriented research rather than confirmation-oriented tuning.

Required controls include:

- versioned scoring configurations;
- input and configuration SHA-256 hashes;
- code commit SHA in experiment records;
- development and validation partitions;
- externally sealed holdout contents and labels;
- independent comparators and EFGM-derived ablations;
- sensitivity and perturbation testing;
- explicit counterexample retention;
- rejected-candidate retention;
- no rewriting gold labels because EFGM disagrees;
- human approval before promotion.

A candidate must demonstrate useful behavior against independently defined evidence and simpler alternatives.

---

# 6. Known Structural Limitation: Compensatory Aggregation

Falsification work has shown that aggregate means can hide sparse catastrophic failures. A single critical observation can be diluted by strong neighbors.

This is a material known limitation of the current frozen equations and experimental Agent Governance aggregation.

The current research direction compares continuous scores with distinct non-compensatory diagnostics:

- a **neutral observation floor**;
- low-percentile or soft-min diagnostics;
- explicit versioned **candidate prerequisite sets**;
- possible future veto diagnostics;
- independent invariant checklists.

The observation floor is **not itself a prerequisite verdict**. Only metric paths explicitly configured as candidate prerequisites can produce a candidate-prerequisite breach.

The current candidate prerequisite list and threshold are research hypotheses. `EFGM-EXP-0004` is designed to test whether they reduce false reassurance without creating unacceptable false alarms or merely encoding authored labels.

No candidate prerequisite or veto is canonical.

---

# 7. Experimental Extension: Agent Governance v0.3

Agent Governance v0.3 is not part of the frozen EFGM v2 baseline.

Its central proposition is:

> High coherent task flow can coexist with low governance integrity.

The state vector is:

```text
S_t = [F_T, e_c, A, B, O, M_g, S_g, R_c, A_a]
```

Where:

- `F_T` — task/decision flow inherited from EFGM v2 `DQ`;
- `e_c` — cognitive/decision entropy summary;
- `A` — objective alignment;
- `B` — boundary integrity;
- `O` — observability;
- `M_g` — environmental-memory governance;
- `S_g` — coordination governance;
- `R_c` — control recoverability;
- `A_a` — agency amplification.

## 7.1 Symbol discipline

```text
G  = EFGM v2 Grounding
GI = Agent Governance v0.3 Governance Integrity
```

```text
GI = geometric_mean(applicable governance families)
```

A strictly single-agent scenario may mark the **entire coordination-governance family** `not_applicable`. That family is excluded from `GI` rather than assumed perfect. Results expose applicable/excluded family names and family count because cross-case comparison may require stratification.

No other whole-family N/A semantics are currently implemented.

## 7.2 Agency Exposure and Coherent Unsafe Execution

```text
AE  = A_a × (1 - GI)
CUE = F_T × AE
0 <= CUE <= AE <= 1
```

- `AE` = Agency Exposure: consequential agency insufficiently governed;
- `CUE` = Coherent Unsafe Execution: effective task flow operating through that exposure.

Because normalized `F_T` cannot exceed one, AE and CUE are structurally related rather than orthogonal. A generic low-AE/high-CUE state is mathematically impossible.

`uncontrolled_agency_risk` is retained as a compatibility alias for `CUE` during the current research cycle.

The agent benchmark treats `AE` and `CUE` as explicit **lower-is-better** comparators. It records candidate config identity/hash and code SHA.

A construct-separation diagnostic lowers task-flow maturity while holding governance and agency inputs fixed. The expected implementation behavior is:

```text
AE remains unchanged
CUE decreases
```

That verifies the algebraic implementation contract only. `EFGM-EXP-0006` is reserved for semantic validation using independently authored, mathematically feasible exposure-versus-execution contrasts.

## 7.3 Candidate classification

The current classifier uses exhaustive candidate regions:

1. elevated `AE` or `CUE` → `Elevated uncontrolled-agency risk`;
2. otherwise `GI` determines governed versus governance-deficit state;
3. task flow determines high-flow versus low-flow substate.

This removes the prior gap where a modest improvement in `GI` could produce a worse classification.

Current labels are:

- `Governed autonomous operation`;
- `Governed but low-flow`;
- `High-flow governance deficit`;
- `Low-flow governance deficit`;
- `Elevated uncontrolled-agency risk`.

These remain experimental descriptive labels, not calibrated incident probabilities.

---

# 8. Temporal Governance and Recovery

A static score is insufficient to characterize autonomous-agent governance.

```text
S_t
 ↓ agent action / environment change
S_t+1
 ↓ governance intervention
S_t+2
 ↓
Did governance regain control?
```

Every temporal state carries an explicit `sequence_id`. States from different sequences are rejected rather than interpreted as one recovery trajectory. Transition results retain candidate config identity/hash, before/after input hashes, and a residual-state hash when residual evidence is supplied.

The temporal scaffold distinguishes two signals.

## 8.1 Recovery progress

`recovery_progress_signal` requires:

- the same explicit sequence identity;
- a valid `pre_intervention → post_intervention` transition;
- a declared intervention;
- higher `GI`;
- lower `AE`.

This indicates movement in the intended direction. It is not a recovery attestation.

## 8.2 Verified recovery signal

`verified_recovery_signal` additionally requires:

- the post-intervention state itself is classified as governed;
- no candidate-prerequisite breach after intervention;
- no elevated AE/CUE diagnostic;
- complete residual-state evidence;
- no material residual state marked present.

Residual-state surfaces currently include:

- credentials;
- persistence;
- environmental memory;
- coordination;
- privileges;
- scheduled actions;
- irreversible side effects;
- rollback gaps.

For verified-recovery assessment, `clear`, `present`, and `not_applicable` residual claims require rationale, scorer identity/type, positive confidence, and evidence references. `unknown` prevents verified recovery. `not_applicable` is an evidence-backed scope claim, not an evidence-free escape hatch.

Even `verified_recovery_signal` is an experimental research signal, **not** a production containment attestation.

`EFGM-EXP-0005` is designed to falsify this logic using unrelated-sequence attempts, governance-deficient post-states, partial interventions, cached credentials, persistence/memory surviving containment, delegated peer goals, rollback gaps, trace loss, N/A misuse, and delayed containment.

---

# 9. Governance Loop

```text
Detect entropy → Protect verified flow → Restore coherence → Reassess
```

For autonomous agents:

```text
Observe → Detect deviation → Constrain / revoke → Clean residual state → Verify recovery → Reassess
```

The purpose is not merely to classify degradation. It is to make degradation and recovery measurable enough to support accountable intervention.

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

1. Preserve the frozen EFGM v2 baseline.
2. Keep repository terminology/version identity coherent.
3. Run `EFGM-EXP-0004` on neutral floors, candidate prerequisites, benign controls, and independent invariants.
4. Run `EFGM-EXP-0005` on sequence identity, intervention, residual-state evidence, and verified recovery.
5. Run `EFGM-EXP-0006` on independently authored AE-versus-CUE semantic labels within the structural constraint `CUE <= AE`.
6. Measure inter-rater agreement for EFGM v2 and Agent Governance observations.
7. Keep real holdout data externally sealed until candidates are frozen.
8. Test confidence propagation only as an explicit future candidate.

---

# 12. Current Status

```text
Canonical model:        EFGM v2 — experimental research baseline
Python package:         0.2.0 — unreleased research package
Experimental extension: Agent Governance v0.3 — research candidate
```

Neither EFGM v2 nor Agent Governance v0.3 is a validated production risk engine.
