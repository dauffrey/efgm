# Metric Definitions

## Purpose

This document defines the core metrics used by the Entropy-Flow Governance Model (EFGM) to evaluate whether a system, workflow, reasoning process, or operational environment is maintaining coherent flow or degrading under entropy.

EFGM separates metrics into two major categories:

1. **Entropy metrics** — indicators of degradation, contradiction, fragmentation, uncertainty, or instability.
2. **Flow-quality metrics** — indicators of coherent execution, reasoning continuity, semantic alignment, and verification strength.

In the EFGM scoring model:

```text
F = (T × E × Fq) / (1 + e)
```

Where:

| Variable | Meaning |
|---|---|
| `F` | Coherent flow score |
| `T` | Time, sequence continuity, or iteration stability |
| `E` | Capability, tooling, infrastructure, or available execution capacity |
| `Fq` | Flow quality |
| `e` | Entropy load |

Higher entropy lowers coherent flow. Higher flow quality improves coherent flow.

---

# 1. Scoring Convention

Unless otherwise stated, all metrics should be normalized to a `0.00–1.00` scale.

## Entropy Metric Scale

For entropy metrics, higher values are worse.

| Score | Meaning |
|---:|---|
| `0.00` | No observable entropy |
| `0.25` | Low entropy; minor degradation |
| `0.50` | Moderate entropy; noticeable instability |
| `0.75` | High entropy; significant degradation |
| `1.00` | Severe entropy; system is incoherent or unreliable |

## Flow-Quality Metric Scale

For flow-quality metrics, higher values are better.

| Score | Meaning |
|---:|---|
| `0.00` | No coherent flow quality observed |
| `0.25` | Weak flow quality |
| `0.50` | Partial or inconsistent flow quality |
| `0.75` | Strong flow quality |
| `1.00` | Fully coherent, validated, and stable flow quality |

---

# 2. Entropy Metrics

Entropy metrics measure the degree to which a system is drifting away from coherent alignment.

## 2.1 Contradiction Density

| Field | Definition |
|---|---|
| Metric Name | Contradiction Density |
| Category | Entropy |
| Direction | Higher is worse |
| Definition | The proportion of claims, decisions, rules, outputs, or observations that conflict with other known claims, decisions, rules, outputs, or observations. |
| Purpose | Detects whether the system is producing or operating from incompatible information. |
| Example Signals | Conflicting requirements, inconsistent answers, incompatible technical assumptions, contradictory status reports, opposing conclusions from the same evidence. |
| Suggested Formula | `Contradiction Density = conflicting claims / total evaluated claims` |
| Score Range | `0.00–1.00` |

### Interpretation

| Score Range | Interpretation |
|---:|---|
| `0.00–0.20` | Few or no contradictions |
| `0.21–0.40` | Minor contradictions requiring clarification |
| `0.41–0.60` | Moderate contradiction load |
| `0.61–0.80` | High contradiction load |
| `0.81–1.00` | Severe incoherence |

### Example

If 5 of 50 evaluated claims conflict with other verified claims:

```text
5 / 50 = 0.10
```

Contradiction Density = `0.10`

---

## 2.2 Uncertainty Variance

| Field | Definition |
|---|---|
| Metric Name | Uncertainty Variance |
| Category | Entropy |
| Direction | Higher is worse |
| Definition | The degree to which confidence, estimates, assumptions, or forecasts fluctuate without new evidence or justified explanation. |
| Purpose | Detects unstable confidence, volatile estimates, or unreliable forecasting behaviour. |
| Example Signals | Confidence swings, unsupported forecast changes, inconsistent risk ratings, unstable root-cause assumptions, frequent reversals without new data. |
| Suggested Formula | `Uncertainty Variance = normalized variance of confidence or estimate changes over time` |
| Score Range | `0.00–1.00` |

### Interpretation

| Score Range | Interpretation |
|---:|---|
| `0.00–0.20` | Stable uncertainty level |
| `0.21–0.40` | Minor unexplained variation |
| `0.41–0.60` | Moderate instability |
| `0.61–0.80` | High instability |
| `0.81–1.00` | Severe forecast or confidence instability |

### Notes

Uncertainty is not automatically bad. A system can be uncertain and still coherent if the uncertainty is clearly explained. This metric should measure **unexplained or unstable uncertainty**, not honest uncertainty.

---

## 2.3 Memory Fragmentation

