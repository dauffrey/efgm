# EFGM Glossary

## Purpose

This glossary defines current EFGM terminology and explicitly separates the **canonical v2 decision-integrity model**, the **historical v1 coherent-flow model**, and the **experimental v0.3 autonomous-agent extension**.

If this glossary conflicts with `docs/model-specification-v2.md`, the canonical v2 specification and executable implementation take precedence for v2 research.

---

# 1. Model Versions

## EFGM v1 — Historical Coherent-Flow Model

The original operational line used:

```text
F = (T × E × Fq) / (1 + e)
```

It remains available for compatibility and conceptual history. It is **not** the canonical model for new decision-integrity research.

## EFGM v2 — Canonical Decision-Integrity Baseline

The current canonical research baseline.

```text
Ei = weighted input entropy
Eo = weighted output entropy
CRC = (Ei - Eo) / max(Ei, ε)
G = weighted grounding
Q = (T × C × Fq × G × U)^(1/5)
DQ = Q / (1 + Eo + Be + Oe)
OutcomeConfidence = DQ × (1 - H)
OD = OQ - DQ
```

## EFGM v0.3 — Experimental Governed Agentic Flow

An experimental autonomous-agent extension that keeps v2 task/decision flow separate from agent-governance integrity and agency amplification.

It is not part of the frozen v2 baseline.

---

# 2. Canonical v2 Terms

## `T` — Observation Maturity / Sequence Continuity

How mature, stable, and continuous the observation sequence is for the assessed decision. `T` is not literal elapsed clock time.

## `C` — Capability Suitability

Whether the available tools, rules, evidence access, expertise, and execution mechanisms are suitable for the assessed objective.

## `Fq` — Flow Quality

Coherent progression toward the intended objective. The baseline family includes:

- task completion consistency;
- reasoning continuity;
- semantic coherence;
- verification success rate.

## `G` — Grounding

Whether an apparently coherent result is actually supported by valid rules/evidence and remains factually and domain consistent.

**`G` is reserved for Grounding in canonical v2.** Agentic Governance Integrity uses `GI`.

## `U` — Uncertainty Calibration

Whether expressed confidence is proportionate to evidence.

## `Ei` — Input Entropy

The weighted disorder present before the decision process acts. Baseline metrics:

- input contradiction;
- input ambiguity;
- input goal conflict;
- missing context;
- hidden-information load.

## `Eo` — Output Entropy

The weighted degradation introduced or retained in the output. Baseline metrics:

- output contradiction;
- uncertainty mismatch;
- goal drift;
- reasoning instability;
- context decay.

## `Be` — Behavioral Entropy

Decision distortion arising from feedback pressure rather than ordinary semantic inconsistency. Baseline metrics include chasing behavior, outcome bias, sunk-cost pressure, false-pattern detection, and overconfidence feedback.

## `Oe` — Operational Entropy

Execution degradation that can reduce decision reliability, including timeouts, retry instability, tool failures, latency pressure, and workflow interruption.

## `H` — Hidden-Information Load

Relevant state that is materially inaccessible at decision time. Higher `H` reduces confidence in expected outcomes without automatically declaring the decision itself poor.

## `Q` — Positive-Factor Quality Composite

```text
Q = (T × C × Fq × G × U)^(1/5)
```

A frozen research aggregation, not a scientifically validated constant or law.

## `DQ` — Decision Quality

```text
DQ = Q / (1 + Eo + Be + Oe)
```

The integrity of the resulting decision under the evidence and conditions available at decision time.

## `CRC` — Coherence Recovery Capacity

```text
CRC = (Ei - Eo) / max(Ei, ε)
```

Measures how much input disorder was reduced or amplified by the decision process. `CRC` is separate from `DQ`.

## `OQ` — Outcome Quality

Observed quality of the eventual outcome after the fact.

## `OD` — Outcome Divergence

```text
OD = OQ - DQ
```

A descriptive gap between outcome quality and decision quality. It is not inherently good or bad.

## Outcome Confidence

```text
OutcomeConfidence = DQ × (1 - H)
```

A provisional measure that lowers expected-outcome confidence when hidden information is high.

---

# 3. Evidence and Observation Terms

## `MetricObservation`

The auditable unit used to support a normalized EFGM metric.

Fields include:

- `value`;
- `status`;
- `rationale`;
- `evidence_refs`;
- `scorer_id`;
- `scorer_type`;
- `confidence`;
- optional timestamp.

## `observed`

A numeric value directly supported by evidence.

## `inferred`

A numeric value estimated from indirect evidence or reviewer judgment.

## `unknown`

Evidence is insufficient to characterize the metric. `unknown` carries no numeric value and blocks completed baseline scoring.

## `not_applicable`

