# EFGM Assumptions

## Purpose

This document records the working assumptions behind the **canonical EFGM v2 decision-integrity baseline** and identifies assumptions introduced by the **experimental v0.3 agent-governance candidate**.

These are hypotheses to test, not facts to defend. If an assumption fails under controlled evidence, EFGM should be simplified, revised, or rejected accordingly.

The historical v1 equation:

```text
F = (T × E × Fq) / (1 + e)
```

belongs to the legacy coherent-flow model and is not the current canonical operational equation. Historical v1 material is preserved under `docs/legacy/`.

---

# 1. Canonical v2 Model Assumptions

## A-001 — Decision Integrity Can Be Assessed From Observable Evidence

EFGM assumes that a decision process can be characterized well enough to support governance analysis using observable evidence about:

- sequence continuity;
- capability suitability;
- flow quality;
- grounding;
- uncertainty calibration;
- input and output degradation;
- behavioral pressure;
- operational disruption.

This does not assume perfect measurement. It assumes the constructs may be measurable enough to add value beyond unstructured judgment.

**Status:** Unvalidated  
**Primary test:** inter-rater agreement, construct validity, predictive comparison.

## A-002 — Input and Output Entropy Are Distinguishable

EFGM assumes the disorder presented to a decision process (`Ei`) can be distinguished from degradation introduced or retained by the process (`Eo`).

This distinction is necessary for Coherence Recovery Capacity:

```text
CRC = (Ei - Eo) / max(Ei, ε)
```

**Status:** Unvalidated  
**Primary test:** controlled input/output mutation cases and scorer agreement.

## A-003 — Decision Quality and Outcome Quality Are Different Constructs

EFGM assumes a decision should be evaluated using information available at decision time rather than judged only by its eventual outcome.

```text
DQ != OQ
OD = OQ - DQ
```

This protects against outcome bias and allows lucky bad decisions and unlucky good decisions to remain analytically distinct.

**Status:** Required research principle; empirical usefulness still unvalidated.

## A-004 — Flow Quality, Grounding, and Calibration Are Distinguishable

EFGM v2 assumes:

- `Fq` measures coherent progression;
- `G` measures evidentiary/rule grounding;
- `U` measures confidence calibration.

A fluent answer may have high semantic coherence and low grounding. A factually grounded answer may still be badly calibrated about uncertainty.

**Status:** Unvalidated  
**Primary test:** blinded scorer agreement and construct-selective mutations.

## A-005 — Behavioral Entropy Adds Information

EFGM assumes decision distortion caused by chasing behavior, outcome bias, sunk-cost pressure, false-pattern detection, or overconfidence feedback may provide explanatory or predictive value beyond grounding and calibration alone.

**Status:** Unvalidated  
**Primary test:** ablation and independent-label comparison.

## A-006 — Operational Entropy May Affect Decision Reliability

The frozen v2 model currently penalizes `DQ` for operational entropy such as tool failures, retries, timeouts, latency pressure, and workflow interruptions.

However, EFGM does **not** assume this placement is settled. Operational entropy may prove to belong partly or entirely in a downstream execution-reliability construct.

**Status:** Explicit open question.

## A-007 — The Geometric Positive-Factor Composite Is Useful

The frozen v2 baseline uses:

```text
Q = (T × C × Fq × G × U)^(1/5)
```

EFGM assumes only that this is a useful baseline candidate for comparison. It does not assume geometric aggregation is scientifically necessary or superior to simpler arithmetic or checklist models.

**Status:** Provisional  
**Primary test:** ablation, independent baselines, unseen cases.

## A-008 — Additive Entropy Penalties Are a Useful Baseline

The frozen v2 baseline uses:

```text
DQ = Q / (1 + Eo + Be + Oe)
```

This is a reproducible hypothesis, not an established law. Interaction effects, gates, or alternative execution models may perform better.

**Status:** Provisional.

## A-009 — Missing Evidence Must Not Become a Favorable Number

Canonical observation states are:

```text
observed
inferred
unknown
not_applicable
```

EFGM assumes that silently mapping `unknown` to zero or another favorable value would create false reassurance.

Therefore:

```text
unknown != 0.00
unknown != safe
not_applicable != unknown
```

**Status:** Required governance invariant.

## A-010 — Evidence Provenance Improves Research Quality

