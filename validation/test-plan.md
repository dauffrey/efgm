# EFGM Validation Test Plan

## Purpose

This document defines a practical test plan for validating the **Entropy-Flow Governance Model (EFGM)**.

The purpose of validation is not to prove that EFGM is a final mathematical theory or production-grade governance engine. The purpose is to determine whether EFGM provides useful, repeatable, and explainable insight when applied to real or simulated AI-assisted reasoning, software delivery, release readiness, incident response, and operational governance scenarios.

EFGM should advance only if testing shows that it helps reviewers identify coherence degradation, entropy accumulation, and decision-readiness issues more clearly than informal review alone.

---

## 1. Validation Objectives

The validation effort should determine whether EFGM is:

| Objective | Description |
|---|---|
| Understandable | Reviewers can understand the model, variables, metrics, and governance loop without excessive explanation. |
| Operationally useful | The model helps identify practical degradation, uncertainty, contradiction, or drift. |
| Repeatable | Different reviewers can apply the scoring method and reach reasonably similar conclusions. |
| Explainable | Scores can be traced back to observed evidence and stated rationale. |
| Actionable | The model produces useful governance recommendations such as proceed, monitor, verify, pause, or stop. |
| Appropriately limited | The model does not create false precision or imply certainty beyond available evidence. |

---

## 2. Core Validation Questions

Validation should answer the following questions:

1. Does EFGM help identify when a system, workflow, or reasoning chain is losing coherence?
2. Are the entropy metrics observable and distinguishable?
3. Are the flow-quality metrics practical and useful?
4. Can reviewers score the same scenario consistently?
5. Do EFGM results align with expert judgment?
6. Does the final classification support useful governance decisions?
7. Are the current scoring bands appropriate?
8. Does the model add value beyond a normal checklist, review meeting, or status report?
9. Where does the model overreach, underperform, or create ambiguity?
10. Should EFGM continue as a conceptual framework, assessment template, scoring tool, or be retired?

---

## 3. Validation Scope

### In Scope

The initial validation should include controlled examples from the following areas:

| Area | Example Scenario |
|---|---|
| AI reasoning governance | Review an AI-generated answer for coherence, contradiction, and verification strength. |
| AI-assisted software development | Review a Copilot-style code recommendation or pull request. |
| Release readiness | Assess whether a release package is coherent enough to proceed. |
| Incident response | Review an incident timeline and determine whether the response converged or fragmented. |
| Documentation governance | Assess whether a runbook, procedure, or knowledge article still reflects operational reality. |
| Migration planning | Review whether a migration plan remains aligned across application, database, infrastructure, security, and operational layers. |

### Out of Scope

The initial validation should not attempt to:

- prove EFGM as a scientific law;
- use EFGM as a formal compliance standard;
- replace architecture, security, privacy, or change-management review;
- score live production incidents without human oversight;
- make automated go/no-go decisions without reviewer approval;
- evaluate sensitive client data without sanitization and approval.

---

## 4. Validation Principles

The following principles should guide validation:

1. **Evidence first** — every score should be supported by observable evidence.
2. **Rationale required** — every score should include a short explanation.
3. **Unknown is not automatically failure** — missing evidence should be marked explicitly as unknown.
4. **Human judgment remains final** — EFGM supports review; it does not replace expert decision-making.
5. **Avoid false precision** — scores should be treated as governance indicators, not exact measurements.
6. **Use sanitized examples** — do not include confidential, sensitive, or restricted operational data.
7. **Compare against expert review** — EFGM should be evaluated against practical human judgment.

---

## 5. Test Scenarios

## 5.1 Scenario A: AI Reasoning Review

### Objective

Determine whether EFGM can identify coherence degradation in an AI-generated response or reasoning chain.

### Test Input

A prompt, AI-generated response, and any available supporting evidence.

### Evaluation Focus

| Metric Area | What to Look For |
|---|---|
| Contradiction Density | Does the answer conflict with itself or known facts? |
| Uncertainty Variance | Does confidence shift without evidence? |
| Context Decay | Does the response ignore earlier valid constraints? |
| Reasoning Continuity | Does the conclusion follow from the evidence? |
| Verification Success Rate | Are verifiable claims supported by reliable sources or tests? |

### Expected Output

- entropy metric scores;
- flow-quality metric scores;
- coherent flow score;
- classification;
- governance recommendation;
- reviewer rationale.

---

## 5.2 Scenario B: AI-Assisted Code Review

### Objective

Determine whether EFGM can help identify entropy introduced by AI-generated or AI-assisted code changes.

### Test Input

A sanitized code change, pull request, or Copilot-style suggestion.

