# EFGM Governance Principles

## Purpose

This document defines the governance principles for applying the **Entropy-Flow Governance Model (EFGM)** responsibly.

EFGM is intended to help reviewers identify when a system, workflow, decision path, AI-assisted output, or operational process is maintaining coherent flow or degrading under entropy. These principles are intended to prevent misuse, overclaiming, false precision, and inappropriate reliance on the score alone.

EFGM should support judgment. It should not replace judgment.

---

## 1. Treat EFGM as a Governance Aid, Not an Absolute Truth Engine

EFGM scores should be interpreted as structured indicators, not definitive proof.

A score can help answer:

> Is this system, workflow, or reasoning chain coherent enough to proceed?

A score should not be treated as proof that:

- the output is correct;
- the system is safe;
- the decision is risk-free;
- the evidence is complete;
- the process no longer requires human review.

EFGM provides a coherence signal. It does not determine objective truth by itself.

---

## 2. Preserve Evidence and Rationale

Every EFGM assessment should record the evidence behind the score.

Each metric score should include:

- the observed signal;
- the evidence source;
- the rationale for the score;
- the confidence level;
- any assumptions or unknowns.

A score without evidence should be treated as weak or provisional.

### Minimum Evidence Standard

| Field | Description |
|---|---|
| Metric | The EFGM metric being scored |
| Score | Normalized value, usually `0.00–1.00` |
| Evidence | Observable reason for the score |
| Rationale | Explanation of how the evidence maps to the score |
| Confidence | Reviewer confidence in the score |
| Status | Verified, Inferred, Assumed, Unknown, or Not Applicable |

---

## 3. Distinguish Verified, Inferred, Assumed, Unknown, and Not Applicable

EFGM assessments should clearly separate evidence states.

| Label | Meaning |
|---|---|
| Verified | Supported by direct evidence |
| Inferred | Reasonable conclusion from available evidence |
| Assumed | Used as a working assumption, but not verified |
| Unknown | Evidence is missing, incomplete, or unavailable |
| Not Applicable | Metric does not apply to the assessment context |

This distinction is critical because uncertainty should not be hidden inside a numeric score.

Unknown evidence should not automatically be treated as failure. However, significant unknowns may increase entropy if they materially affect the decision.

---

## 4. Do Not Confuse Activity with Coherent Flow

A system may appear active, productive, or formally compliant while becoming less coherent.

Examples include:

- a release checklist is complete, but rollback has not been verified;
- an AI answer is fluent, but unsupported by evidence;
- an incident response is busy, but investigation theories keep changing;
- a migration plan exists, but source and target assumptions conflict;
- documentation exists, but no longer matches operational reality.

EFGM should help reviewers evaluate whether work is not only moving, but moving coherently toward a validated objective.

---

## 5. Use Conservative Interpretation When Entropy Is High

When entropy indicators are high, recommendations should become more conservative.

High entropy may indicate:

- contradiction;
- uncertainty;
- fragmented context;
- stale assumptions;
- verification gaps;
- recurring instability;
- operational drift;
- hidden dependencies.

In these cases, the preferred governance response is usually:

```text
Pause → Verify → Restore coherence → Reassess
```

High entropy should not be ignored simply because capability, tooling, or execution velocity appears strong.

---

## 6. Use EFGM to Support Decisions, Not Replace Accountability

EFGM can help structure a recommendation, but it should not remove decision accountability.

The responsible owner, reviewer, architect, release manager, incident lead, or governance authority remains accountable for the final decision.

EFGM should clarify:

- what is known;
- what is uncertain;
- what is contradictory;
- what requires verification;
- what action is recommended.

It should not obscure who owns the decision.

---

## 7. Avoid False Precision

EFGM uses numeric scoring, but the model is currently heuristic and investigational.

Scores should be interpreted as approximate governance indicators, not exact measurements.

For example, the difference between `0.62` and `0.64` should not be overinterpreted. The classification band and supporting evidence usually matter more than small numeric differences.

Recommended practice:

- use decimals consistently;
- avoid excessive precision;
- explain scoring rationale;
- focus on entropy drivers and governance actions.

---

## 8. Calibrate Weights by Domain

Default metric weights should be treated as provisional.

Different domains may require different weighting.

| Domain | Likely Higher-Weight Metrics |
|---|---|
| AI reasoning review | Contradiction Density, Context Decay, Verification Success Rate |
| Release readiness | Verification Success Rate, Environment Inconsistency, Recovery Integrity |
| Incident response | Reasoning Continuity, Memory Fragmentation, Recursion Instability |
| Migration planning | Hidden Dependencies, Environment Inconsistency, Operational Traceability |
| Documentation review | Context Decay, Memory Fragmentation, Semantic Coherence |

Weights should be reviewed and adjusted based on evidence, expert judgment, and observed outcomes.

