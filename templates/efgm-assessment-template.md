# EFGM Assessment Template

## Purpose

This template provides a repeatable structure for applying the **Entropy-Flow Governance Model (EFGM)** to an AI output, software change, release package, incident response, operational workflow, migration activity, or decision-support scenario.

The goal is to determine whether the assessed system or workflow is maintaining coherent flow, accumulating entropy, or requiring governance intervention before proceeding.

Use this template to support structured review, not to replace human judgment, technical validation, risk review, or formal governance processes.

---

# 1. Assessment Summary

| Field | Value |
|---|---|
| Assessment ID |  |
| Assessment Name |  |
| Assessment Type | AI reasoning / Code review / Release readiness / Incident review / Migration / Operational workflow / Other |
| Date |  |
| Reviewer(s) |  |
| System / Workflow / Artifact Assessed |  |
| Business / Operational Context |  |
| Assessment Status | Draft / In Review / Final |

---

# 2. Objective

## 2.1 Assessment Objective

Describe what this assessment is intended to determine.

```text
Example: Determine whether the release package is coherent enough to proceed to deployment.
```

## 2.2 Decision Question

State the primary governance question.

```text
Example: Is the current system, workflow, decision, or output coherent enough to proceed?
```

## 2.3 Intended Outcome

| Outcome Type | Description |
|---|---|
| Proceed |  |
| Proceed with Monitoring |  |
| Verify Before Proceeding |  |
| Pause and Correct |  |
| Stop / Escalate |  |

---

# 3. Scope

## 3.1 Included in Scope

List what is included in the assessment.

- 
- 
- 

## 3.2 Excluded from Scope

List what is not covered by this assessment.

- 
- 
- 

## 3.3 Assumptions

List the assumptions used during the assessment.

| Assumption | Status | Notes |
|---|---|---|
|  | Verified / Inferred / Assumed / Unknown |  |
|  | Verified / Inferred / Assumed / Unknown |  |

## 3.4 Constraints

List known constraints affecting the assessment.

- 
- 
- 

---

# 4. Evidence Reviewed

## 4.1 Evidence Sources

| Evidence Source | Type | Status | Notes |
|---|---|---|---|
|  | Document / Ticket / Code / Test Result / Log / Email / Meeting Notes / Other | Verified / Partial / Missing / Unknown |  |
|  | Document / Ticket / Code / Test Result / Log / Email / Meeting Notes / Other | Verified / Partial / Missing / Unknown |  |

## 4.2 Evidence Quality

| Quality Indicator | Rating | Notes |
|---|---:|---|
| Completeness | 0.00–1.00 |  |
| Currency | 0.00–1.00 |  |
| Traceability | 0.00–1.00 |  |
| Reliability | 0.00–1.00 |  |

## 4.3 Evidence Gaps

List missing, incomplete, contradictory, or stale evidence.

- 
- 
- 

---

# 5. EFGM Scoring Inputs

The current operational EFGM equation is:

```text
F = (T × E × Fq) / (1 + e)
```

Where:

| Variable | Meaning |
|---|---|
| `F` | Coherent flow score |
| `T` | Time, iteration continuity, or observation maturity |
| `E` | Capability, tooling, compute, or operational capacity |
| `Fq` | Flow quality |
| `e` | Entropy load |

---

# 6. Time / Continuity Score

## 6.1 T — Time, Iteration Continuity, or Observation Maturity

| Field | Value |
|---|---:|
| Score | 0.00–1.00 |
| Confidence | 0.00–1.00 |

## 6.2 Rationale

Explain why this score was assigned.

```text

```

## 6.3 Evidence

- 
- 
- 

---

# 7. Capability / Capacity Score

## 7.1 E — Capability, Tooling, Compute, or Operational Capacity

| Field | Value |
|---|---:|
| Score | 0.00–1.00 |
| Confidence | 0.00–1.00 |

## 7.2 Rationale

Explain why this score was assigned.

```text

```

## 7.3 Evidence

- 
- 
- 

---

# 8. Entropy Assessment

Entropy metrics measure degradation, contradiction, uncertainty, fragmentation, instability, or context loss.

Higher entropy scores are worse.

## 8.1 Entropy Metric Scores

| Metric | Score | Weight | Weighted Score | Evidence | Notes |
|---|---:|---:|---:|---|---|
| Contradiction Density |  |  |  |  |  |
| Uncertainty Variance |  |  |  |  |  |
| Memory Fragmentation |  |  |  |  |  |
| Recursion Instability |  |  |  |  |  |
| Context Decay |  |  |  |  |  |

## 8.2 Optional Additional Entropy Indicators

Use these if relevant to the assessment.

| Metric | Score | Weight | Weighted Score | Evidence | Notes |
|---|---:|---:|---:|---|---|
| Duplicated Logic |  |  |  |  |  |
| Operational Drift |  |  |  |  |  |
| Stale Assumptions |  |  |  |  |  |
| Hidden Dependencies |  |  |  |  |  |
| Environment Inconsistency |  |  |  |  |  |

## 8.3 Entropy Load Calculation

```text
e = (weighted entropy scores) / (total entropy weights)
```

| Field | Value |
|---|---:|
| Entropy Load `e` |  |
| Confidence |  |

## 8.4 Primary Entropy Drivers

List the highest entropy contributors.

1. 
2. 
3. 

## 8.5 Entropy Rationale

```text

```

---

# 9. Flow-Quality Assessment

Flow-quality metrics measure whether the system is making coherent, traceable, stable progress toward the intended objective.