### Evaluation Focus

| Metric Area | What to Look For |
|---|---|
| Duplicated Logic | Does the change repeat existing logic inconsistently? |
| Semantic Coherence | Does the implementation align with naming, architecture, and domain meaning? |
| Hidden Dependencies | Does the change rely on unstated assumptions or services? |
| Verification Success Rate | Are tests, build results, or review evidence available? |
| Operational Traceability | Can the change be traced to a requirement, defect, or objective? |

### Expected Output

- review scorecard;
- entropy drivers;
- required follow-up validation;
- recommendation to accept, revise, test further, or reject.

---

## 5.3 Scenario C: Release Readiness Assessment

### Objective

Determine whether EFGM can assess whether a release is coherent enough to proceed.

### Test Input

A sanitized release package, checklist, deployment notes, test evidence, known issues, and rollback plan.

### Evaluation Focus

| Metric Area | What to Look For |
|---|---|
| Task Completion Consistency | Are required release steps complete? |
| Verification Success Rate | Is test and deployment evidence available? |
| Environment Inconsistency | Are there differences between test, acceptance, and production assumptions? |
| Stale Assumptions | Are dependencies or approvals outdated? |
| Recovery Integrity | Is rollback or recovery verified? |

### Expected Output

- release coherence score;
- entropy risk summary;
- proceed / monitor / verify / pause / stop recommendation;
- list of blockers or watch items.

---

## 5.4 Scenario D: Incident Response Review

### Objective

Determine whether EFGM can identify whether an incident response converged toward verified understanding or fragmented under entropy.

### Test Input

A sanitized incident timeline, notes, alerts, communications, actions taken, and resolution summary.

### Evaluation Focus

| Metric Area | What to Look For |
|---|---|
| Contradiction Density | Were there competing or conflicting theories? |
| Memory Fragmentation | Were facts scattered across logs, chats, tickets, or emails? |
| Recursion Instability | Did the team repeat failed actions or reopen resolved theories? |
| Context Decay | Were key timeline facts lost or ignored? |
| Recovery Integrity | Was service restoration stable and understood? |

### Expected Output

- response coherence assessment;
- entropy drivers;
- recommended process improvements;
- lessons learned for future response.

---

## 5.5 Scenario E: Documentation Coherence Review

### Objective

Determine whether EFGM can detect documentation entropy in a runbook, support guide, procedure, or knowledge article.

### Test Input

A document and available evidence of current system behavior.

### Evaluation Focus

| Metric Area | What to Look For |
|---|---|
| Context Decay | Does the document omit or contradict current facts? |
| Memory Fragmentation | Is related information scattered across multiple unlinked sources? |
| Contradiction Density | Do instructions conflict internally or externally? |
| Verification Success Rate | Can the instructions be validated? |
| Semantic Coherence | Are terms used consistently? |

### Expected Output

- document coherence score;
- required updates;
- retired assumptions;
- recommended source-of-truth changes.

---

## 5.6 Scenario F: Migration Planning Review

### Objective

Determine whether EFGM can assess coherence across a complex migration or upgrade path.

### Test Input

A sanitized migration plan, environment inventory, dependency list, validation checklist, deployment sequence, and rollback approach.

### Evaluation Focus

| Metric Area | What to Look For |
|---|---|
| Environment Inconsistency | Are source and target environments aligned? |
| Hidden Dependencies | Are integrations, roles, jobs, scripts, and infrastructure dependencies visible? |
| Task Completion Consistency | Are migration steps complete and sequenced? |
| Verification Success Rate | Are validation checks defined and executable? |
| Operational Traceability | Can each migration action be linked to evidence or requirement? |

### Expected Output

- migration coherence score;
- entropy drivers;
- unresolved assumptions;
- readiness recommendation.

---

## 6. Scoring Method

The validation should use the current EFGM operational equation:

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

All metric values should be normalized to a `0.00–1.00` scale.

---

## 7. Entropy Metric Scoring

Entropy metrics use the convention: **higher is worse**.

| Score | Meaning |
|---:|---|
| `0.00` | No observable entropy |
| `0.25` | Low entropy |
| `0.50` | Moderate entropy |
| `0.75` | High entropy |
| `1.00` | Severe entropy |

Core entropy metrics:

| Metric | Description |
|---|---|
| Contradiction Density | Conflicting claims relative to total claims. |
| Uncertainty Variance | Instability in confidence, estimates, or forecasts over time. |
| Memory Fragmentation | Lost, duplicated, stale, or disconnected context. |
| Recursion Instability | Circular rework or failure to converge. |
| Context Decay | Earlier valid facts ignored, contradicted, or omitted without explanation. |

