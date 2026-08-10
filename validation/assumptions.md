# EFGM Assumptions

## Purpose

This document records working assumptions behind the **canonical EFGM v2 decision-integrity baseline** and the **experimental Agent Governance v0.3 extension**.

```text
Canonical model:        EFGM v2
Python package:         0.2.0
Experimental extension: Agent Governance v0.3
```

These are hypotheses to test, not facts to defend. If an assumption fails under controlled evidence, EFGM should be simplified, revised, or rejected accordingly.

The historical v1 equation:

```text
F = (T × E × Fq) / (1 + e)
```

belongs to the legacy coherent-flow model and is not the current canonical operational equation. Historical v1 material is preserved under `docs/legacy/`.

---

# 1. Canonical EFGM v2 Model Assumptions

## A-001 — Decision Integrity Can Be Assessed From Observable Evidence

EFGM assumes that a decision process can be characterized well enough to support governance analysis using observable evidence about sequence continuity, capability suitability, flow quality, grounding, uncertainty calibration, input/output degradation, behavioral pressure, and operational disruption.

**Status:** Unvalidated  
**Primary test:** inter-rater agreement, construct validity, predictive comparison.

## A-002 — Input and Output Entropy Are Distinguishable

EFGM assumes the disorder presented to a decision process (`Ei`) can be distinguished from degradation introduced or retained by the process (`Eo`).

```text
CRC = (Ei - Eo) / max(Ei, ε)
```

**Status:** Unvalidated  
**Primary test:** controlled input/output mutation cases and scorer agreement.

## A-003 — Decision Quality and Outcome Quality Are Different Constructs

```text
DQ != OQ
OD = OQ - DQ
```

A decision should be evaluated using information available at decision time rather than judged only by eventual outcome.

**Status:** Required research principle; empirical usefulness still unvalidated.

## A-004 — Flow Quality, Grounding, and Calibration Are Distinguishable

- `Fq` measures coherent progression;
- `G` measures evidentiary/rule grounding;
- `U` measures confidence calibration.

**Status:** Unvalidated  
**Primary test:** blinded scorer agreement and construct-selective mutations.

## A-005 — Behavioral Entropy Adds Information

Decision distortion from chasing behavior, outcome bias, sunk-cost pressure, false-pattern detection, or overconfidence feedback may add value beyond grounding and calibration alone.

**Status:** Unvalidated  
**Primary test:** ablation and independent-label comparison.

## A-006 — Operational Entropy May Affect Decision Reliability

The frozen EFGM v2 model currently penalizes `DQ` for tool failures, retries, timeouts, latency pressure, and workflow interruptions. This placement remains an explicit open question.

**Status:** Open.

## A-007 — The Geometric Positive-Factor Composite Is Useful

```text
Q = (T × C × Fq × G × U)^(1/5)
```

This is a frozen baseline hypothesis, not a claim that geometric aggregation is scientifically necessary.

**Status:** Provisional.

## A-008 — Additive Entropy Penalties Are a Useful Baseline

```text
DQ = Q / (1 + Eo + Be + Oe)
```

This is a reproducible hypothesis, not an established law.

**Status:** Provisional.

## A-009 — Missing Evidence Must Not Become a Favorable Number

```text
observed
inferred
unknown
not_applicable
```

```text
unknown != 0.00
unknown != safe
not_applicable != unknown
```

**Status:** Required governance invariant.

## A-010 — Evidence Provenance Improves Research Quality

Recording rationale, evidence references, scorer identity/type, and confidence improves auditability and supports analysis of disagreement. Whether the additional burden improves predictive validity remains empirical.

**Status:** Required for research-grade runs; incremental benefit unvalidated.

## A-011 — Classification Bands Can Add Governance Value

Provisional labels may improve actionability, but current thresholds are not assumed calibrated across domains.

**Status:** Unvalidated.

## A-012 — Some Dimensions May Be Non-Compensatory

Retained counterexamples demonstrate that family means can dilute sparse catastrophic failures. Non-compensatory mechanisms are therefore legitimate candidates to test, but no particular prerequisite set, veto set, or threshold is assumed validated.

Candidate mechanisms include:

- neutral observation floors;
- explicit candidate prerequisite sets;
- extreme-degradation veto diagnostics;
- soft-min / low-percentile diagnostics;
- independent invariant checklists.

**Status:** Supported research need; implementation details unvalidated.

