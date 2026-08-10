# EFGM Governance Principles

## Purpose

This document defines responsible-use and research-governance principles for the Entropy-Flow Governance Model (EFGM).

```text
Canonical model:        EFGM v2
Python package:         0.2.0
Experimental extension: Agent Governance v0.3
```

EFGM should support judgment. It should not replace judgment.

---

## 1. Treat EFGM as a Governance Aid, Not a Truth or Approval Engine

EFGM scores and diagnostics do not prove that an output is correct, a system is safe, a decision is compliant, a release is approved, an autonomous agent is adequately controlled, or available evidence is complete.

A high EFGM score must not bypass required security, privacy, architecture, legal, regulatory, change-management, safety, or domain-review controls.

---

## 2. Preserve Evidence and Rationale

Every research-grade applied normalized metric should use `MetricObservation` semantics:

| Field | Purpose |
|---|---|
| `value` | Normalized value when applicable |
| `status` | Evidence/observation state |
| `rationale` | Why evidence maps to the value/state |
| `evidence_refs` | Traceable support |
| `scorer_id` | Reviewer/model identity |
| `scorer_type` | Human, model, automated, or hybrid |
| `confidence` | Scorer confidence |

A numeric score without defensible evidence is weak research evidence even where compatibility mode can technically score it.

---

## 3. Use One Canonical Observation Vocabulary

| Status | Meaning |
|---|---|
| `observed` | Directly supported by evidence |
| `inferred` | Estimated from indirect evidence or reviewer judgment |
| `unknown` | Evidence is insufficient to score the observation |
| `not_applicable` | The construct genuinely does not apply |

Do not introduce parallel canonical scoring states such as `verified` or `assumed`.

```text
0.00 != unknown
unknown != not_applicable
unknown != safe
```

---

## 4. Do Not Confuse Activity With Coherent Flow

A system may remain active or productive while degrading. Examples include a fluent but unsupported AI answer, a release checklist without rollback evidence, or an agent completing tasks outside authorized boundaries.

EFGM should evaluate whether progress remains coherent and governed, not merely whether activity occurred.

---

## 5. Keep Decision Quality Separate From Outcome Quality

```text
DQ != OQ
```

A favorable outcome does not retroactively improve decision-time evidence. Decision-time metrics should use only information available at the assessed decision point.

---

## 6. Preserve Non-Compensatory Concerns Without Inventing Hard Rules

Current counterexamples show that aggregate means can dilute sparse catastrophic failures.

Therefore:

- aggregate scores are not proof every critical condition is healthy;
- `governance_observation_floor` may expose a weak observation but is **not itself a prerequisite verdict**;
- low-percentile/soft-min diagnostics may be tested separately;
- only explicitly configured **candidate prerequisite metric paths** may produce candidate-prerequisite breaches;
- possible veto rules require separate preregistration and validation;
- independent invariant checklists remain required comparators;
- no candidate threshold, prerequisite set, or veto becomes canonical merely because it fixes a known counterexample.

`EFGM-EXP-0004` is intended to falsify candidate prerequisite semantics against catastrophic cases, benign low-score controls, ablations, perturbation, and an independent checklist.

---

## 7. Separate Agency From Governance Failure

For autonomous-agent research, high privilege, connectivity, persistence, coordination, or action velocity is not automatically unsafe.

Agent Governance v0.3 preserves distinctions between agency amplification, governance integrity (`GI`), agency exposure (`AE`), and coherent unsafe execution (`CUE`).

```text
AE  = A_a × (1 - GI)
CUE = F_T × AE
0 <= CUE <= AE <= 1
```

AE and CUE are related rather than orthogonal. A generic low-AE/high-CUE case is structurally impossible and must not be used as a research target.

A capable agent with strong governance is not equivalent to a capable agent with weak governance.

---

## 8. Unknown Governance Evidence Is Not Safety Evidence

An unobserved boundary violation, missing trace, unknown persistence surface, or untested revocation mechanism must not be treated as evidence of integrity.

If a material observation is `unknown`, completed scoring remains blocked according to applicable model rules.

---

## 9. Explicit N/A Must Be Evidence-Backed and Narrowly Scoped

`not_applicable` should be used only when a construct genuinely does not apply.

In the current Agent Governance implementation, **whole-family N/A is permitted only for coordination governance** in a strictly single-agent scenario. Every coordination observation must be explicitly `not_applicable` with defensible rationale and scorer provenance.

The family is excluded from `GI` rather than assumed perfect. Results expose applicable/excluded governance families and family count because cross-case comparisons may require stratification.

No other whole-family N/A semantics are currently supported.