Suggested default calculation:

```text
e = (CD + UV + MF + RI + CX) / 5
```

Where:

| Symbol | Meaning |
|---|---|
| `CD` | Contradiction Density |
| `UV` | Uncertainty Variance |
| `MF` | Memory Fragmentation |
| `RI` | Recursion Instability |
| `CX` | Context Decay |

---

## 8. Flow-Quality Metric Scoring

Flow-quality metrics use the convention: **higher is better**.

| Score | Meaning |
|---:|---|
| `0.00` | No coherent flow quality observed |
| `0.25` | Weak flow quality |
| `0.50` | Partial or inconsistent flow quality |
| `0.75` | Strong flow quality |
| `1.00` | Fully coherent, validated, and stable flow quality |

Core flow-quality metrics:

| Metric | Description |
|---|---|
| Task Completion Consistency | Required steps completed relative to expected steps. |
| Reasoning Continuity | Later steps preserve earlier valid context. |
| Semantic Coherence | Terminology, claims, and conclusions remain aligned. |
| Verification Success Rate | Verified claims relative to verifiable claims. |

Suggested default calculation:

```text
Fq = (TCC + RC + SC + VSR) / 4
```

Where:

| Symbol | Meaning |
|---|---|
| `TCC` | Task Completion Consistency |
| `RC` | Reasoning Continuity |
| `SC` | Semantic Coherence |
| `VSR` | Verification Success Rate |

---

## 9. Classification Bands

The calculated coherent flow score may be interpreted using the following provisional bands:

| Coherent Flow Score | Classification | Suggested Action |
|---:|---|---|
| `0.80–1.00` | Coherent | Proceed with normal governance. |
| `0.60–0.79` | Mostly coherent | Proceed with monitoring. |
| `0.40–0.59` | Degraded but usable | Reduce entropy before major decisions. |
| `0.20–0.39` | Misaligned | Stabilize before proceeding. |
| `0.00–0.19` | Incoherent | Stop, reassess, and restore coherence. |

These bands are provisional and should be adjusted based on validation results.

---

## 10. Minimum Assessment Record

Each validation assessment should capture the following fields:

```yaml
assessment_id: example-release-readiness-001
scenario_type: release_readiness
reviewer: reviewer_name_or_role
date: YYYY-MM-DD
objective: "Assess whether the release package is coherent enough to proceed."
evidence_reviewed:
  - "Deployment checklist"
  - "Test results"
  - "Rollback plan"
T: 0.80
E: 0.90
entropy:
  contradiction_density: 0.20
  uncertainty_variance: 0.30
  memory_fragmentation: 0.25
  recursion_instability: 0.10
  context_decay: 0.20
flow_quality:
  task_completion_consistency: 0.80
  reasoning_continuity: 0.75
  semantic_coherence: 0.70
  verification_success_rate: 0.65
calculated:
  e: 0.21
  Fq: 0.725
  F: 0.431
classification: "Degraded but usable"
recommendation: "Reduce entropy before major decisions."
entropy_drivers:
  - "Uncertainty variance"
  - "Memory fragmentation"
rationale: "Most release steps are present, but test evidence and rollback validation require clarification."
confidence: 0.75
status: Inferred
```

---

## 11. Reviewer Comparison Method

To test repeatability, each scenario should be reviewed by at least two reviewers where practical.

### Comparison Criteria

| Criterion | Target |
|---|---|
| Final classification agreement | Reviewers should usually be within one classification band. |
| Entropy driver agreement | Reviewers should identify at least one common major entropy driver. |
| Flow-quality agreement | Reviewers should broadly agree on strongest and weakest flow-quality areas. |
| Recommendation agreement | Reviewers should reach similar proceed / monitor / verify / pause / stop guidance. |
| Rationale quality | Reviewers should cite evidence rather than intuition alone. |

### Disagreement Handling

Reviewer disagreement should be treated as useful validation evidence.

Disagreement may indicate:

- unclear metric definitions;
- insufficient evidence;
- ambiguous scenario framing;
- poor weighting;
- subjective interpretation;
- need for domain-specific calibration.

---

## 12. Success Criteria

EFGM should be considered promising if validation shows that:

1. Reviewers can understand and apply the model.
2. Scores can be explained using evidence.
3. The model identifies real degradation patterns.
4. Results generally align with expert judgment.
5. The model helps clarify whether to proceed, verify, pause, or stop.
6. The assessment process is not excessively burdensome.
7. Reviewer disagreement reveals useful refinement opportunities.
8. The model improves discussion quality around coherence, uncertainty, and entropy.

---

## 13. Failure Criteria