---

## 9. Prefer Explainable Scoring Over Black-Box Scoring

EFGM should remain explainable.

A reviewer should be able to understand:

- why each score was assigned;
- which evidence contributed to the score;
- which entropy drivers mattered most;
- which flow-quality indicators remained strong;
- why the final recommendation was produced.

If an automated EFGM engine is created, it should expose intermediate scoring logic and not only produce a final score.

---

## 10. Do Not Use EFGM Where Evidence Cannot Be Reasonably Assessed

EFGM is not appropriate for every situation.

It should be avoided or used cautiously when:

- evidence is unavailable;
- the evaluator lacks domain understanding;
- the metric definitions cannot be applied consistently;
- the decision requires specialized legal, medical, financial, safety, or regulatory authority;
- the scoring would create a false sense of certainty;
- the work is simple enough that EFGM would add unnecessary overhead.

EFGM is most useful where coherence, uncertainty, evidence, and operational alignment materially affect the decision.

---

## 11. Preserve Human Review for High-Impact Decisions

For high-impact decisions, EFGM should trigger or support human review rather than replace it.

High-impact contexts may include:

- production releases;
- security-relevant changes;
- client-facing decisions;
- incident restoration decisions;
- AI-generated recommendations used for operational action;
- migrations or upgrades with material service impact;
- decisions involving sensitive, confidential, or regulated information.

When impact is high and entropy is non-trivial, escalation should be preferred over automated approval.

---

## 12. Use Sanitized Examples for Repository Documentation

Repository examples should avoid sensitive or confidential information.

Do not include:

- credentials;
- production secrets;
- private client data;
- confidential architecture details;
- personal information;
- restricted government or enterprise material;
- real incident details unless sanitized and approved.

Use synthetic, generalized, or sanitized examples wherever possible.

---

## 13. Maintain Clear Boundaries With Existing Governance

EFGM should complement existing governance frameworks. It should not be positioned as a replacement for:

- enterprise risk management;
- architecture review;
- security review;
- privacy assessment;
- change management;
- compliance review;
- quality assurance;
- incident management;
- release management;
- human expert judgment.

EFGM adds a coherence-and-entropy lens. Existing governance remains necessary.

---

## 14. Make Governance Actions Explicit

An EFGM assessment should end with an explicit recommended action.

Recommended action categories:

| Action | Meaning |
|---|---|
| Proceed | Coherence is strong enough to continue |
| Proceed with Monitoring | Flow is acceptable, but some entropy drivers should be watched |
| Verify | Additional evidence is needed before relying on the result |
| Stabilize | Entropy must be reduced before major action |
| Pause | The system is not coherent enough to proceed safely |
| Escalate | Human or specialized review is required |
| Stop | The output, workflow, or decision path is materially incoherent |

The recommendation should be supported by the score, evidence, and reviewer rationale.

---

## 15. Reassess After Coherence-Restoration Actions

EFGM should support iterative governance.

If an assessment recommends verification, stabilization, or escalation, the system should be reassessed after corrective action.

Example loop:

```text
Initial Assessment → Entropy Identified → Corrective Action → Reassessment → Decision
```

This prevents EFGM from becoming a one-time scoring exercise and reinforces the core governance loop:

```text
Detect Entropy → Protect Flow → Restore Coherence
```

---

## 16. Record Limitations and Unknowns

Every assessment should include a limitations section.

Examples:

- evidence was incomplete;
- only one reviewer scored the assessment;
- no independent verification was performed;
- scoring weights were default values;
- the scenario was synthetic;
- some claims were not verifiable;
- the assessment was time-limited.

Limitations do not invalidate the assessment, but they should affect confidence.

---

## 17. Use EFGM as an Early-Warning Framework

EFGM is strongest when used to detect coherence degradation before failure.

It should help teams identify patterns such as:

- increasing contradiction;
- declining verification;
- growing uncertainty;
- process drift;
- context fragmentation;
- repeated rework;
- hidden dependency exposure;
- unstable decision confidence.

The goal is not only to classify the current state. The goal is to intervene before incoherence becomes failure.

---

## 18. Review and Improve the Model Over Time

EFGM should be treated as a developing framework.

The principles, metrics, thresholds, and weights should be revised as more examples are tested.

Recommended review triggers:

- after each pilot assessment;
- after reviewer feedback;
- after false positives or false negatives are identified;
- after new use cases are added;
- after the scoring engine changes;
- after the model is compared to real outcomes.

---

## Summary

EFGM should be used carefully, transparently, and conservatively.

The model is intended to help reviewers identify when coherent flow is weakening under entropy pressure. Its value depends on evidence-based scoring, explainable rationale, calibrated interpretation, and responsible human oversight.

The core responsible-use principle is:

> Use EFGM to make coherence degradation visible, not to create false certainty.
