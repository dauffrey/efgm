# EFGM Glossary

## Purpose

This glossary defines the core terms used by the **Entropy-Flow Governance Model (EFGM)** repository.

The goal is to keep terminology consistent across the white paper, model definition, metric definitions, validation plan, examples, templates, and governance documents.

EFGM is currently an early-stage governance framework and scoring concept. These definitions should be treated as working definitions that may be refined through review, testing, and applied use.

---

# 1. Core Model Terms

## Entropy-Flow Governance Model (EFGM)

A proposed governance framework for evaluating whether a system, workflow, reasoning chain, or operational process is maintaining coherent flow or degrading under entropy accumulation.

EFGM is intended to help identify when current understanding, decisions, or execution are becoming less coherent and may require verification, correction, or escalation.

---

## Coherent Flow

Useful, traceable, stable progression toward an intended objective.

A system has coherent flow when its actions, reasoning, evidence, assumptions, decisions, and outputs remain aligned enough to support reliable movement toward the desired outcome.

Coherent flow does not require perfection. It requires sufficient alignment, continuity, and verification to proceed responsibly.

---

## Entropy

The accumulation of disorder, uncertainty, contradiction, fragmentation, drift, or degradation within a system.

In EFGM, entropy reduces coherent flow by weakening the system's ability to reason, decide, execute, or recover reliably.

Examples include conflicting information, stale assumptions, hidden dependencies, fragmented documentation, repeated rework, and loss of verified context.

---

## Entropy Load

The normalized amount of entropy present in a system, workflow, reasoning chain, or assessment.

Entropy load is represented as `e` in the operational equation:

```text
F = (T × E × Fq) / (1 + e)
```

Higher entropy load reduces the coherent flow score.

---

## Flow Quality

The degree to which a system's progress remains coherent, consistent, traceable, and verifiable.

Flow quality is represented as `Fq` in the operational equation.

High flow quality indicates that the system is completing required work, preserving valid context, using consistent meaning, and verifying its claims or outputs.

---

## Coherent Flow Score

The calculated EFGM score representing the degree to which a system is maintaining coherent flow under entropy pressure.

The score is represented as `F` in the operational equation:

```text
F = (T × E × Fq) / (1 + e)
```

The score is not an absolute truth. It is a governance indicator that should be interpreted with supporting evidence, reviewer judgment, and context.

---

## Alignment

A stable state where the system's understanding, actions, evidence, constraints, decisions, and outputs remain consistent with the intended objective and operational reality.

Alignment means the system is coherent enough to proceed.

---

## Misalignment

A degraded state where the system's understanding, actions, assumptions, or outputs no longer remain sufficiently consistent with the intended objective, verified evidence, or operational reality.

Misalignment may require pause, correction, escalation, or reassessment.

---

## Coherence

The degree to which information, reasoning, decisions, and actions fit together in a consistent and meaningful way.

A coherent system can explain why it is acting, what evidence supports its position, what assumptions it depends on, and how its actions connect to the objective.

---

## Coherence Degradation

The process by which a system gradually loses alignment, traceability, stability, or verification.

Coherence degradation may occur before visible failure. A system can remain active, busy, or technically functional while its understanding of reality becomes less reliable.

---

## Governance Intervention

An action taken to reduce entropy, protect coherent flow, or restore alignment.

Examples include revalidating assumptions, clarifying ownership, adding verification evidence, pausing a release, splitting work into smaller tasks, updating documentation, or escalating to human review.

---

# 2. Conceptual Formula Terms

## T — Time / Sequence / Continuity

Represents the time, sequence, iteration continuity, or observation maturity available to the system.

In practical scoring, `T` may represent whether the system has had enough stable observation, iteration, or sequencing to support reliable assessment.

---

## E — Energy / Capability / Capacity

Represents the capability available to perform useful work.

Depending on context, `E` may include tooling, compute, human expertise, operational capacity, infrastructure readiness, or available execution resources.

---

## Et — Energy Transfer

The conceptual transformation of available capability into system activity.

In the original conceptual formula:

```text
T × E → Et → F ± e → A|M
```

`Et` represents the movement from potential capability into actual work, reasoning, decision-making, or operational execution.

---

## F — Flow / Coherent Flow Score

Represents coherent progression toward an objective.

In the conceptual formula, `F` means flow. In the operational equation, `F` is the calculated coherent flow score.

---

## e — Entropy

Represents degradation pressure acting against coherent flow.

Entropy may include contradiction, uncertainty, fragmentation, context decay, operational drift, hidden dependencies, or other destabilizing factors.

---

## A — Alignment

The system remains stable, coherent, and sufficiently aligned with its objective, evidence, constraints, and operating conditions.

---

## M — Misalignment

