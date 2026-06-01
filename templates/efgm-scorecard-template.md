# EFGM Scorecard Template

## Purpose

This scorecard provides a compact structure for applying the Entropy-Flow Governance Model (EFGM) to a workflow, AI-assisted reasoning chain, release package, incident review, migration activity, operational process, or decision path.

The scorecard is intended to help reviewers capture:

- entropy signals;
- flow-quality signals;
- supporting evidence;
- calculated EFGM values;
- classification;
- recommended governance action.

EFGM should be used as a governance aid, not as a substitute for evidence, expert review, operational judgment, or formal approval processes.

---

## Assessment Metadata

| Field | Value |
|---|---|
| Assessment Name |  |
| Assessment ID |  |
| Assessment Type | AI Reasoning / Release Readiness / Incident Review / Migration / Operational Workflow / Other |
| Assessor |  |
| Date |  |
| Version |  |
| System / Workflow / Decision Reviewed |  |
| Objective |  |
| Scope |  |
| Out of Scope |  |
| Evidence Sources Reviewed |  |
| Confidence in Evidence | High / Medium / Low |

---

## EFGM Core Equation

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

## Scoring Convention

All scores should be normalized to a `0.00–1.00` scale.

### Entropy Metrics

For entropy metrics, higher values are worse.

| Score | Meaning |
|---:|---|
| `0.00` | No observable entropy |
| `0.25` | Low entropy |
| `0.50` | Moderate entropy |
| `0.75` | High entropy |
| `1.00` | Severe entropy |

### Flow-Quality Metrics

For flow-quality metrics, higher values are better.

| Score | Meaning |
|---:|---|
| `0.00` | No coherent flow quality observed |
| `0.25` | Weak flow quality |
| `0.50` | Partial or inconsistent flow quality |
| `0.75` | Strong flow quality |
| `1.00` | Fully coherent, validated, and stable flow quality |

---

## 1. Entropy Scorecard

Entropy metrics identify degradation, contradiction, uncertainty, fragmentation, instability, and context loss.

| Metric | Direction | Weight | Score | Weighted Score | Evidence | Notes |
|---|---|---:|---:|---:|---|---|
| Contradiction Density | Higher is worse | 0.25 |  |  |  |  |
| Uncertainty Variance | Higher is worse | 0.15 |  |  |  |  |
| Memory Fragmentation | Higher is worse | 0.20 |  |  |  |  |
| Recursion Instability | Higher is worse | 0.15 |  |  |  |  |
| Context Decay | Higher is worse | 0.25 |  |  |  |  |
| **Total Entropy Load (`e`)** |  | **1.00** |  |  |  |  |

### Entropy Calculation

```text
e = (w1 × CD) + (w2 × UV) + (w3 × MF) + (w4 × RI) + (w5 × CX)
```

If equal weighting is preferred:

```text
e = (CD + UV + MF + RI + CX) / 5
```

### Primary Entropy Drivers

List the strongest entropy contributors.

| Rank | Entropy Driver | Evidence | Governance Concern |
|---:|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |

---

## 2. Flow-Quality Scorecard

Flow-quality metrics identify coherent execution, stable reasoning, semantic alignment, and verification strength.

| Metric | Direction | Weight | Score | Weighted Score | Evidence | Notes |
|---|---|---:|---:|---:|---|---|
| Task Completion Consistency | Higher is better | 0.25 |  |  |  |  |
| Reasoning Continuity | Higher is better | 0.25 |  |  |  |  |
| Semantic Coherence | Higher is better | 0.20 |  |  |  |  |
| Verification Success Rate | Higher is better | 0.30 |  |  |  |  |
| **Total Flow Quality (`Fq`)** |  | **1.00** |  |  |  |  |

### Flow-Quality Calculation

```text
Fq = (w1 × TCC) + (w2 × RC) + (w3 × SC) + (w4 × VSR)
```

If equal weighting is preferred:

```text
Fq = (TCC + RC + SC + VSR) / 4
```

### Primary Flow Strengths

List the strongest coherence contributors.

| Rank | Flow Strength | Evidence | Governance Benefit |
|---:|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |

---

## 3. Core Variable Scores

| Variable | Definition | Score | Evidence / Rationale |
|---|---|---:|---|
| `T` | Time, iteration continuity, or observation maturity |  |  |
| `E` | Capability, tooling, compute, or operational capacity |  |  |
| `Fq` | Flow quality |  |  |
| `e` | Entropy load |  |  |
| `F` | Coherent flow score |  |  |

---

## 4. Final EFGM Calculation

```text
F = (T × E × Fq) / (1 + e)
```

| Component | Value |
|---|---:|
| `T` |  |
| `E` |  |
| `Fq` |  |
| `e` |  |
| `F` |  |

### Calculation Notes

```text
Insert calculation here.
```

---

## 5. Classification

| Coherent Flow Score | Classification | Interpretation | Suggested Action |
|---:|---|---|---|
| `0.80–1.00` | Coherent | Flow is strong and entropy is controlled | Proceed with normal governance |
| `0.60–0.79` | Mostly Coherent | Flow is acceptable with watch items | Proceed with monitoring |
| `0.40–0.59` | Degraded but Usable | Coherence is weakened but usable | Reduce entropy before major decisions |
| `0.20–0.39` | Misaligned | Entropy materially affects reliability | Stabilize before proceeding |
| `0.00–0.19` | Incoherent | System is not reliable enough to proceed | Stop, reassess, and restore coherence |

### Selected Classification

| Field | Value |
|---|---|
| Final Classification |  |
| Classification Rationale |  |
| Confidence in Classification | High / Medium / Low |

---

## 6. Governance Recommendation

| Decision Area | Recommendation |
|---|---|
| Proceed / Monitor / Verify / Pause / Stop |  |
| Required Corrective Actions |  |
| Verification Required Before Proceeding |  |
| Escalation Required | Yes / No |
| Escalation Target |  |
| Reassessment Required | Yes / No |
| Reassessment Trigger |  |

---

## 7. Evidence Quality

| Evidence Type | Available? | Quality | Notes |
|---|---|---|---|
| Source documents | Yes / No | High / Medium / Low |  |
| System logs | Yes / No | High / Medium / Low |  |
| Test results | Yes / No | High / Medium / Low |  |
| Human review | Yes / No | High / Medium / Low |  |
| AI-generated output | Yes / No | High / Medium / Low |  |
| Operational records | Yes / No | High / Medium / Low |  |
| Decision records | Yes / No | High / Medium / Low |  |

---

## 8. Assumption Register

| Assumption | Status | Evidence | Risk if Wrong | Owner |
|---|---|---|---|---|
|  | Verified / Inferred / Assumed / Unknown / Not Applicable |  |  |  |
|  | Verified / Inferred / Assumed / Unknown / Not Applicable |  |  |  |
|  | Verified / Inferred / Assumed / Unknown / Not Applicable |  |  |  |

---

## 9. Issues and Follow-Up Actions

| Action ID | Action | Owner | Priority | Due Date | Status |
|---|---|---|---|---|---|
| 1 |  |  | High / Medium / Low |  | Open / In Progress / Closed |
| 2 |  |  | High / Medium / Low |  | Open / In Progress / Closed |
| 3 |  |  | High / Medium / Low |  | Open / In Progress / Closed |

---

## 10. Reviewer Notes

```text
Add reviewer notes here.
```

---

## 11. Summary

| Summary Field | Value |
|---|---|
| Overall Result |  |
| Main Entropy Drivers |  |
| Main Flow Strengths |  |
| Final Recommendation |  |
| Reassessment Needed | Yes / No |

