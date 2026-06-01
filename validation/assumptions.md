# EFGM Assumptions

## Purpose

This document identifies the working assumptions behind the Entropy-Flow Governance Model (EFGM).

The purpose of this file is to make the model’s underlying assumptions explicit so they can be reviewed, challenged, refined, validated, or rejected during testing.

EFGM should be treated as an early-stage governance framework and prototype scoring concept. The assumptions in this document are not proven facts. They are starting points for structured investigation.

---

## 1. Foundational Assumptions

### 1.1 Coherence Can Be Assessed

EFGM assumes that the coherence of a system, workflow, reasoning chain, or decision path can be assessed using observable signals.

In this context, coherence means that the system’s current state remains aligned with:

- the intended objective;
- verified evidence;
- known constraints;
- traceable decisions;
- current operating conditions;
- validated assumptions;
- expected process flow.

This does not mean coherence can be measured perfectly. It means coherence may be assessed well enough to support governance decisions.

### 1.2 Entropy Can Be Observed Through Degradation Signals

EFGM assumes that entropy is not directly observed as a physical quantity in this model. Instead, entropy is inferred from practical degradation signals such as:

- contradiction;
- uncertainty instability;
- memory fragmentation;
- recursion instability;
- context decay;
- duplicated logic;
- operational drift;
- stale assumptions;
- hidden dependencies;
- environment inconsistency.

These indicators are treated as observable proxies for coherence degradation.

### 1.3 Coherent Flow Weakens as Entropy Accumulates

EFGM assumes that increasing entropy reduces the reliability of coherent flow.

This is represented operationally as:

```text
F = (T × E × Fq) / (1 + e)
```

Where higher entropy load `e` reduces the coherent flow score `F`.

This relationship is provisional and should be tested against practical examples.

### 1.4 Capability Alone Is Not Sufficient

EFGM assumes that high capability, tooling, compute, automation, or expertise does not guarantee coherent outcomes.

A capable system can still degrade if it is affected by:

- contradictory inputs;
- fragmented context;
- weak verification;
- poor traceability;
- stale assumptions;
- unstable decision logic.

This assumption is central to EFGM because the model distinguishes between capability and coherent flow.

### 1.5 Activity Is Not the Same as Coherent Progress

EFGM assumes that a system may remain active, productive, or technically functional while its understanding, decision path, or workflow becomes less coherent.

Examples include:

- a team completing tasks while working from conflicting assumptions;
- an AI system producing fluent output with weak verification;
- a release checklist being completed while rollback readiness is unclear;
- an incident response generating updates without converging on cause.

EFGM is intended to help identify this difference.

---

## 2. Measurement Assumptions

### 2.1 Metrics Can Be Normalized

EFGM assumes that entropy and flow-quality indicators can be normalized to a common `0.00–1.00` scale.

This allows multiple indicators to be compared and aggregated.

However, normalization rules may differ by use case. A release readiness assessment, incident review, and AI reasoning review may require different scoring guidance.

### 2.2 Metrics May Require Human Judgment

EFGM assumes that some scoring will require human interpretation, especially during early validation.

Examples include:

- deciding whether two claims are truly contradictory;
- determining whether uncertainty is justified;
- assessing whether reasoning continuity was preserved;
- determining whether documentation is stale;
- evaluating whether a workflow has drifted.

The model should therefore capture both the score and the rationale behind the score.

### 2.3 Evidence Quality Affects Score Confidence

EFGM assumes that the quality of available evidence affects the reliability of the final assessment.

A score based on verified artifacts should carry more confidence than a score based on assumptions or incomplete information.

Each assessment should distinguish between:

| Evidence Status | Meaning |
|---|---|
| Verified | Supported by reliable evidence |
| Inferred | Reasonably concluded from available evidence |
| Assumed | Used as a working assumption |
| Unknown | Not enough evidence available |
| Not Applicable | Metric does not apply in the current context |

### 2.4 Unknown Should Not Automatically Mean Bad

EFGM assumes that missing evidence should not always be scored as failure.

Unknown values should be explicitly marked as unknown unless the absence of evidence itself creates operational risk.

For example:

- If rollback evidence is missing before a production release, that may increase entropy.
- If a metric does not apply to a simple documentation review, it should be marked not applicable.

### 2.5 Metric Weighting Is Context-Dependent

EFGM assumes that different domains may require different metric weights.

For example:

