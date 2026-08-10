# EFGM Glossary

## Purpose

This glossary separates the **canonical EFGM v2 decision-integrity model**, the **historical v1 coherent-flow model**, the **Python package version**, and the **experimental Agent Governance v0.3 extension**.

```text
Canonical model:        EFGM v2
Python package:         0.2.0
Experimental extension: Agent Governance v0.3
```

If this glossary conflicts with `docs/model-specification-v2.md`, the canonical v2 specification and executable implementation take precedence for EFGM v2 research.

---

# 1. Model Versions

## EFGM v1 — Historical Coherent-Flow Model

```text
F = (T × E × Fq) / (1 + e)
```

Retained for compatibility and conceptual history. It is **not** the canonical model for new decision-integrity research.

## EFGM v2 — Canonical Decision-Integrity Baseline

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

## Package `0.2.0`

The current unreleased Python package identity. Package `0.2.0` is not a model name and should not be called “EFGM v0.2.”

## Agent Governance v0.3 — Experimental Extension

An autonomous-agent research extension that keeps EFGM v2 task/decision flow separate from governance integrity and agency amplification. It is not part of the frozen EFGM v2 baseline.

---

# 2. Canonical EFGM v2 Terms

## `T` — Observation Maturity / Sequence Continuity

How mature, stable, and continuous the observation sequence is for the assessed decision. `T` is not literal elapsed clock time.

## `C` — Capability Suitability

Whether available tools, rules, evidence access, expertise, and execution mechanisms are suitable for the assessed objective.

## `Fq` — Flow Quality

Coherent progression toward the intended objective. The baseline family includes task completion consistency, reasoning continuity, semantic coherence, and verification success rate.

## `G` — Grounding

Whether an apparently coherent result is supported by valid rules/evidence and remains factually and domain consistent.

**`G` is reserved for Grounding in EFGM v2.** Agent Governance uses `GI`.

## `U` — Uncertainty Calibration

Whether expressed confidence is proportionate to evidence.

## `Ei` — Input Entropy

Weighted disorder presented before the decision process acts.

## `Eo` — Output Entropy

Weighted degradation introduced or retained by the decision process.

## `Be` — Behavioral Entropy

Decision distortion arising from feedback pressure such as chasing behavior, outcome bias, sunk-cost pressure, false-pattern detection, or overconfidence feedback.

## `Oe` — Operational Entropy

Execution degradation such as timeouts, retry instability, tool failures, latency pressure, and workflow interruption.

## `H` — Hidden-Information Load

Relevant state materially inaccessible at decision time. Higher `H` lowers expected-outcome confidence without automatically declaring the decision poor.

## `Q` — Positive-Factor Quality Composite

```text
Q = (T × C × Fq × G × U)^(1/5)
```

A frozen research aggregation, not a validated law.

## `DQ` — Decision Quality

```text
DQ = Q / (1 + Eo + Be + Oe)
```

Integrity of the resulting decision under evidence and conditions available at decision time.

## `CRC` — Coherence Recovery Capacity

```text
CRC = (Ei - Eo) / max(Ei, ε)
```

How much input disorder was reduced or amplified by the decision process. `CRC` is separate from `DQ`.

## `OQ` — Outcome Quality

Observed quality of the eventual outcome after the fact.

## `OD` — Outcome Divergence

```text
OD = OQ - DQ
```

Descriptive gap between outcome and decision quality.

## Outcome Confidence

```text
OutcomeConfidence = DQ × (1 - H)
```

Provisional expected-outcome confidence after accounting for hidden information.

---

# 3. Evidence and Observation Terms

## `MetricObservation`

The auditable normalized observation unit. Fields include `value`, `status`, `rationale`, `evidence_refs`, `scorer_id`, `scorer_type`, `confidence`, and optional timestamp.

## `observed`

Numeric value directly supported by evidence.

## `inferred`

Numeric value estimated from indirect evidence or reviewer judgment.

## `unknown`

Evidence is insufficient to characterize the metric. Carries no numeric value and blocks completed scoring.

## `not_applicable`

The construct genuinely does not apply. Carries no numeric value and is excluded only where model semantics permit.

## Measured `0.00`

An applicable observation assessed at the bottom of its normalized scale. It is not equivalent to `unknown` or `not_applicable`.

## Provenance Complete

Research-grade evidence requirements are satisfied for applied values and no unresolved unknowns remain.

---

# 4. Agent Governance v0.3 Terms

## `F_T` — Task / Decision Flow

EFGM v2 `DQ` used as the task-flow component in Agent Governance.

## `e_c` — Cognitive / Decision Entropy Summary

Experimental summary derived from EFGM v2 output, behavioral, and operational entropy.

## `A` — Objective Alignment

Whether the active objective remains subordinate to authorized scope and later governance changes.

## `B` — Boundary Integrity

Whether the agent remains inside authorized trust, privilege, capability, and credential boundaries.

## `O` — Observability

Whether governance can reconstruct material agent behavior and state changes.

## `M_g` — Environmental-Memory Governance

Governance of external writable/readable state that can function as persistent agent memory.

> Any surface an agent can write now and read later can potentially function as memory.

## `S_g` — Coordination Governance

Governance of peer discovery, delegation, messages, and shared goals in multi-agent or delegated workflows.

A whole-family `not_applicable` state is currently permitted **only** for coordination governance in a strictly single-agent scenario.

## `R_c` — Control Recoverability