| Field | Definition |
|---|---|
| Metric Name | Memory Fragmentation |
| Category | Entropy |
| Direction | Higher is worse |
| Definition | The degree to which relevant context, history, documentation, or state is lost, duplicated, stale, disconnected, or distributed across incompatible sources. |
| Purpose | Detects whether the system has enough coherent memory to continue operating reliably. |
| Example Signals | Missing prior decisions, duplicate records, stale documentation, disconnected tickets, forgotten assumptions, conflicting source-of-truth locations. |
| Suggested Formula | `Memory Fragmentation = fragmented context items / total relevant context items` |
| Score Range | `0.00–1.00` |

### Interpretation

| Score Range | Interpretation |
|---:|---|
| `0.00–0.20` | Context is intact and traceable |
| `0.21–0.40` | Minor gaps or duplication |
| `0.41–0.60` | Moderate fragmentation |
| `0.61–0.80` | High fragmentation |
| `0.81–1.00` | Critical loss of operational memory |

### Example Evidence

- A migration plan exists in one location, but execution scripts exist elsewhere with no clear linkage.
- A support team acts on an old decision because the updated decision was only recorded in email.
- AI context omits a previous constraint and reintroduces a rejected assumption.

---

## 2.4 Recursion Instability

| Field | Definition |
|---|---|
| Metric Name | Recursion Instability |
| Category | Entropy |
| Direction | Higher is worse |
| Definition | The degree to which a system loops, repeats analysis, reopens resolved items, or fails to converge on a stable state or decision. |
| Purpose | Detects circular rework, unstable reasoning, or process non-convergence. |
| Example Signals | Repeated retries, repeated root-cause resets, circular discussions, unresolved loops, reopened decisions, failure to reach an executable conclusion. |
| Suggested Formula | `Recursion Instability = repeated or non-convergent cycles / total process cycles` |
| Score Range | `0.00–1.00` |

### Interpretation

| Score Range | Interpretation |
|---:|---|
| `0.00–0.20` | Process converges cleanly |
| `0.21–0.40` | Minor repetition |
| `0.41–0.60` | Moderate rework or looping |
| `0.61–0.80` | High failure to converge |
| `0.81–1.00` | Severe recursive instability |

### Example

A team investigates the same issue across five meetings but keeps returning to the same unresolved assumption without new evidence. This would produce a high Recursion Instability score.

---

## 2.5 Context Decay

| Field | Definition |
|---|---|
| Metric Name | Context Decay |
| Category | Entropy |
| Direction | Higher is worse |
| Definition | The degree to which earlier valid facts, constraints, assumptions, or decisions are ignored, contradicted, weakened, or omitted over time without justification. |
| Purpose | Detects whether valid context is degrading across time, handoffs, iterations, or reasoning steps. |
| Example Signals | Previously confirmed facts disappear, earlier constraints are violated, decisions are forgotten, old assumptions return, validated evidence is ignored. |
| Suggested Formula | `Context Decay = decayed context items / total previously valid context items` |
| Score Range | `0.00–1.00` |

### Interpretation

| Score Range | Interpretation |
|---:|---|
| `0.00–0.20` | Context remains preserved |
| `0.21–0.40` | Minor context weakening |
| `0.41–0.60` | Moderate context decay |
| `0.61–0.80` | High context loss |
| `0.81–1.00` | Severe loss of continuity |

### Distinction from Memory Fragmentation

Memory Fragmentation measures whether context is scattered, duplicated, or disconnected.

Context Decay measures whether valid context is forgotten, weakened, or contradicted over time.

---

# 3. Flow-Quality Metrics

Flow-quality metrics measure whether a system is moving coherently toward its intended objective.

## 3.1 Task Completion Consistency

| Field | Definition |
|---|---|
| Metric Name | Task Completion Consistency |
| Category | Flow Quality |
| Direction | Higher is better |
| Definition | The proportion of required or expected steps that are completed correctly, in sequence, and without unjustified omission. |
| Purpose | Measures execution reliability against the expected workflow or objective. |
| Example Signals | Checklist completion, deployment steps completed, required validations performed, expected artifacts produced, acceptance criteria satisfied. |
| Suggested Formula | `Task Completion Consistency = correctly completed required steps / total required steps` |
| Score Range | `0.00–1.00` |

### Interpretation

| Score Range | Interpretation |
|---:|---|
| `0.00–0.20` | Most required steps missing or failed |
| `0.21–0.40` | Weak completion |
| `0.41–0.60` | Partial completion |
| `0.61–0.80` | Mostly complete |
| `0.81–1.00` | Complete or near-complete execution |

---

## 3.2 Reasoning Continuity