The system has degraded into an unstable, incoherent, or unreliable state where continued action may require correction, verification, or escalation.

---

# 3. Entropy Metric Terms

## Contradiction Density

The proportion of evaluated claims, decisions, requirements, observations, or outputs that conflict with other known or verified information.

Example:

```text
Contradiction Density = conflicting claims / total evaluated claims
```

Higher values indicate greater entropy.

---

## Uncertainty Variance

The instability of confidence, estimates, assumptions, forecasts, or risk ratings over time, especially when changes are not supported by new evidence.

Uncertainty itself is not necessarily bad. This metric focuses on unexplained or unstable uncertainty.

Higher values indicate greater entropy.

---

## Memory Fragmentation

The degree to which relevant context, decisions, documentation, or system state is lost, duplicated, stale, scattered, or disconnected across sources.

Examples include missing decision history, duplicated documents, stale runbooks, disconnected tickets, or knowledge stored only in chat or individual memory.

Higher values indicate greater entropy.

---

## Recursion Instability

The degree to which a system loops, repeats analysis, reopens resolved issues, retries without learning, or fails to converge on a stable conclusion or action.

Examples include repeated root-cause resets, circular discussions, failed correction loops, or unresolved retry cycles.

Higher values indicate greater entropy.

---

## Context Decay

The loss, weakening, contradiction, or omission of earlier valid facts, assumptions, constraints, or decisions over time.

Context decay occurs when previously valid information is ignored, forgotten, or contradicted without explanation.

Higher values indicate greater entropy.

---

## Operational Drift

The divergence between the intended, documented, or approved process and the way work is actually being performed.

Operational drift may occur gradually as exceptions, shortcuts, undocumented practices, or environmental differences accumulate.

Higher values indicate greater entropy.

---

## Stale Assumption

An assumption that may have been valid earlier but has not been recently verified and may no longer reflect current reality.

Stale assumptions increase entropy because decisions may be based on outdated or untested beliefs.

---

## Hidden Dependency

A dependency that affects outcomes but is not visible, documented, monitored, or understood within the normal workflow.

Hidden dependencies can cause a system to appear coherent while remaining vulnerable to unexpected failure.

---

## Environment Inconsistency

A mismatch between environments, configurations, versions, data, permissions, infrastructure, or runtime behavior.

Examples include differences between development, test, acceptance, training, and production environments.

---

## Duplicated Logic

Repeated or overlapping logic across code, documents, workflows, or decisions that may diverge over time.

Duplicated logic can increase entropy when multiple versions of the same rule or process evolve independently.

---

# 4. Flow-Quality Metric Terms

## Task Completion Consistency

The proportion of required or expected steps that are completed correctly, in sequence, and without unjustified omission.

Example:

```text
Task Completion Consistency = correctly completed required steps / total required steps
```

Higher values indicate stronger flow quality.

---

## Reasoning Continuity

The degree to which later reasoning preserves, builds on, and remains consistent with earlier valid context, assumptions, evidence, and decisions.

Reasoning continuity is strong when conclusions follow from evidence and earlier constraints remain respected.

Higher values indicate stronger flow quality.

---

## Semantic Coherence

The degree to which terminology, claims, classifications, evidence, and conclusions remain meaningfully aligned within the same conceptual frame.

Semantic coherence is weak when terms are used inconsistently or when conclusions do not match the meaning of the evidence.

Higher values indicate stronger flow quality.

---

## Verification Success Rate

The proportion of verifiable claims, outputs, decisions, or artifacts that are successfully validated against reliable evidence, tests, source systems, or accepted criteria.

Example:

```text
Verification Success Rate = successfully verified claims / total verifiable claims
```

Higher values indicate stronger flow quality.

---

## Operational Traceability

The ability to trace a decision, output, artifact, or action back to supporting evidence, source material, approval, requirement, or system state.

Operational traceability improves confidence that flow is coherent and reviewable.

---

## Deployment Predictability

The degree to which deployment or release outcomes are reasonably knowable based on available evidence, environment consistency, test results, dependencies, and rollback readiness.

Higher deployment predictability indicates stronger flow quality in release-readiness contexts.

---

## Observability

The availability of logs, metrics, traces, reports, artifacts, or audit evidence needed to understand system behavior and validate outcomes.

Observability supports verification and reduces hidden entropy.

---

## Recovery Integrity

The degree to which a system can restore coherence after failure, disruption, or degradation.

Recovery integrity includes rollback readiness, incident recovery quality, state restoration, evidence preservation, and post-recovery validation.

---

# 5. Scoring and Interpretation Terms

## Normalization

The process of converting metric values to a common scale, typically `0.00` to `1.00`, so they can be compared and combined.