EFGM assumes that recording rationale, evidence references, scorer identity/type, and confidence makes scoring more auditable and supports analysis of disagreement.

Whether strict provenance improves predictive validity enough to justify its assessment burden remains empirical.

**Status:** Required for research-grade runs; incremental benefit unvalidated.

## A-011 — Classification Bands Can Add Governance Value

EFGM currently maps continuous values to provisional governance labels. It assumes these labels may help actionability but does not assume the current thresholds are calibrated across domains.

**Status:** Unvalidated.

## A-012 — Some Dimensions May Be Non-Compensatory

Current falsification work has demonstrated that family means can dilute sparse catastrophic failures.

EFGM therefore now assumes only that **non-compensatory prerequisite or veto behavior is a legitimate candidate to test**. It does not assume a particular prerequisite set or threshold has already been validated.

Candidate mechanisms include:

- prerequisite floors;
- extreme-degradation veto diagnostics;
- soft-min / low-percentile diagnostics;
- independent invariant checklists.

**Status:** Supported as a research need by retained counterexamples; implementation details unvalidated.

---

# 2. Experimental v0.3 Agent-Governance Assumptions

## AG-001 — High Task Flow Can Coexist With Weak Governance

The v0.3 candidate assumes an autonomous agent can remain effective at task execution while moving outside authorized objectives, boundaries, observability, memory controls, coordination controls, or recoverability expectations.

This is the central motivation for separating task flow from agent-governance integrity.

**Status:** Supported by controlled synthetic construct tests; not externally validated.

## AG-002 — Agent-Governance Integrity Is Distinct From v2 Grounding

v2 `G` means **Grounding**.

v0.3 uses `GI` for **Governance Integrity** to avoid symbol and construct collision.

The governance families are:

- objective alignment;
- boundary integrity;
- observability;
- environmental-memory governance;
- coordination governance;
- control recoverability.

**Status:** Candidate construct architecture.

## AG-003 — Agency Amplification Is Not Automatically Unsafe

High privilege, connectivity, persistence, coordination, or action velocity can be legitimate and well governed.

Risk should arise from the interaction between agency and governance weakness rather than from agency alone.

**Status:** Required design principle for current v0.3 research.

## AG-004 — Agency Exposure and Coherent Unsafe Execution Are Different

The earlier candidate:

```text
R_U = F_T × A_a × (1 - GI)
```

mixes uncontrolled agency with task effectiveness. That can make apparent risk fall when task flow falls, even though a poorly governed high-agency system may still present material exposure.

The current experimental decomposition is:

```text
AE  = A_a × (1 - GI)
CUE = F_T × AE
```

Where:

- `AE` = Agency Exposure;
- `CUE` = Coherent Unsafe Execution.

Neither formula is canonical or a calibrated incident probability.

**Status:** New candidate hypothesis requiring comparison.

## AG-005 — External Writable/Readable State Can Function as Memory

Any surface an agent can write now and read later may function as environmental memory even if it is not labeled as a memory subsystem.

Examples may include files, tickets, databases, queues, caches, shared documents, tool state, or other persistent environment surfaces.

**Status:** Candidate operational principle requiring external testing.

## AG-006 — Unknown Governance Evidence Is Not Safety Evidence

An unobserved boundary violation, unmeasured trace gap, or unknown persistence surface must not be treated as proof of integrity.

**Status:** Required governance invariant.

## AG-007 — N/A Governance Families Should Be Excluded, Not Assumed Perfect

Some agent scenarios may genuinely lack a governance family—for example, a strictly single-agent case may have no multi-agent coordination surface.

An explicitly all-`not_applicable` family should be excluded from the experimental `GI` aggregation rather than blocking scoring or being assigned a favorable numeric value.

This exclusion requires explicit rationale and scorer provenance in research-grade runs.

**Status:** Candidate v0.3 semantics.

## AG-008 — Static Snapshots Are Insufficient for Autonomous Governance

An agent may move through materially different governance states during execution.

EFGM therefore assumes temporal research must evaluate state transitions, including governance changes and recovery after intervention.

```text
S_t → action/environment change → S_t+1 → intervention → S_t+2
```

**Status:** Research direction; predictive temporal model not established.

## AG-009 — Recoverability Should Become Increasingly Observable

Control recoverability should ultimately be supported by intervention evidence such as:

- revocation effectiveness;
- containment effectiveness;
- residual credential/capability state;
- cleanup completeness;
- rollback effectiveness;
- recovery latency.