EFGM should be reconsidered, simplified, or retired if validation shows that:

1. Reviewers cannot understand the model without extensive explanation.
2. Metrics cannot be scored consistently.
3. Results do not align with expert judgment.
4. The score creates false confidence.
5. The assessment requires too much effort for the value produced.
6. The model duplicates existing checklists without adding insight.
7. The terms are too abstract for practical use.
8. The model encourages overclaiming or inappropriate automation.

---

## 14. Validation Phases

## Phase 1: Document Review

Review the current EFGM documents for clarity, consistency, overclaiming, and usability.

### Activities

- Review README and executive summary.
- Review model definition.
- Review metric definitions.
- Review white paper.
- Identify duplicated or conflicting language.
- Confirm that limitations are clearly stated.

### Exit Criteria

- Terminology is understandable.
- Key equations are consistently defined.
- Intended use and non-use are clear.

---

## Phase 2: Controlled Scenario Testing

Apply EFGM to a small number of sanitized scenarios.

### Recommended Minimum Set

| Scenario | Minimum Count |
|---|---:|
| AI reasoning review | 2 |
| AI-assisted code review | 2 |
| Release readiness | 2 |
| Incident review | 1 |
| Documentation review | 1 |

### Exit Criteria

- Each scenario produces a completed scorecard.
- Scores include evidence and rationale.
- Reviewers can identify entropy drivers and governance actions.

---

## Phase 3: Calibration Review

Compare scores across scenarios and reviewers.

### Activities

- Identify scoring variance.
- Review where reviewers disagreed.
- Adjust metric definitions if needed.
- Adjust scoring bands if needed.
- Consider domain-specific weights.

### Exit Criteria

- Known scoring ambiguities are documented.
- Candidate improvements are captured.
- Revised metrics or weights are proposed if necessary.

---

## Phase 4: Practical Fit Assessment

Determine whether EFGM should continue and in what form.

### Possible Outcomes

| Outcome | Meaning |
|---|---|
| Continue as concept | Useful framing, but not ready for scoring. |
| Continue as checklist | Useful for structured review without numeric scoring. |
| Continue as scorecard | Numeric scoring appears useful with human review. |
| Continue as prototype engine | Suitable for tooling experiments. |
| Refactor substantially | Useful idea, but current model needs major revision. |
| Retire | Does not add sufficient value. |

---

## 15. Data Handling and Sanitization

Validation examples should avoid sensitive or restricted data.

Do not include:

- credentials;
- personal information;
- client-sensitive operational details;
- restricted architecture diagrams;
- confidential incident data;
- proprietary third-party material;
- unapproved Government of Alberta, CGI, or client information.

Use sanitized, simulated, or public examples where possible.

---

## 16. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| False precision | Treat scores as governance indicators, not exact truth. |
| Subjective scoring | Require evidence and rationale for every score. |
| Overclaiming | Clearly state that EFGM is early-stage and investigational. |
| Metric overlap | Track where metrics are hard to distinguish and refine definitions. |
| Reviewer fatigue | Use lightweight templates and limit scoring to meaningful scenarios. |
| Poor adoption | Start with practical examples, not abstract theory alone. |
| Misuse as automated approval | Require human review for governance decisions. |

---

## 17. Validation Output Artifacts

The validation process should produce the following artifacts:

| Artifact | Purpose |
|---|---|
| Completed assessment templates | Evidence of applied scoring. |
| Scenario summaries | Short summaries of each tested case. |
| Reviewer comparison notes | Agreement and disagreement analysis. |
| Metric refinement log | Proposed changes to definitions or weights. |
| Open questions | Issues requiring further research or decision. |
| Decision summary | Recommendation on whether and how to continue EFGM. |

---

## 18. Recommended Decision Gate

After initial validation, reviewers should decide whether EFGM should proceed.

### Decision Questions

1. Did EFGM identify coherence degradation that reviewers found meaningful?
2. Did the model improve the quality of the review conversation?
3. Were the metrics understandable and usable?
4. Did the scoring result align with reviewer judgment?
5. Did the model produce actionable governance recommendations?
6. Did the model avoid false certainty and overclaiming?
7. Is the value high enough to justify further development?

### Possible Decision

```text
Proceed / Refine / Pause / Retire
```

---

## 19. Summary

The EFGM validation test plan is intended to test whether the model is practical, explainable, repeatable, and useful.

The model should be validated through controlled, evidence-based scenarios and compared against expert judgment.

The goal is not to prove EFGM as a universal theory. The goal is to determine whether EFGM helps reviewers recognize when coherent flow is degrading under entropy pressure and whether that insight supports better governance decisions.