For temporal residual-state verification, an N/A claim is stronger than ordinary omission: it is a scope assertion and therefore requires rationale, scorer identity/type, positive confidence, and evidence references before it can contribute to a verified-recovery candidate.

---

## 10. Avoid False Precision

Small decimal differences should not be overinterpreted. Focus on evidence, uncertainty, dominant drivers, counterexamples, classification stability, sensitivity to perturbation, and recommended action.

Versioned thresholds are research parameters, not natural constants.

---

## 11. Prefer Explainable Scoring

An EFGM result should expose enough intermediate state to explain which observations were applied, which values were unknown/N/A, how composites were calculated, which drivers dominated, which diagnostics fired, which governance families were applicable, and why a label was produced.

Do not reduce EFGM to an opaque final number.

---

## 12. Preserve Human Accountability for Consequential Decisions

High-impact contexts require accountable human or authorized institutional review. EFGM may structure evidence but does not become the decision owner.

---

## 13. Falsification Comes Before Promotion

Required practices include:

- frozen baseline comparison;
- simpler EFGM-derived ablations;
- genuinely independent baselines;
- controlled mutations;
- sensitivity and perturbation analysis;
- counterexample retention;
- rejected-candidate retention;
- no label rewriting to favor EFGM;
- sealed holdouts outside the tuning-visible repository;
- human approval before candidate promotion.

A more elaborate candidate is not automatically better.

---

## 14. Keep Holdouts Sealed

Real holdout case contents and preferred labels must not be visible to the tuning loop before candidate freeze.

Freeze hypothesis/success criteria, code SHA, configuration identity/hash, dataset identity, scorer information, and holdout access state before exposure.

Once a holdout is exposed to a tuning lineage, it is no longer unseen evidence for that lineage.

---

## 15. Distinguish Recovery Progress From Verified Recovery

EFGM is iterative:

```text
Assess → Detect degradation → Intervene → Reassess
```

For autonomous agents:

```text
Observe → Detect deviation → Constrain / revoke → Clean residual state → Verify recovery → Reassess
```

Temporal states must share an explicit `sequence_id` before they can be interpreted as one trajectory. Cross-sequence state comparisons are rejected rather than treated as recovery evidence. Transition results should retain candidate config identity/hash, before/after input hashes, and residual-state identity where applicable.

### Recovery progress

A same-sequence valid `pre_intervention → post_intervention` transition with a declared intervention, higher `GI`, and lower `AE`.

Recovery progress means movement in the intended direction. It is not proof control has been restored.

### Verified recovery signal

A stronger experimental signal requiring recovery progress plus:

- the post-intervention state itself is classified as governed;
- no remaining candidate-prerequisite breach;
- no elevated AE/CUE diagnostic;
- complete residual-state evidence;
- no material residual credentials, persistence, environmental memory, coordination, privileges, scheduled actions, irreversible side effects, or rollback gaps marked present.

For verified-recovery assessment, `clear`, `present`, and `not_applicable` residual claims require evidence and scorer provenance; `unknown` prevents verified recovery.

Even verified recovery is a **research signal, not a production containment attestation**.

`EFGM-EXP-0005` must actively test unrelated sequences, governance-deficient post-states, partial recovery, residual-state failure cases, and N/A misuse.

---

## 16. Separate Implementation Invariants From Scientific Validation

A unit test can prove that code obeys a formula or classification rule. It cannot establish that the construct is useful in the world.

Examples:

- monotonic classification boundary tests verify implementation consistency;
- lowering task flow while holding governance/agency fixed can verify `AE` remains unchanged and `CUE` decreases;
- `CUE <= AE` is a structural formula invariant, not evidence that either construct is useful;
- independent semantic labels are still required to determine whether `AE` and `CUE` are useful distinct constructs.

`EFGM-EXP-0006` is reserved for that semantic validation using only mathematically feasible contrasts.

---

## 17. Use Sanitized Repository Material

Do not commit credentials, production secrets, personal information, client-confidential material, restricted architecture, unapproved incident details, sensitive logs, or real sealed-holdout contents/labels.

Prefer public, simulated, sanitized, or independently approved evidence.

---

## 18. Record Limitations

Every serious assessment or experiment should disclose material limitations such as synthetic authorship, internal labels, missing external replication, uncalibrated thresholds, domain assumptions, known counterexamples, and incomplete temporal evidence.

Limitations are part of the result, not an optional appendix.

---

## 19. Current Responsible-Use Principle

```text
Use EFGM to make coherence and governance degradation visible,
not to manufacture certainty or bypass accountable controls.
```

The core governance loop remains:

```text
Detect entropy → Protect verified flow → Restore coherence → Reassess
```
