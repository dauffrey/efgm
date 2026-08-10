# EFGM Governance Principles

## Purpose

This document defines responsible-use and research-governance principles for the Entropy-Flow Governance Model (EFGM).

The canonical research baseline is EFGM v2. Experimental extensions, including EFGM v0.3 Governed Agentic Flow, must remain clearly identified as candidates until promoted through the research process.

EFGM should support judgment. It should not replace judgment.

---

## 1. Treat EFGM as a Governance Aid, Not a Truth or Approval Engine

EFGM scores and diagnostics are structured indicators. They do not prove that:

- an output is correct;
- a system is safe;
- a decision is compliant;
- a release is approved;
- an autonomous agent is adequately controlled;
- available evidence is complete.

A high EFGM score must not bypass required security, privacy, architecture, legal, regulatory, change-management, safety, or domain-review controls.

---

## 2. Preserve Evidence and Rationale

Every research-grade applied metric should use the executable `MetricObservation` semantics:

| Field | Purpose |
|---|---|
| `value` | Normalized value when applicable |
| `status` | Evidence/observation state |
| `rationale` | Why the observation maps to the value/state |
| `evidence_refs` | Traceable supporting evidence |
| `scorer_id` | Reviewer/model identity |
| `scorer_type` | Human, model, automated, or hybrid |
| `confidence` | Scorer confidence |

A numeric score without defensible evidence should be treated as weak research evidence even when compatibility mode can technically score it.

---

## 3. Use One Canonical Observation Vocabulary

The executable v2/v0.3 vocabulary is:

| Status | Meaning |
|---|---|
| `observed` | Directly supported by evidence |
| `inferred` | Estimated from indirect evidence or reviewer judgment |
| `unknown` | Evidence is insufficient to score the observation |
| `not_applicable` | The construct genuinely does not apply |

Do not introduce parallel status labels such as `verified` or `assumed` into canonical scoring records. Those words may appear in prose, but when evidence enters the EFGM schema it must map to the canonical observation states.

Critical distinction:

```text
0.00 != unknown
unknown != not_applicable
unknown != safe
```

---

## 4. Do Not Confuse Activity With Coherent Flow

A system may remain active, productive, or formally compliant while degrading.

Examples include:

- a release checklist is complete but rollback evidence is missing;
- an AI answer is fluent but unsupported;
- an agent successfully completes tasks outside authorized boundaries;
- an incident response is busy but repeatedly resets its causal theory;
- documentation exists but no longer matches operational reality.

EFGM should evaluate whether progress remains coherent and governed, not merely whether activity occurred.

---

## 5. Keep Decision Quality Separate From Outcome Quality

A favorable outcome does not retroactively improve decision-time evidence.

Research scoring must avoid outcome leakage:

```text
DQ != OQ
```

Decision-time metrics should use only information available at the time of the assessed decision.

---

## 6. Preserve Non-Compensatory Safety and Governance Concerns

Current counterexamples show that aggregate means can dilute a sparse catastrophic failure.

Therefore:

- aggregate scores must not be treated as sufficient proof that every critical condition is healthy;
- critical-dimension floors, veto diagnostics, soft-min diagnostics, or invariant checklists may be tested as separate candidate layers;
- those diagnostics must be preregistered by semantic role rather than invented after observing a failure;
- no candidate threshold becomes canonical without validation.

---

## 7. Separate Agency From Governance Failure

For autonomous-agent research, high privilege, connectivity, persistence, coordination, or action velocity is not automatically unsafe.

EFGM v0.3 should preserve the distinction between:

- agency amplification;
- governance integrity (`GI`);
- agency exposure (`AE`);
- coherent unsafe execution (`CUE`).

A capable agent with strong governance is not equivalent to a capable agent with weak governance.

---

## 8. Unknown Governance Evidence Is Not Safety Evidence

An unobserved boundary violation, missing trace, unknown persistence surface, or untested revocation mechanism must not be treated as evidence of integrity.

If a material observation is `unknown`, completed scoring should remain blocked according to the applicable model rules.

---

## 9. Explicit N/A Must Be Evidence-Backed

`not_applicable` should be used only when a construct genuinely does not apply.

For experimental v0.3, a whole governance family may be excluded from `GI` only where the implementation explicitly permits it and every observation in the family is marked `not_applicable` with defensible rationale and scorer provenance.

N/A must never be used to avoid measuring an inconvenient control.

---

## 10. Avoid False Precision

Small decimal differences should not be overinterpreted.

Focus on:

- evidence;
- uncertainty;
- dominant entropy/governance drivers;
- counterexamples;
- classification stability;
- recommended action;
- sensitivity to reasonable perturbation.

Versioned thresholds are research parameters, not natural constants.

---

## 11. Prefer Explainable Scoring

An EFGM result should expose enough intermediate state to explain:

- which observations were applied;
- which evidence supports them;
- which values were unknown or N/A;
- how composites were calculated;
- which drivers dominated;
- which diagnostic flags fired;
- why a recommendation or classification was produced.

Do not reduce EFGM to an opaque final number.

---

## 12. Preserve Human Accountability for Consequential Decisions

High-impact contexts require accountable human or authorized institutional review.

Examples include:

- production releases;
- security-sensitive changes;
- access-control decisions;
- autonomous-agent deployment;
- incident containment/restoration;
- regulated or privacy-impacting workflows;
- client-facing operational decisions.

EFGM may structure the evidence but does not become the accountable decision owner.

---

## 13. Falsification Comes Before Promotion

EFGM research must actively search for failure cases.

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

Real holdout case contents and preferred labels must not be visible to the autonomous tuning loop before candidate freeze.

A candidate should be frozen with:

- hypothesis and success criteria;
- code SHA;
- configuration ID/hash;
- dataset identity;
- scorer information;
- holdout access state.

Once a holdout is exposed to a tuning lineage, it is no longer unseen evidence for that lineage.

---

## 15. Reassess After Intervention

EFGM is intended to support iterative governance:

```text
Assess → Detect degradation → Intervene → Reassess
```

For autonomous agents:

```text
Observe → Detect deviation → Constrain / revoke → Clean residual state → Verify recovery → Reassess
```

A successful intervention should eventually be supported by observable state change rather than by declaration alone.

---

## 16. Use Sanitized Repository Material

Do not commit:

- credentials;
- production secrets;
- personal information;
- client-confidential material;
- restricted architecture;
- unapproved incident details;
- sensitive logs;
- real sealed-holdout contents or labels.

Prefer public, simulated, sanitized, or independently approved evidence.

---

## 17. Record Limitations

Every serious assessment or experiment should disclose material limitations, such as:

- synthetic case authorship;
- internal labels;
- single-scorer measurement;
- missing external replication;
- tuning-visible validation data;
- uncalibrated thresholds;
- domain-specific assumptions;
- known counterexamples;
- incomplete temporal evidence.

Limitations are part of the result, not an optional appendix.

---

## 18. Current Responsible-Use Principle

```text
Use EFGM to make coherence and governance degradation visible,
not to manufacture certainty or bypass accountable controls.
```

The core governance loop remains:

```text
Detect entropy → Protect verified flow → Restore coherence → Reassess
```