Whether governance can regain control after intervention through effective revocation, containment, state cleanup, and rollback.

## `A_a` — Agency Amplification

Consequential reach available through privilege, connectivity, persistence, coordination, and action velocity. High `A_a` is not automatically unsafe.

## `GI` — Governance Integrity

```text
GI = geometric_mean(applicable governance-family scores)
```

Experimental aggregate of applicable governance families. `GI` is intentionally distinct from EFGM v2 `G`.

## Applicable Governance Families

The family names actually included in `GI` for a result.

## Excluded Governance Families

Whole families excluded under explicit N/A semantics. Current implementation permits only coordination governance to be excluded this way.

## Governance Family Count

Number of governance families included in `GI`. Different family counts may require stratified comparison rather than assuming direct equivalence.

## `AE` — Agency Exposure

```text
AE = A_a × (1 - GI)
```

Consequential agency that is insufficiently governed. `AE` does not fall merely because task-flow quality is low.

## `CUE` — Coherent Unsafe Execution

```text
CUE = F_T × AE
```

Effective task flow operating through agency exposure.

Because normalized `F_T` is in `[0,1]`:

```text
0 <= CUE <= AE <= 1
```

AE and CUE are related rather than orthogonal; a generic low-AE/high-CUE case is not a valid model state.

`uncontrolled_agency_risk` is retained as a compatibility alias for `CUE` during the current research cycle.

## Governance Observation Floor

```text
GovernanceObservationFloor = min(applicable governance observations)
```

A neutral non-compensatory diagnostic. A low floor does **not** automatically mean a prerequisite has failed.

## Low-Percentile Governance Diagnostic

Experimental statistic emphasizing weak observations without replacing `GI` with a hard minimum.

## Candidate Prerequisite

A governance metric path explicitly listed in the versioned Agent Governance candidate configuration for experimental non-compensatory testing.

Candidate prerequisites are hypotheses, not established safety invariants.

## Candidate Prerequisite Breach

A configured candidate-prerequisite metric whose applicable value is below the versioned candidate threshold.

## Monotonic Candidate Classification

An implementation invariant: with other state held constant, improving `GI` should not produce a more severe label. Elevated AE/CUE is evaluated first; otherwise GI determines governed versus deficit, and task flow determines high-flow versus low-flow.

---

# 5. Temporal Agent-Governance Terms

## `S_t` — Agent Governance State at Time `t`

Snapshot of task flow, cognitive entropy, governance dimensions, and agency amplification at a stage of operation.

## `sequence_id`

Explicit identity binding temporal states to one trajectory. States with different sequence identities are rejected as a single transition rather than compared as recovery states.

## State Transition

Measured change between two same-sequence agent-governance states after action, environmental change, or governance intervention. Transition results record candidate config identity/hash and before/after input hashes; post-intervention residual evidence is separately hashed when supplied.

## Governance Intervention

Action intended to regain or strengthen control, such as scope change, revocation, containment, cleanup, or rollback.

## Residual State

State that can survive an apparent intervention. Current experimental surfaces include credentials, persistence, environmental memory, coordination, privileges, scheduled actions, irreversible side effects, and rollback gaps.

## Residual Status

One of:

```text
clear
present
unknown
not_applicable
```

For a verified-recovery candidate, `clear`, `present`, and `not_applicable` require rationale, scorer identity/type, positive confidence, and evidence references. `unknown` blocks verified recovery. `not_applicable` is an evidence-backed claim that the residual surface does not apply; it is not an evidence-free omission.

## Recovery Progress Signal

A same-sequence valid `pre_intervention → post_intervention` transition with a declared intervention, higher `GI`, and lower `AE`.

Indicates movement in the intended direction; it is not recovery attestation.

## Governed Post-State

A post-intervention Agent Governance classification of either `Governed autonomous operation` or `Governed but low-flow`. Verified recovery requires a governed post-state rather than merely an improvement from a worse state.

## Verified Recovery Signal

Recovery progress plus:

- a governed post-state;
- no candidate-prerequisite breach after intervention;
- no elevated AE/CUE flag;
- complete residual-state evidence;
- no material residual state marked present.

Still an experimental research signal, not a production containment attestation.

---

# 6. Research-Control Terms

## Frozen Baseline

A model/configuration/code identity preserved unchanged for reproducible comparison.

## Candidate Model

A proposed change under evaluation that is not canonical.

## Development Set

Cases visible to tuning and hypothesis generation.

## Validation Set

Cases used for periodic comparison but not treated as a sealed holdout.

## Sealed Holdout

Externally controlled cases/labels not visible to the tuning loop before candidate freeze.

## Counterexample

Retained case exposing a material failure or limitation.

## Independent Baseline

Comparator whose criteria are not simply derived from EFGM's own composite scores.

---

# 7. Historical v1 Terms

Use only for historical conceptual discussion or explicit v1 compatibility scoring:

- `E` — Energy / Capability / Capacity;
- `Et` — Energy Transfer;
- `F` — Coherent Flow Score;
- `e` — single aggregate Entropy Load;
- `A|M` — Alignment / Misalignment conceptual outcome.

Do not substitute these for canonical EFGM v2 constructs in new research.

---

# 8. Governance Principle

```text
Detect entropy → Protect verified flow → Restore coherence → Reassess
```

EFGM scores and Agent Governance diagnostics are research indicators, not proof of truth, safety, compliance, or production readiness.
