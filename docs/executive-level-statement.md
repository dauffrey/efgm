# Executive Summary: Entropy-Flow Governance Model (EFGM)

## Purpose

The **Entropy-Flow Governance Model (EFGM)** is an experimental governance and measurement framework for evaluating whether AI-assisted reasoning, operational decisions, software-delivery workflows, and autonomous-agent activity remain coherent, grounded, calibrated, traceable, and governed under degradation pressure.

EFGM is not a proven scientific law, compliance standard, or production-ready risk engine.

## Version Identity

```text
Canonical model:        EFGM v2 — Decision Integrity
Python package:         0.2.0 — unreleased research package
Experimental extension: Agent Governance v0.3
```

Package `0.2.0` is not a model name. Agent Governance v0.3 is experimental and does not replace EFGM v2.

## Current Model Authority

The earlier coherent-flow equation:

```text
F = (T × E × Fq) / (1 + e)
```

belongs to historical v1 compatibility material. It is not the current operational research equation.

The canonical EFGM v2 formula family is:

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

EFGM v2 intentionally separates input disorder from output degradation, internal coherence from grounding, uncertainty from calibration, decision quality from outcome quality, decision quality from coherence recovery, and missing evidence from measured low values.

A successful outcome does not prove that the decision was good, and a poor outcome does not prove that the decision was bad.

## Evidence Discipline

Research-grade scoring uses auditable `MetricObservation` records with canonical states:

```text
observed
inferred
unknown
not_applicable
```

`unknown` is never silently interpreted as safe or numeric zero.

## Experimental Agent Governance v0.3

The core hypothesis is:

> High coherent task flow can coexist with weak governance integrity.

The candidate measures objective alignment, boundary integrity, observability, environmental-memory governance, coordination governance, control recoverability, and agency amplification.

```text
G  = EFGM v2 Grounding
GI = Agent Governance v0.3 Governance Integrity
```

The current experimental decomposition is:

```text
AE  = A_a × (1 - GI)
CUE = F_T × AE
```

- `AE` — **Agency Exposure**: consequential agency that is insufficiently governed.
- `CUE` — **Coherent Unsafe Execution**: effective task flow operating through that exposure.

The current benchmark treats both as lower-is-better comparators. A controlled task-flow mutation verifies that `AE` can remain stable while `CUE` changes, but that is only an implementation contract. Independent semantic validation is preregistered as `EFGM-EXP-0006`.

## Known Aggregation Limitation

Current falsification work shows that aggregate means can hide a sparse catastrophic dimension. The current response is deliberately experimental:

- report a **neutral governance observation floor**;
- report a low-percentile diagnostic;
- configure an explicit set of **candidate prerequisite metric paths**;
- compare candidate prerequisites and possible veto logic with benign controls and independent invariant checklists.

A low observation does **not** automatically become a prerequisite failure. Candidate prerequisites remain hypotheses under `EFGM-EXP-0004`.

## N/A Semantics

A whole governance family can currently be `not_applicable` only for **coordination governance** in a strictly single-agent case. The family is excluded rather than assumed perfect, and the result exposes applicable/excluded family names and family count so cross-case comparisons can be stratified when needed.

## Temporal Governance and Recovery

The autonomous-agent research loop tests whether governance can regain control after intervention:

```text
Observe → Detect deviation → Constrain / revoke → Clean residual state → Verify recovery → Reassess
```

The temporal scaffold distinguishes:

- **recovery progress** — valid pre→post intervention transition, higher `GI`, lower `AE`;
- **verified recovery signal** — recovery progress plus no remaining candidate-prerequisite breach, no elevated AE/CUE condition, complete residual-state evidence, and no material residual state present.

Residual-state checks currently cover credentials, persistence, environmental memory, coordination, privileges, scheduled actions, irreversible side effects, and rollback gaps.

Even verified recovery is an experimental research signal, not a production containment attestation. `EFGM-EXP-0005` is designed to falsify these semantics.

## Current Maturity

EFGM is currently executable, versioned, evidence-traceable, falsification-oriented, and benchmarked on controlled synthetic cases. It is suitable for research, critique, and controlled pilots.

It is not externally validated, independently replicated, a production autonomous-governance engine, a security approval mechanism, or a substitute for existing enterprise governance and accountable human review.

## Immediate Research Priorities

1. Preserve the frozen EFGM v2 baseline.
2. Run `EFGM-EXP-0004` on candidate prerequisites and benign controls.
3. Run `EFGM-EXP-0005` on temporal intervention and residual state.
4. Run `EFGM-EXP-0006` on independently authored AE/CUE semantic labels.
5. Continue inter-rater, construct-validity, sensitivity, and sealed-holdout work.
6. Keep confidence propagation as an explicit future experiment rather than silently altering scores.

The current defensible positioning is:

> **EFGM is an experimental, evidence-traceable framework for studying decision integrity, entropy recovery, and governed autonomous flow.**