---

# 2. Experimental Agent Governance v0.3 Assumptions

## AG-001 — High Task Flow Can Coexist With Weak Governance

An autonomous agent may remain effective at task execution while moving outside authorized objectives, boundaries, observability, memory controls, coordination controls, or recoverability expectations.

**Status:** Supported by controlled synthetic construct tests; not externally validated.

## AG-002 — Governance Integrity Is Distinct From EFGM v2 Grounding

```text
G  = EFGM v2 Grounding
GI = Agent Governance v0.3 Governance Integrity
```

Governance families are objective alignment, boundary integrity, observability, environmental-memory governance, coordination governance, and control recoverability.

**Status:** Candidate construct architecture.

## AG-003 — Agency Amplification Is Not Automatically Unsafe

High privilege, connectivity, persistence, coordination, or action velocity can be legitimate and well governed.

**Status:** Required design principle for current Agent Governance research.

## AG-004 — Agency Exposure and Coherent Unsafe Execution Are Different

```text
AE  = A_a × (1 - GI)
CUE = F_T × AE
```

`AE` represents insufficiently governed consequential agency; `CUE` represents effective task execution operating through that exposure. Neither is a calibrated incident probability.

The current benchmark can verify the implementation relationship, but independent labels are still required to establish whether the constructs are semantically useful.

**Status:** Candidate hypothesis requiring comparison.

## AG-005 — External Writable/Readable State Can Function as Memory

Any surface an agent can write now and read later may function as environmental memory even if it is not labeled as a memory subsystem.

**Status:** Candidate operational principle requiring external testing.

## AG-006 — Unknown Governance Evidence Is Not Safety Evidence

An unobserved boundary violation, unmeasured trace gap, or unknown persistence surface must not be treated as proof of integrity.

**Status:** Required governance invariant.

## AG-007 — Whole-Family N/A Is Currently Permitted Only for Coordination Governance

A strictly single-agent scenario may genuinely have no multi-agent coordination surface. In that case, every coordination-governance observation may be explicitly `not_applicable`, and the coordination family is excluded from `GI` rather than assumed perfect.

The result must expose applicable/excluded families and family count because `GI` values with different applicability profiles may require stratified comparison.

**No other governance family currently has whole-family N/A semantics.** Any future expansion of N/A semantics requires a separate explicit model change and validation.

**Status:** Candidate Agent Governance v0.3 semantics.

## AG-008 — Static Snapshots Are Insufficient for Autonomous Governance

```text
S_t → action/environment change → S_t+1 → intervention → S_t+2
```

Temporal research must evaluate changes rather than final static state alone.

**Status:** Research direction; predictive temporal model not established.

## AG-009 — Recoverability Should Become Increasingly Observable

Control recoverability should be supported by intervention evidence such as revocation effectiveness, containment effectiveness, residual credential/capability state, cleanup completeness, rollback effectiveness, and recovery latency.

**Status:** Candidate measurement direction.

## AG-010 — Observation Floors Are Diagnostics, Not Automatic Prerequisites

`governance_observation_floor` is the minimum applicable governance observation. It is reported to expose sparse weak dimensions, but a low value does not by itself create a hard prerequisite failure.

Only metric paths explicitly listed as **candidate prerequisites** in the versioned Agent Governance configuration can generate a candidate-prerequisite breach.

The current candidate prerequisite list and threshold are preregistered research hypotheses. `EFGM-EXP-0004` must test whether they reduce false reassurance without creating unacceptable false alarms or merely encoding authored labels.

**Status:** Candidate non-compensatory semantics; unvalidated.

## AG-011 — Recovery Progress Is Not Verified Recovery

A valid `pre_intervention → post_intervention` state with higher `GI` and lower `AE` indicates **recovery progress** only.

A stronger experimental `verified_recovery_signal` additionally requires:

- no remaining candidate-prerequisite breach;
- no elevated AE/CUE diagnostic;
- complete residual-state evidence;
- no material residual credentials, persistence, memory, coordination, privileges, scheduled actions, irreversible side effects, or rollback gaps marked present.

Even this signal is not a production containment attestation.

**Status:** Candidate temporal semantics; requires falsification under `EFGM-EXP-0005`.

## AG-012 — Candidate Classification Should Be Monotonic in Its Intended Directions