The construct genuinely does not apply. It carries no numeric value and is excluded according to the relevant aggregation rules.

## Measured `0.00`

An applicable observation assessed at the bottom of its normalized scale. It is **not** equivalent to `unknown` or `not_applicable`.

## Provenance Complete

An assessment satisfies the research-grade evidence requirements for rationale, evidence references where required, scorer identity/type, positive confidence for applied values, and no unresolved unknowns.

---

# 4. Agent-Governance Terms (Experimental v0.3)

## `F_T` — Task / Decision Flow

The v2 decision-quality value used as the task-flow component in the agent-governance candidate.

## `e_c` — Cognitive / Decision Entropy Summary

An experimental summary derived from v2 output, behavioral, and operational entropy.

## `A` — Objective Alignment

Whether the active objective remains subordinate to authorized scope and later governance changes.

## `B` — Boundary Integrity

Whether the agent remains inside authorized trust, privilege, capability, and credential boundaries.

## `O` — Observability

Whether governance can reconstruct material agent behavior and state changes.

## `M_g` — Environmental-Memory Governance

Governance of external writable/readable state that can function as persistent agent memory.

Working principle:

> Any surface an agent can write now and read later can potentially function as memory.

## `S_g` — Coordination Governance

Governance of peer discovery, delegation, messages, and shared goals in multi-agent or delegated workflows.

## `R_c` — Control Recoverability

Whether governance can regain control after intervention through effective revocation, containment, state cleanup, and rollback.

## `A_a` — Agency Amplification

The consequential reach available to an agent through privilege, connectivity, persistence, coordination, and action velocity.

High `A_a` is not automatically unsafe.

## `GI` — Governance Integrity

The experimental aggregate of applicable agent-governance families.

```text
GI = geometric_mean(applicable governance-family scores)
```

`GI` is intentionally distinct from v2 `G` (Grounding).

## `AE` — Agency Exposure

```text
AE = A_a × (1 - GI)
```

Consequential agency that is insufficiently governed. Unlike the earlier uncontrolled-agency candidate, `AE` does not fall merely because task-flow quality is low.

## `CUE` — Coherent Unsafe Execution

```text
CUE = F_T × AE
```

Effective task flow operating through agency exposure.

The earlier v0.3 field `uncontrolled_agency_risk` is retained only as a compatibility alias for `CUE` while experiments compare candidate formulations.

## Governance Prerequisite Floor

An experimental non-compensatory diagnostic equal to the lowest applicable governance observation. It exists to expose sparse catastrophic failures that family means can dilute.

It is a diagnostic, not a promoted replacement for the continuous v0.3 scores.

## Soft-Min / Low-Percentile Diagnostic

An experimental statistic emphasizing the weakest governance observations without replacing the aggregate score with a hard minimum.

---

# 5. Temporal Agent-Governance Terms

## `S_t` — Agent Governance State at Time `t`

A snapshot of task flow, cognitive entropy, governance dimensions, and agency amplification at a particular stage of agent operation.

## State Transition

A measured change from one governance state to another after agent action, environmental change, or governance intervention.

## Governance Intervention

An action intended to regain or strengthen control, such as scope change, revocation, containment, state cleanup, or rollback.

## Residual Agency

Capability, persistence, connectivity, credentials, coordination, or writable state that remains available after a governance intervention.

## Recovery

A transition in which governance integrity increases and/or agency exposure decreases after intervention, with evidence that material residual state has been addressed.

---

# 6. Research-Control Terms

## Frozen Baseline

A model/configuration/code identity that is preserved unchanged for reproducible comparison.

## Candidate Model

A proposed change under evaluation that is not yet canonical.

## Development Set

Cases visible to the tuning and hypothesis-generation loop.

## Validation Set

Cases used for periodic candidate comparison but not treated as a genuinely sealed holdout.

## Sealed Holdout

Externally controlled cases/labels not visible to the tuning loop before candidate freeze.

## Counterexample

A retained case that exposes a material failure or limitation in a model or candidate.

## Independent Baseline

A comparator whose criteria are not simply derived from EFGM's own composite scores.

---

# 7. Historical v1 Terms

The following terms remain useful only when discussing the original conceptual model or explicit v1 compatibility scoring:

- `E` — Energy / Capability / Capacity;
- `Et` — Energy Transfer;
- `F` — Coherent Flow Score;
- `e` — single aggregate Entropy Load;
- `A|M` — Alignment / Misalignment conceptual outcome.

Do not use those v1 symbols as substitutes for the canonical v2 constructs in new decision-integrity research.

---

# 8. Governance Principle

EFGM's core operating principle remains:

```text
Detect entropy → Protect verified flow → Restore coherence → Reassess
```

Scores are governance indicators, not proof of truth, safety, compliance, or production readiness.