| Field | Definition |
|---|---|
| Metric Name | Reasoning Continuity |
| Category | Flow Quality |
| Direction | Higher is better |
| Definition | The degree to which later reasoning steps preserve, build on, and remain consistent with earlier valid context, assumptions, evidence, and decisions. |
| Purpose | Measures whether the reasoning chain remains stable across iterations. |
| Example Signals | Earlier constraints are respected, assumptions are carried forward, conclusions follow from evidence, decisions remain traceable, no unexplained logic jumps. |
| Suggested Formula | `Reasoning Continuity = continuity-preserving reasoning steps / total reasoning steps` |
| Score Range | `0.00–1.00` |

### Interpretation

| Score Range | Interpretation |
|---:|---|
| `0.00–0.20` | Reasoning is disconnected or incoherent |
| `0.21–0.40` | Weak continuity |
| `0.41–0.60` | Partial continuity |
| `0.61–0.80` | Strong continuity |
| `0.81–1.00` | Highly coherent reasoning chain |

---

## 3.3 Semantic Coherence

| Field | Definition |
|---|---|
| Metric Name | Semantic Coherence |
| Category | Flow Quality |
| Direction | Higher is better |
| Definition | The degree to which terminology, claims, classifications, evidence, and conclusions remain meaningfully aligned within the same conceptual frame. |
| Purpose | Detects whether the system is using concepts consistently and drawing conclusions that match the stated meaning of the evidence. |
| Example Signals | Consistent terminology, stable definitions, aligned conclusions, correct use of domain language, no category confusion, no semantic drift. |
| Suggested Formula | `Semantic Coherence = semantically aligned items / total evaluated semantic items` |
| Score Range | `0.00–1.00` |

### Interpretation

| Score Range | Interpretation |
|---:|---|
| `0.00–0.20` | Meaning is incoherent or misaligned |
| `0.21–0.40` | Weak semantic alignment |
| `0.41–0.60` | Partial alignment |
| `0.61–0.80` | Strong alignment |
| `0.81–1.00` | Highly coherent semantic structure |

### Example

If a document uses “risk,” “issue,” “defect,” and “incident” interchangeably without defining the distinction, Semantic Coherence should decrease.

---

## 3.4 Verification Success Rate

| Field | Definition |
|---|---|
| Metric Name | Verification Success Rate |
| Category | Flow Quality |
| Direction | Higher is better |
| Definition | The proportion of verifiable claims, outputs, decisions, or artifacts that are successfully validated against reliable evidence, tests, source systems, or accepted criteria. |
| Purpose | Measures whether the system’s outputs can be confirmed rather than merely asserted. |
| Example Signals | Passed tests, cited evidence, successful deployment validation, reconciled data, confirmed source-of-truth checks, peer review acceptance. |
| Suggested Formula | `Verification Success Rate = successfully verified claims / total verifiable claims` |
| Score Range | `0.00–1.00` |

### Interpretation

| Score Range | Interpretation |
|---:|---|
| `0.00–0.20` | Little or no verification |
| `0.21–0.40` | Weak verification |
| `0.41–0.60` | Partial verification |
| `0.61–0.80` | Strong verification |
| `0.81–1.00` | Highly verified output |

### Notes

This metric should exclude claims that are not reasonably verifiable. The denominator should be **verifiable claims**, not all claims.

---

# 4. Optional Composite Calculations

## 4.1 Entropy Load

Entropy load may be calculated as a weighted average of entropy metrics:

```text
e = (w1 × CD) + (w2 × UV) + (w3 × MF) + (w4 × RI) + (w5 × CX)
```

Where:

| Symbol | Meaning |
|---|---|
| `CD` | Contradiction Density |
| `UV` | Uncertainty Variance |
| `MF` | Memory Fragmentation |
| `RI` | Recursion Instability |
| `CX` | Context Decay |
| `w1–w5` | Metric weights |

If no domain-specific weighting is available, use equal weights:

```text
e = (CD + UV + MF + RI + CX) / 5
```

---

## 4.2 Flow Quality

Flow quality may be calculated as a weighted average of flow-quality metrics:

```text
Fq = (w1 × TCC) + (w2 × RC) + (w3 × SC) + (w4 × VSR)
```

Where:

| Symbol | Meaning |
|---|---|
| `TCC` | Task Completion Consistency |
| `RC` | Reasoning Continuity |
| `SC` | Semantic Coherence |
| `VSR` | Verification Success Rate |
| `w1–w4` | Metric weights |

If no domain-specific weighting is available, use equal weights:

```text
Fq = (TCC + RC + SC + VSR) / 4
```

---

# 5. Suggested Default Weights

Default weights should be treated as provisional and adjusted by domain.

## Entropy Weights