Higher flow-quality scores are better.

## 9.1 Flow-Quality Metric Scores

| Metric | Score | Weight | Weighted Score | Evidence | Notes |
|---|---:|---:|---:|---|---|
| Task Completion Consistency |  |  |  |  |  |
| Reasoning Continuity |  |  |  |  |  |
| Semantic Coherence |  |  |  |  |  |
| Verification Success Rate |  |  |  |  |  |

## 9.2 Optional Additional Flow-Quality Indicators

Use these if relevant to the assessment.

| Metric | Score | Weight | Weighted Score | Evidence | Notes |
|---|---:|---:|---:|---|---|
| Operational Traceability |  |  |  |  |  |
| Deployment Predictability |  |  |  |  |  |
| Observability |  |  |  |  |  |
| Recovery Integrity |  |  |  |  |  |

## 9.3 Flow-Quality Calculation

```text
Fq = (weighted flow-quality scores) / (total flow-quality weights)
```

| Field | Value |
|---|---:|
| Flow Quality `Fq` |  |
| Confidence |  |

## 9.4 Strongest Flow Contributors

List the strongest contributors to coherent flow.

1. 
2. 
3. 

## 9.5 Flow-Quality Rationale

```text

```

---

# 10. Coherent Flow Calculation

## 10.1 Input Summary

| Variable | Score | Notes |
|---|---:|---|
| `T` |  |  |
| `E` |  |  |
| `Fq` |  |  |
| `e` |  |  |

## 10.2 Calculation

```text
F = (T × E × Fq) / (1 + e)
```

```text
F = (___ × ___ × ___) / (1 + ___)
F = ___
```

## 10.3 Result

| Field | Value |
|---|---:|
| Coherent Flow Score `F` |  |
| Confidence |  |

---

# 11. Classification

Use the scoring bands below unless a domain-specific threshold has been defined.

| Coherent Flow Score | Classification | Interpretation | Suggested Action |
|---:|---|---|---|
| `0.80–1.00` | Coherent | Flow is strong and entropy is controlled | Proceed with normal governance |
| `0.60–0.79` | Mostly Coherent | Flow is acceptable with watch items | Proceed with monitoring |
| `0.40–0.59` | Degraded but Usable | Coherence exists but entropy is material | Verify assumptions and reduce entropy |
| `0.20–0.39` | Misaligned | Entropy is materially degrading reliability | Pause and stabilize before proceeding |
| `0.00–0.19` | Incoherent | Current state is not reliable enough to use | Stop, reassess, and restore coherence |

## 11.1 Assigned Classification

| Field | Value |
|---|---|
| Classification |  |
| Suggested Action |  |

## 11.2 Classification Rationale

```text

```

---

# 12. Governance Recommendation

## 12.1 Recommended Action

Select one.

- [ ] Proceed
- [ ] Proceed with monitoring
- [ ] Verify before proceeding
- [ ] Pause and correct
- [ ] Stop and escalate

## 12.2 Recommendation Summary

```text

```

## 12.3 Required Corrections Before Proceeding

| Correction | Owner | Priority | Due Date | Status |
|---|---|---|---|---|
|  |  | High / Medium / Low |  | Open / In Progress / Complete |
|  |  | High / Medium / Low |  | Open / In Progress / Complete |

## 12.4 Verification Required

| Verification Item | Evidence Needed | Owner | Status |
|---|---|---|---|
|  |  |  | Open / In Progress / Complete |
|  |  |  | Open / In Progress / Complete |

---

# 13. Risk and Limitation Notes

## 13.1 Known Risks

- 
- 
- 

## 13.2 Assessment Limitations

- 
- 
- 

## 13.3 Unknowns

- 
- 
- 

---

# 14. Reviewer Notes

## 14.1 Reviewer Observations

```text

```

## 14.2 Disagreements or Alternate Interpretations

```text

```

## 14.3 Follow-Up Questions

- 
- 
- 

---

# 15. Final Assessment Statement

Provide a concise final statement suitable for summary reporting.

```text
Based on the available evidence, this assessment indicates that the system/workflow/output is [classification]. The primary entropy drivers are [drivers]. The strongest flow-quality contributors are [contributors]. The recommended governance action is [action].
```

---

# 16. Assessment Metadata

| Field | Value |
|---|---|
| Created By |  |
| Created Date |  |
| Last Updated By |  |
| Last Updated Date |  |
| Version |  |
| Related Documents |  |
| Related Issues / Tickets |  |

---

# 17. Appendix: Status Labels

Use the following labels when documenting evidence, assumptions, and findings.

| Label | Meaning |
|---|---|
| Verified | Supported by direct evidence |
| Inferred | Reasonable conclusion from available evidence |
| Assumed | Working assumption used for assessment |
| Unknown | Evidence unavailable or insufficient |
| Not Applicable | Metric or item does not apply to this assessment |

---

# 18. Appendix: Scoring Guidance

## 18.1 Entropy Metrics

Higher is worse.

| Score | Meaning |
|---:|---|
| `0.00` | No observable entropy |
| `0.25` | Low entropy |
| `0.50` | Moderate entropy |
| `0.75` | High entropy |
| `1.00` | Severe entropy |

## 18.2 Flow-Quality Metrics

Higher is better.

| Score | Meaning |
|---:|---|
| `0.00` | No coherent flow quality observed |
| `0.25` | Weak flow quality |
| `0.50` | Partial or inconsistent flow quality |
| `0.75` | Strong flow quality |
| `1.00` | Fully coherent, validated, and stable flow quality |