With other state held constant, improving `GI` should not move a case from a governance-deficit label into a more severe elevated-risk label. The current classifier therefore uses exhaustive regions based on elevated AE/CUE, governed-versus-deficit GI, and high-versus-low task flow.

**Status:** Required implementation invariant for the current candidate classifier; empirical usefulness of the labels remains unvalidated.

---

# 3. Measurement Assumptions

## M-001 — Normalized Scores Can Be Applied Consistently Enough to Test

Base observations use a normalized `[0,1]` scale when applicable.

**Status:** Unvalidated.

## M-002 — Human Judgment Will Remain Necessary During Early Validation

Some constructs require domain interpretation. Rationale and disagreement should be retained as validation data.

**Status:** Expected.

## M-003 — Reviewer Confidence Should Not Yet Be Silently Folded Into Scores

Confidence is recorded but not mathematically propagated in the frozen baseline or current Agent Governance candidate. Uncertainty intervals or Monte Carlo treatments remain future explicit experiments.

**Status:** Deferred.

## M-004 — Domain-Specific Weights May Help or Overfit

Domain-specific configurations must be versioned and validated against independent evidence.

**Status:** Open question.

---

# 4. Governance and Scientific Assumptions

## G-001 — EFGM Supports Judgment; It Does Not Replace Accountability

Scores and diagnostics are decision-support signals. Accountable domain owners remain responsible for consequential decisions.

## G-002 — EFGM Must Compete With Simpler Alternatives

A more elaborate candidate should not be promoted if a simpler independent checklist provides equivalent or better useful performance.

## G-003 — Holdouts Must Remain Outside the Tuning Loop

Real holdout contents and labels must remain externally sealed until candidate and success criteria are frozen.

## G-004 — Counterexamples Are Assets

Material failures, false reassurance, regressions, and rejected candidates must be retained.

## G-005 — Internal Synthetic Success Is Not External Validation

Controlled synthetic cases can test responsiveness and invariants but cannot establish external predictive validity.

## G-006 — EFGM May Fail to Add Enough Value

Retiring or simplifying a construct is a valid successful research outcome.

---

# 5. Assumption Register

| ID | Assumption | Status | Primary Validation |
|---|---|---|---|
| A-001 | Decision integrity can be assessed from observable evidence | Unvalidated | Inter-rater + predictive tests |
| A-002 | `Ei` and `Eo` are distinguishable | Unvalidated | Controlled mutations |
| A-003 | `DQ` and `OQ` should remain separate | Research principle | Outcome-divergence studies |
| A-004 | `Fq`, `G`, `U` are distinct | Unvalidated | Construct validity |
| A-005 | Behavioral entropy adds value | Unvalidated | Ablation |
| A-006 | Operational entropy belongs partly in `DQ` | Open | Execution-reliability comparison |
| A-007 | Geometric aggregation adds value | Provisional | Simpler-baseline comparison |
| A-008 | Additive entropy penalties are useful | Provisional | Alternative aggregation tests |
| A-009 | Unknown must not default favorable | Required | Invariant tests |
| A-010 | Provenance improves research quality | Required / benefit unvalidated | Inter-rater + predictive tests |
| A-011 | Classification bands add value | Unvalidated | False reassurance/alarm tests |
| A-012 | Non-compensatory diagnostics deserve testing | Supported research need | Sparse-failure benchmark |
| AG-001 | High flow can coexist with weak governance | Synthetic support | External agent cases |
| AG-002 | `GI` is distinct from v2 `G` | Candidate construct | Construct validity |
| AG-003 | Agency itself is not automatically unsafe | Design principle | Comparative cases |
| AG-004 | `AE` and `CUE` should be separated | Candidate | Independent semantic labels |
| AG-007 | Whole-family N/A currently applies only to coordination | Candidate semantics | N/A + stratification tests |
| AG-010 | Observation floor is distinct from candidate prerequisites | Candidate semantics | EXP-0004 |
| AG-011 | Recovery progress is distinct from verified recovery | Candidate semantics | EXP-0005 |
| AG-012 | Candidate classifier should be monotonic | Implementation invariant | Boundary/adversarial tests |
| M-003 | Confidence propagation should remain explicit research | Deferred | Uncertainty experiments |

---

# 6. Review Rule

The purpose of this register is not to protect EFGM's assumptions. It is to make them easy to falsify.

A question is not resolved because a preferred narrative sounds plausible. It is resolved only to the extent supported by reproducible evidence.