In EFGM, entropy metrics and flow-quality metrics are commonly normalized to support scoring.

---

## Weight

A multiplier used to adjust the importance of a metric within a composite score.

Weights should be treated as provisional unless calibrated through domain-specific validation.

---

## Classification Band

A score range used to interpret the coherent flow score.

Example bands may include:

| Score Range | Classification |
|---:|---|
| `0.80–1.00` | Coherent |
| `0.60–0.79` | Mostly coherent |
| `0.40–0.59` | Degraded but usable |
| `0.20–0.39` | Misaligned |
| `0.00–0.19` | Incoherent |

Classification bands are provisional and should be validated through applied testing.

---

## Entropy Driver

A metric or condition that contributes significantly to overall entropy load.

Examples include high contradiction density, severe context decay, fragmented documentation, or repeated non-convergent rework.

---

## Confidence

The assessor's level of confidence in the metric score or assessment conclusion.

Confidence should be based on evidence quality, source reliability, completeness, and reviewer agreement.

---

## Evidence Status

A label used to describe the strength of support behind a claim, score, or conclusion.

Recommended labels:

| Label | Meaning |
|---|---|
| Verified | Supported by direct evidence |
| Inferred | Reasonably concluded from available evidence |
| Assumed | Used as a working assumption |
| Unknown | Not enough evidence to assess |
| Not Applicable | Does not apply in this context |

---

# 6. Governance Action Terms

## Proceed

Continue with normal governance because coherent flow appears sufficient and entropy is low or controlled.

---

## Monitor

Continue while tracking known entropy drivers or uncertainty areas.

This action is appropriate when flow remains mostly coherent but watch items exist.

---

## Verify

Pause or slow decision-making long enough to confirm claims, assumptions, artifacts, dependencies, or evidence.

Verification is appropriate when uncertainty, contradiction, or missing evidence could affect the decision.

---

## Stabilize

Reduce entropy before proceeding.

Stabilization may include resolving contradictions, consolidating context, restoring traceability, clarifying ownership, updating documentation, or correcting process drift.

---

## Escalate

Raise the issue to a human reviewer, governance body, architecture group, security/risk team, product owner, or decision authority.

Escalation is appropriate when entropy is high, evidence is insufficient, risk is material, or the system is no longer coherent enough to self-correct.

---

## Stop

Halt the action, decision, release, or autonomous process until coherence can be restored.

This is appropriate when the system is misaligned, evidence is contradictory, verification is insufficient, or continued action would create unacceptable risk.

---

# 7. Domain Terms

## AI Reasoning Governance

Use of EFGM to assess whether an AI-assisted reasoning process remains coherent, evidence-aligned, and verifiable.

This may include evaluating hallucination risk, prompt drift, unsupported assumptions, context decay, or inconsistent conclusions.

---

## AI-Assisted Development

Use of AI tools such as coding assistants to generate, review, explain, or modify software artifacts.

In EFGM, AI-assisted development can be assessed for architectural alignment, duplicated logic, hidden dependencies, verification quality, and operational traceability.

---

## Release Readiness

The degree to which a release is coherent enough to proceed based on artifacts, test results, environment readiness, dependency state, rollback planning, support readiness, and stakeholder alignment.

---

## Incident Review

A structured review of an incident or outage to determine what happened, why it happened, how it was resolved, and what should be improved.

EFGM can be used to evaluate whether incident response converged toward verified understanding or accumulated entropy.

---

## Migration Planning

The planning and execution of system movement, upgrade, modernization, or environment transition.

EFGM can help assess whether application, database, security, infrastructure, validation, and operational layers remain coherent during migration.

---

# 8. Important Boundaries

## EFGM Is Not a Proof of Correctness

An EFGM score does not prove that an output, release, decision, or system is correct.

It indicates the assessed level of coherent flow under observed entropy.

---

## EFGM Does Not Replace Expert Judgment

EFGM is intended to support review and governance. It does not replace architecture review, security review, privacy review, operational approval, legal review, or human accountability.

---

## EFGM Should Not Create False Precision

Scores should be interpreted with evidence, rationale, uncertainty, and reviewer context.

A precise numeric score without reliable evidence should not be treated as meaningful.

---

## EFGM Is Provisional

The current terminology, scoring bands, metrics, and weights are working definitions.

They should be refined through real examples, reviewer feedback, and validation against observed outcomes.

---

# 9. Summary

EFGM uses a small set of core concepts:

```text
Coherent Flow
Entropy
Flow Quality
Verification
Alignment
Governance Intervention
```

The model's purpose is to help determine whether a system, workflow, reasoning chain, or decision path is still coherent enough to proceed, or whether entropy has accumulated enough to require verification, stabilization, escalation, or pause.