**Status:** Candidate measurement direction.

---

# 3. Measurement Assumptions

## M-001 — Normalized Scores Can Be Applied Consistently Enough to Test

Base observations use a normalized `[0,1]` scale when applicable. EFGM assumes scoring anchors can become consistent enough for research comparison.

**Status:** Unvalidated.

## M-002 — Human Judgment Will Remain Necessary During Early Validation

Some constructs require domain interpretation. EFGM assumes scoring can still be useful if rationale and evidence are preserved and disagreement is treated as validation data.

**Status:** Expected.

## M-003 — Reviewer Confidence Should Not Yet Be Silently Folded Into Scores

Confidence is recorded but the frozen baseline does not mathematically propagate scorer uncertainty.

Possible uncertainty propagation, intervals, or Monte Carlo treatments are future candidates and must be tested explicitly rather than introduced invisibly.

**Status:** Deferred research question.

## M-004 — Domain-Specific Weights May Help or Overfit

EFGM does not assume domain-specific weighting is automatically better. Domain-specific configurations must be versioned and validated against independent evidence.

**Status:** Open question.

---

# 4. Governance and Scientific Assumptions

## G-001 — EFGM Supports Judgment; It Does Not Replace Accountability

EFGM scores and diagnostics are decision-support signals. Accountable domain owners remain responsible for consequential decisions.

## G-002 — EFGM Must Compete With Simpler Alternatives

A more elaborate EFGM candidate should not be promoted if a simpler independent checklist provides equivalent or better useful performance.

## G-003 — Holdouts Must Remain Outside the Tuning Loop

Real holdout contents and labels must remain externally sealed until the candidate and success criteria are frozen.

## G-004 — Counterexamples Are Assets

Material failures, false reassurance, regressions, and rejected candidates must be retained rather than hidden.

## G-005 — Internal Synthetic Success Is Not External Validation

Controlled synthetic cases can test responsiveness and invariants but cannot establish external predictive validity.

## G-006 — EFGM May Fail to Add Enough Value

The research program must preserve the possibility that some constructs are redundant, some formulas are unnecessary, or the overall scoring burden does not outperform simpler governance methods.

Retiring or simplifying a construct is a valid successful research outcome.

---

# 5. Assumption Register

| ID | Assumption | Status | Primary Validation |
|---|---|---|---|
| A-001 | Decision integrity can be assessed from observable evidence | Unvalidated | Inter-rater + predictive tests |
| A-002 | `Ei` and `Eo` are distinguishable | Unvalidated | Controlled mutations |
| A-003 | `DQ` and `OQ` should remain separate | Research principle | Outcome-divergence studies |
| A-004 | `Fq`, `G`, `U` are distinct | Unvalidated | Construct validity |
| A-005 | Behavioral entropy adds value | Unvalidated | Ablation |
| A-006 | Operational entropy belongs partly in `DQ` | Open | Execution-reliability comparison |
| A-007 | Geometric aggregation adds value | Provisional | Simpler-baseline comparison |
| A-008 | Additive entropy penalties are useful | Provisional | Alternative aggregation tests |
| A-009 | Unknown must not default favorable | Required | Invariant tests |
| A-010 | Provenance improves research quality | Required / benefit unvalidated | Inter-rater + predictive tests |
| A-011 | Classification bands add value | Unvalidated | False reassurance/alarm tests |
| A-012 | Non-compensatory diagnostics deserve testing | Supported research need | Sparse-failure benchmark |
| AG-001 | High flow can coexist with weak governance | Synthetic support | External agent cases |
| AG-002 | `GI` is distinct from v2 `G` | Candidate construct | Construct validity |
| AG-003 | Agency itself is not automatically unsafe | Design principle | Comparative cases |
| AG-004 | `AE` and `CUE` should be separated | Candidate | Benchmark comparison |
| AG-007 | All-N/A governance families should be excluded | Candidate semantics | N/A tests |
| AG-008 | Temporal state matters | Candidate direction | Transition experiments |
| M-003 | Confidence propagation should remain explicit research | Deferred | Uncertainty experiments |

---

# 6. Review Rule

The purpose of this register is not to protect EFGM's assumptions.

It is to make them easy to falsify.

A question is not resolved because a preferred narrative sounds plausible. It is resolved only to the extent supported by reproducible evidence.