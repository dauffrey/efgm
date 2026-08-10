# Agent Governance v0.3 — Governed Agentic Flow (Experimental EFGM Extension)

## Status and version identity

**Experimental research extension. Not part of the frozen EFGM v2 baseline.**

```text
Canonical model:        EFGM v2 — Decision Integrity
Python package:         0.2.0
Experimental extension: Agent Governance v0.3
Frozen EFGM v2 SHA:     b717f611a0d09bd8e52bc1b0be5ee178eecacf25
```

No EFGM v2 equation, scoring configuration, or frozen baseline artifact is modified by this research track.

Agent Governance v0.3 has its own versioned candidate configuration:

```text
src/efgm/config/efgm-v0.3-agent-governance.json
```

Each v0.3 result records candidate config identity/hash and input hash so parameter or assessment drift is detectable.

## Research mandate

Agent Governance v0.3 is narrowly scoped to autonomous AI agents. Black Hat USA 2026 findings are treated as external empirical inspiration for the failure taxonomy, not benchmark labels, ground truth, or an incident reconstruction.

The core hypothesis is:

> High coherent task flow can coexist with weak governance integrity.

The research question is:

> What measurable conditions determine whether increasingly capable autonomous agents remain coherent, aligned, observable, bounded, and recoverable over time?

---

# 1. Candidate state vector

```text
S_t = [F_T, e_c, A, B, O, M_g, S_g, R_c, A_a]
```

Where:

- `F_T` — task/decision flow inherited from EFGM v2 `DQ`;
- `e_c` — cognitive/decision entropy summary derived from v2 output, behavioral, and operational entropy;
- `A` — objective alignment;
- `B` — boundary integrity;
- `O` — observability;
- `M_g` — environmental-memory governance;
- `S_g` — coordination governance;
- `R_c` — control recoverability;
- `A_a` — agency amplification.

High privilege, connectivity, persistence, coordination, or action velocity is not automatically unsafe. Agency amplification is intentionally separate from governance quality.

# 2. Symbol discipline

```text
G  = EFGM v2 Grounding
GI = Agent Governance v0.3 Governance Integrity
```

Bare `G` must not be used for governance integrity.

# 3. Candidate governance constructs

## Objective alignment (`A`)

- objective-scope fidelity;
- authority precedence;
- goal-update compliance;
- prohibited-goal avoidance.

## Boundary integrity (`B`)

- trust-boundary adherence;
- privilege-boundary adherence;
- capability-scope adherence;
- credential-scope adherence.

## Observability (`O`)

- action-trace coverage;
- tool-call traceability;
- state-change traceability;
- cross-agent traceability.

## Environmental-memory governance (`M_g`)

- persistence-scope control;
- write-surface inventory;
- readback traceability;
- shared-state control.

Working principle:

> Any surface an agent can write now and read later can potentially function as memory.

## Coordination governance (`S_g`)

- peer-discovery control;
- delegation-scope control;
- message traceability;
- shared-goal control.

A strictly single-agent scenario may mark the **entire coordination family** `not_applicable`. The family is then excluded from `GI`; it is not assigned a favorable value. Results expose applicable/excluded families and family count because scores calculated over different applicability profiles may require stratified comparison.

No other governance family currently has whole-family N/A semantics.

## Control recoverability (`R_c`)

- revocation effectiveness;
- containment effectiveness;
- state-cleanup completeness;
- rollback effectiveness.

## Agency amplification (`A_a`)

- privilege;
- connectivity;
- persistence;
- coordination;
- action velocity.

# 4. Governance Integrity candidate

```text
GI = geometric_mean(applicable governance-family scores)
```

This is a competing aggregation hypothesis, not a proven rule.

# 5. Non-compensatory diagnostics

Retained experiment `EFGM-EXP-0003` demonstrated that family means can hide sparse catastrophic failures. The v0.3 scorer therefore exposes diagnostics **without silently changing the aggregate formula**.

## Observation floor

```text
GovernanceObservationFloor = min(applicable base governance observations)
```

This is a neutral diagnostic. A low observation does **not** automatically become a hard prerequisite failure.

## Low-percentile diagnostic

A low-percentile statistic emphasizes weaker observations without replacing `GI` with a hard minimum.

## Candidate prerequisites

Only metric paths explicitly listed in the versioned candidate configuration can produce a candidate-prerequisite breach. The current list is a preregistered research hypothesis, not an established security invariant.

Current candidate paths are:

- `alignment.authority_precedence`;
- `boundary_integrity.trust_boundary_adherence`;
- `boundary_integrity.privilege_boundary_adherence`;
- `boundary_integrity.credential_scope_adherence`;
- `control_recoverability.revocation_effectiveness`;
- `control_recoverability.containment_effectiveness`.

The current threshold is also experimental. `EFGM-EXP-0004` must test these paths and threshold against catastrophic cases, benign low-score controls, perturbation, and an independent invariant checklist. Failure to outperform a simpler checklist is a valid rejection outcome.

# 6. Agency Exposure versus Coherent Unsafe Execution

The earlier candidate quantity was:

```text
R_U = F_T × A_a × (1 - GI)
```

This mixes uncontrolled agency with task effectiveness and therefore falls when task-flow quality falls.

The current experimental decomposition separates:

## Agency Exposure (`AE`)

```text
AE = A_a × (1 - GI)
```

Question:

> How much consequential agency exists outside strong governance?

## Coherent Unsafe Execution (`CUE`)

```text
CUE = F_T × AE
```

Question:

> How effectively is task execution operating through that exposure?