| Use Case | Metrics That May Need Higher Weight |
|---|---|
| AI reasoning review | Verification Success Rate, Contradiction Density, Context Decay |
| Release readiness | Verification Success Rate, Environment Inconsistency, Recovery Integrity |
| Incident response | Reasoning Continuity, Memory Fragmentation, Recursion Instability |
| Documentation review | Context Decay, Memory Fragmentation, Semantic Coherence |
| Migration planning | Hidden Dependencies, Environment Inconsistency, Operational Traceability |

Default weights should be treated as provisional until calibrated.

---

## 3. Model Assumptions

### 3.1 The Operational Equation Is Heuristic

EFGM assumes the current operational equation is a useful governance heuristic, not a proven mathematical law.

```text
F = (T × E × Fq) / (1 + e)
```

The equation is intended to support structured reasoning and comparative assessment. It should not be treated as a precise physical, statistical, or predictive equation without further validation.

### 3.2 Entropy and Flow Quality Are Distinct but Related

EFGM assumes that entropy and flow quality are separate dimensions that interact.

- Entropy measures degradation pressure.
- Flow quality measures coherent execution and reasoning strength.

A system may have high flow quality and still be at risk if entropy is increasing. Likewise, a system may have low entropy but still perform poorly if flow quality is weak.

### 3.3 Flow and Entropy May Form a Feedback Loop

EFGM assumes that flow and entropy may influence each other over time.

```text
F ↔ e
```

This means:

- entropy can weaken coherent flow;
- sustained work, complexity, or workload can create new entropy;
- governance activity may be required to restore coherence.

This supports the governance loop:

```text
Detect Entropy → Protect Flow → Restore Coherence
```

### 3.4 Linear Weighting Is a Starting Point

EFGM currently assumes weighted averages are a practical starting point for calculating entropy and flow quality.

Example entropy expression:

```text
e = w1CD + w2UV + w3MF + w4RI + w5CX
```

Example flow-quality expression:

```text
Fq = w1TC + w2RC + w3SC + w4VS
```

This may later need refinement into nonlinear, threshold-based, or domain-specific scoring.

---

## 4. Governance Assumptions

### 4.1 EFGM Supports Decisions but Does Not Replace Judgment

EFGM assumes that scores should support governance decisions, not replace expert judgment.

The model can help structure the decision environment, but final decisions should still consider:

- domain expertise;
- business risk;
- operational context;
- legal, security, privacy, and compliance requirements;
- stakeholder judgment;
- human accountability.

### 4.2 The Score Is Not Absolute Truth

EFGM assumes that the coherent flow score is an indicator, not a fact.

A score should always be accompanied by:

- evidence;
- rationale;
- assumptions;
- confidence level;
- known limitations;
- recommended governance action.

### 4.3 High Entropy Should Trigger Intervention

EFGM assumes that high entropy should result in governance action.

Possible actions include:

- verify assumptions;
- reconcile contradictions;
- repair documentation;
- split complex work into smaller units;
- improve observability;
- add tests or validation;
- pause release or deployment;
- escalate to human review;
- rebuild the assessment from verified evidence.

### 4.4 Proceed / Pause / Stop Decisions Require Context

EFGM assumes that score bands can guide action but should not be applied mechanically.

For example, a score of `0.55` may be acceptable for exploratory analysis but unacceptable for a production release.

Governance thresholds should be calibrated by domain, risk level, and consequence of failure.

---

## 5. Implementation Assumptions

### 5.1 EFGM Can Be Implemented as a Lightweight Tool

EFGM assumes that the scoring model can be implemented as a lightweight tool, checklist, or scorecard before becoming a larger platform.

Possible implementation forms include:

- Markdown assessment templates;
- JSON-based scoring input;
- command-line scoring tool;
- GitHub Copilot review overlay;
- release readiness scorecard;
- incident review worksheet;
- AI output review checklist.

### 5.2 Inputs Must Be Traceable

EFGM assumes that useful scoring requires traceable inputs.

Each score should connect back to evidence such as:

- documents;
- tickets;
- logs;
- tests;
- source code;
- deployment artifacts;
- meeting decisions;
- AI reasoning traces;
- reviewer notes.

If the evidence cannot be traced, the confidence of the score should decrease.

### 5.3 Automated Scoring Requires Reliable Extraction

EFGM assumes that automated or semi-automated scoring will require reliable extraction of signals from source material.

Examples include:

- identifying claims;
- detecting contradictions;
- comparing requirements to implementation;
- checking test evidence;
- detecting stale documentation;
- mapping dependencies;
- identifying repeated rework cycles.