| Metric | Suggested Default Weight |
|---|---:|
| Contradiction Density | `0.25` |
| Uncertainty Variance | `0.15` |
| Memory Fragmentation | `0.20` |
| Recursion Instability | `0.15` |
| Context Decay | `0.25` |

## Flow-Quality Weights

| Metric | Suggested Default Weight |
|---|---:|
| Task Completion Consistency | `0.25` |
| Reasoning Continuity | `0.25` |
| Semantic Coherence | `0.20` |
| Verification Success Rate | `0.30` |

---

# 6. Metric Collection Guidance

Metrics may be collected from different evidence sources depending on the system being evaluated.

## AI Reasoning Systems

| Metric Area | Possible Evidence |
|---|---|
| Contradiction Density | Conflicting model statements, inconsistent answers |
| Uncertainty Variance | Confidence changes across responses |
| Memory Fragmentation | Lost or duplicated context |
| Recursion Instability | Repeated failed reasoning loops |
| Context Decay | Forgotten constraints |
| Verification Success Rate | Source checks, tool results, test outcomes |

## Software Delivery

| Metric Area | Possible Evidence |
|---|---|
| Contradiction Density | Conflicting requirements, release notes, tickets |
| Memory Fragmentation | Scattered documentation, stale runbooks |
| Recursion Instability | Reopened defects, repeated failed deployments |
| Task Completion Consistency | Deployment checklist completion |
| Verification Success Rate | Test results, build status, production validation |

## Operational Governance

| Metric Area | Possible Evidence |
|---|---|
| Contradiction Density | Conflicting stakeholder direction |
| Uncertainty Variance | Unstable risk ratings |
| Memory Fragmentation | Decisions spread across email, tickets, chat, documents |
| Context Decay | Forgotten approvals or constraints |
| Semantic Coherence | Inconsistent terminology across teams |
| Verification Success Rate | Confirmed evidence, audit trails, sign-offs |

---

# 7. Interpretation Bands

The following bands may be used to interpret the final coherent flow score.

| Coherent Flow Score | Interpretation | Suggested Action |
|---:|---|---|
| `0.80–1.00` | Coherent | Proceed with normal governance |
| `0.60–0.79` | Mostly coherent | Proceed with monitoring |
| `0.40–0.59` | Degraded but usable | Reduce entropy before major decisions |
| `0.20–0.39` | Misaligned | Stabilize before proceeding |
| `0.00–0.19` | Incoherent | Stop, reassess, and restore coherence |

---

# 8. Design Principles

## 8.1 Metrics Should Be Evidence-Based

A metric score should be tied to observable evidence, not intuition alone.

## 8.2 Metrics Should Be Normalized

All metrics should be normalized to a common `0.00–1.00` range to support comparison and aggregation.

## 8.3 Metrics Should Be Explainable

Each score should include a short rationale explaining why the score was assigned.

## 8.4 Metrics Should Distinguish Unknown from Bad

Missing evidence should not automatically be scored as failure. Unknown, unavailable, or not applicable values should be explicitly marked.

Recommended labels:

| Label | Meaning |
|---|---|
| Verified | Supported by evidence |
| Inferred | Reasonable conclusion from available evidence |
| Assumed | Used as a working assumption |
| Unknown | Not enough evidence |
| Not Applicable | Metric does not apply in this context |

## 8.5 Metrics Should Support Governance Action

The purpose of scoring is not only to measure. The purpose is to decide whether to proceed, monitor, stabilize, verify, or stop.

---

# 9. Minimum Metric Record Format

Each measured metric should be recorded with the following structure:

```yaml
metric: Contradiction Density
category: Entropy
score: 0.20
direction: higher_is_worse
evidence:
  - "Two conflicting deployment dates found across release notes and email thread."
rationale: "Minor contradiction; source of truth was later confirmed."
confidence: 0.80
status: Verified
```

---

# 10. Current Limitations

These metric definitions are provisional. They should be refined through applied use against real workflows, AI reasoning traces, incident reviews, release readiness assessments, migration projects, and other operational datasets.

Known limitations include:

- Metric weighting requires calibration.
- Some metrics may overlap in complex systems.
- Human scoring may introduce subjectivity.
- Automated scoring requires reliable evidence extraction.
- Domains may require specialized indicators.
- Thresholds should be validated against actual outcomes.

---

# 11. Summary

EFGM metrics are intended to measure whether a system is maintaining coherent flow or degrading under entropy.

Entropy metrics identify degradation.

Flow-quality metrics identify coherent execution.

Together, they support a governance decision:

```text
Proceed, monitor, stabilize, verify, or stop.
```