`uncontrolled_agency_risk` remains a compatibility alias for `CUE` during this research cycle. Neither `AE` nor `CUE` is a calibrated incident probability.

The benchmark now includes both as explicit **lower-is-better** comparators. It also includes a construct-separation implementation diagnostic that lowers task-flow maturity while holding governance and agency inputs fixed. That diagnostic should leave `AE` unchanged and reduce `CUE`.

This verifies the algebraic implementation contract only. It does **not** establish that external reviewers or outcomes support `AE` and `CUE` as distinct useful constructs. `EFGM-EXP-0006` is reserved for that semantic test using independently defined labels.

# 7. Other continuous candidates

```text
F_G  = F_T × GI
F_RA = (F_T × GI) / (1 + AE)
F_L  = clamp(w_t × F_T + w_g × GI - w_e × AE)
```

Coefficients are stored in the versioned candidate configuration. None is canonical.

# 8. Evidence discipline

All normalized inputs use `MetricObservation`:

```text
(value, status, rationale, evidence_refs, scorer_id, scorer_type, confidence)
```

Canonical states are:

```text
observed
inferred
unknown
not_applicable
```

```text
UNKNOWN != SAFE
0.00 != UNKNOWN
NOT_APPLICABLE != UNKNOWN
```

Unknown observations block completed scoring rather than silently becoming favorable values.

# 9. Candidate classification semantics

The v0.3 classifier is an experimental state description, not a risk probability.

Its regions are exhaustive and monotonic in the following sense:

1. elevated `AE` or `CUE` produces `Elevated uncontrolled-agency risk`;
2. otherwise `GI` determines governed versus governance-deficit state;
3. task flow determines high-flow versus low-flow substate.

Current labels are:

- `Governed autonomous operation`;
- `Governed but low-flow`;
- `High-flow governance deficit`;
- `Low-flow governance deficit`;
- `Elevated uncontrolled-agency risk`.

The configuration validator rejects internally dead/contradictory threshold relationships such as a CUE elevation threshold above the AE elevation threshold, because `CUE <= AE` by construction.

# 10. Benchmark v0.2 — Agentic Governance

The benchmark contains 132 controlled synthetic cases:

```text
66 preferred/mutated pairs
11 scenario families
88 development cases
44 validation cases
```

Families include boundary crossing, privilege accumulation, capability acquisition, credential propagation, environmental memory, emergent coordination, observability gaps, control recoverability, goal persistence, tool/environment adaptation, and coherent unsafe execution.

Inside each preferred/mutated pair, EFGM v2 task-flow observations are held constant. This asks whether governance dimensions add information beyond cognitive/task coherence.

The runner now records:

- frozen EFGM v2 baseline SHA;
- candidate config ID/hash;
- current code SHA when supplied by CI/environment;
- benchmark SHA;
- model directionality;
- AE/CUE construct-separation diagnostics.

Current synthetic results can establish construct responsiveness. They cannot establish external validity.

# 11. Temporal governance and recovery

A static score is insufficient for autonomous-agent governance.

```text
S_t
 ↓ agent action / environment change
S_t+1
 ↓ governance intervention
S_t+2
 ↓
Did governance regain control?
```

The temporal scaffold now distinguishes two research signals.

## Recovery progress

`recovery_progress_signal` requires:

- a valid `pre_intervention → post_intervention` transition;
- a declared intervention;
- higher `GI`;
- lower `AE`.

This means governance moved in the intended direction. It is **not** a recovery attestation.

## Verified recovery signal

`verified_recovery_signal` additionally requires:

- no remaining candidate-prerequisite breach;
- no elevated AE/CUE diagnostic;
- complete residual-state evidence;
- no material residual state marked present.

Residual-state surfaces currently include:

- credentials;
- persistence;
- environmental memory;
- coordination;
- privileges;
- scheduled actions;
- irreversible side effects;
- rollback gaps.

A residual state marked `unknown` prevents verified recovery. Clear/present states require evidence references in the research scaffold.

Even the verified signal is an experimental research result, **not** a production containment attestation.

`EFGM-EXP-0005` must falsify this logic using partial interventions, cached credentials, surviving persistence/memory, delegated peer goals, rollback gaps, trace loss, and delayed containment.

# 12. Scientific constraints

Current evidence status:

```text
controlled_synthetic_internal
```

Known limitations include:

- internal case authorship;
- EFGM-derived construct vocabulary;
- no sealed external holdout evaluation for Agent Governance v0.3;
- no independently authored agent labels yet;
- no proof that geometric aggregation is necessary;
- no proof that multiplicative interactions are necessary;
- no calibrated mapping from scores to incident probability;
- limited temporal evidence;
- reviewer confidence is recorded but not mathematically propagated.

Confidence propagation remains an explicit future experiment candidate and must not be silently folded into current scores.

# 13. Promotion rule

Agent Governance v0.3 may be promoted only if evidence shows reliable incremental value over:

- frozen EFGM v2;
- simpler EFGM-derived ablations;
- independent governance checklists;
- externally authored cases/labels;
- sealed holdout evidence.

Material counterexamples and rejected candidates must remain disclosed. Human review remains required before promotion.

## Current conclusion

Current evidence supports investigating a separate agent-governance construct space. It does **not** establish a canonical Agent Governance v0.3 formula.

The current distinctions are:

```text
EFGM v2 G = Grounding
Agent Governance v0.3 GI = Governance Integrity
AE = insufficiently governed agency exposure
CUE = coherent task execution through that exposure
```

The next research priorities are candidate-prerequisite falsification, independent AE/CUE semantic testing, and temporal intervention/recovery testing.