Until extraction is reliable, human review should remain part of the scoring process.

---

## 6. Adoption Assumptions

### 6.1 The Model Must Be Understandable Without Excessive Explanation

EFGM assumes that practical adoption depends on clear language.

Reviewers should be able to understand:

- what entropy means in operational terms;
- what coherent flow means;
- how scores are calculated;
- why the recommendation was produced;
- what action should follow.

If the model requires excessive explanation, it may need to be simplified.

### 6.2 The Model Must Add Value Beyond Existing Checklists

EFGM assumes that it should only be used where it adds value beyond existing governance processes.

It should not be applied to every task.

It is best suited to situations involving:

- uncertainty;
- conflicting evidence;
- complex dependencies;
- AI-assisted reasoning;
- release readiness;
- incident response;
- migration planning;
- operational drift;
- fragmented documentation.

### 6.3 The Model Should Avoid False Precision

EFGM assumes that numerical scoring can be useful but may also create false confidence.

To reduce this risk, each score should include:

- evidence;
- rationale;
- confidence;
- uncertainty notes;
- recommended action.

The score should not stand alone.

---

## 7. Risk Assumptions

### 7.1 EFGM Could Be Misused as a Compliance Score

EFGM assumes there is a risk that users may treat the score as a compliance result or approval mechanism.

This should be avoided.

EFGM is a coherence-governance aid. It does not replace formal compliance, architecture, security, privacy, legal, or change-management approvals.

### 7.2 EFGM Could Overweight What Is Easy to Measure

EFGM assumes there is a risk that measurable signals may be overweighted while important qualitative factors are missed.

For example, test pass rates may be easy to measure, while stakeholder misunderstanding or hidden dependency risk may be harder to quantify.

The model should preserve qualitative reviewer notes.

### 7.3 EFGM Could Become Too Complex

EFGM assumes that adding too many metrics, submetrics, and weights may reduce usability.

The model should remain lightweight enough to support decision-making without becoming a burden.

### 7.4 EFGM Could Be Applied Outside Its Useful Scope

EFGM assumes it may not be useful for:

- simple binary tasks;
- low-risk work;
- highly regulated decisions requiring formal certification;
- situations without evidence;
- contexts where scoring would add overhead without improving decision quality.

---

## 8. Assumption Review Table

| ID | Assumption | Status | Validation Method |
|---|---|---|---|
| A-001 | Coherence can be assessed using observable signals | Unvalidated | Scenario testing and reviewer comparison |
| A-002 | Entropy can be inferred from degradation indicators | Unvalidated | Apply metrics to known degraded workflows |
| A-003 | Higher entropy reduces coherent flow | Unvalidated | Compare scores against expert judgment |
| A-004 | Flow quality can be measured separately from entropy | Unvalidated | Metric calibration and reviewer feedback |
| A-005 | Weighted averages are sufficient for early scoring | Provisional | Test against alternate scoring methods |
| A-006 | Different domains require different weights | Likely | Compare AI, release, incident, and migration scenarios |
| A-007 | EFGM adds value beyond checklists | Unvalidated | Controlled pilot comparison |
| A-008 | Human scoring can be made consistent enough to be useful | Unvalidated | Inter-reviewer scoring comparison |
| A-009 | Automated scoring requires reliable evidence extraction | Likely | Prototype testing |
| A-010 | Scores should support, not replace, governance judgment | Required | Governance principles review |

---

## 9. Review Questions

Reviewers should challenge the assumptions using questions such as:

1. Are the core assumptions understandable?
2. Are any assumptions too broad or too strong?
3. Which assumptions are most critical to validate first?
4. Which assumptions could create false confidence?
5. Are entropy and flow quality sufficiently distinct?
6. Can the proposed metrics be scored consistently?
7. Are the scoring bands appropriate for different use cases?
8. What evidence would prove the model useful?
9. What evidence would show that the model should be simplified or retired?
10. Which assumptions should be moved into formal validation criteria?

---

## 10. Summary

EFGM depends on several important assumptions:

- coherence can be assessed;
- entropy can be observed through degradation signals;
- entropy weakens coherent flow;
- flow quality can be measured;
- scores can support governance decisions;
- human review remains necessary;
- weights and thresholds require calibration;
- the model must avoid false precision and overreach.

These assumptions should remain visible throughout the repository.

The goal is not to defend the assumptions. The goal is to test them.
