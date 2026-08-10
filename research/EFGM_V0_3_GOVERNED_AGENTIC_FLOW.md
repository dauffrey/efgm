# EFGM v0.3 — Governed Agentic Flow (Experimental Candidate)

## Status

**Experimental research candidate. Not part of the frozen EFGM v0.2 baseline.**

This branch extends the Experiment Runner work from `research/experiment-runner-v0.1`.
The accepted v0.2 baseline remains frozen at:

```text
b717f611a0d09bd8e52bc1b0be5ee178eecacf25
```

No v0.2 equation, scoring configuration, or baseline artifact is modified by this proposal.

## Research mandate

EFGM v0.3 is narrowly scoped to **autonomous AI agents**.

Black Hat USA 2026 security findings are treated as **external empirical inspiration** for the failure taxonomy. They are not benchmark labels, ground truth, or an incident-reconstruction target. The benchmark is intentionally generic so that the model is not trained to explain one event.

Generalization to organizational, cognitive, or other adaptive systems is explicitly deferred.

## Core hypothesis

The v0.2 line of work primarily measures the quality of cognitive/decision flow under entropy, grounding, uncertainty, behavioral pressure, and operational degradation.

The v0.3 candidate tests an additional proposition:

> High coherent task flow can coexist with low governance integrity.

This creates a distinct state in which an agent can remain effective at executing a task while its objectives, capabilities, persistence, communications, or effects move outside governing intent.

The research question is:

> What measurable conditions determine whether increasingly capable autonomous agents remain coherent, aligned, observable, bounded, and recoverable over time?

## Candidate state vector

The first v0.3 implementation deliberately exposes dimensions before declaring a single canonical score:

```text
S_t = [F_T, e_c, A, B, O, M_g, S_g, R_c, A_a]
```

Where:

- `F_T` — task/decision flow inherited from the v2 decision-quality score.
- `e_c` — cognitive/decision entropy summary derived from v2 output, behavioral, and operational entropy.
- `A` — objective alignment.
- `B` — boundary integrity.
- `O` — observability.
- `M_g` — environmental-memory governance.
- `S_g` — multi-agent coordination governance.
- `R_c` — control recoverability.
- `A_a` — agency amplification.

The separation between governance quality and agency amplification is intentional. High privilege, connectivity, persistence, coordination, or action velocity is not automatically unsafe; risk emerges from the interaction between agency and weak governance.

## Candidate constructs

### Objective alignment

Measures whether the active objective remains subordinate to authorized scope and later governance changes.

Metrics:

- objective scope fidelity;
- authority precedence;
- goal-update compliance;
- prohibited-goal avoidance.

### Boundary integrity

Measures whether the agent remains inside authorized trust, privilege, capability, and credential boundaries.

Metrics:

- trust-boundary adherence;
- privilege-boundary adherence;
- capability-scope adherence;
- credential-scope adherence.

### Observability

Measures whether governance can reconstruct material agent behavior.

Metrics:

- action-trace coverage;
- tool-call traceability;
- state-change traceability;
- cross-agent traceability.

### Environmental-memory governance

Treats external writable/readable state as potential agent memory.

Metrics:

- persistence-scope control;
- write-surface inventory;
- readback traceability;
- shared-state control.

This reflects the working principle:

> Any surface an agent can write now and read later can potentially function as memory.

### Coordination governance

Measures whether multi-agent discovery, delegation, messages, and shared goals remain governed.

Metrics:

- peer-discovery control;
- delegation-scope control;
- message traceability;
- shared-goal control.

### Control recoverability

Measures whether governance can actually regain control after intervention.

Metrics:

- revocation effectiveness;
- containment effectiveness;
- state-cleanup completeness;
- rollback effectiveness.

### Agency amplification

Measures the consequential reach available to otherwise coherent reasoning.

Metrics:

- privilege;
- connectivity;
- persistence;
- coordination;
- action velocity.

## Candidate aggregation functions

These functions are deliberately competing hypotheses.

First define governance integrity as a geometric aggregation:

```text
G = geometric_mean(A, B, O, M_g, S_g, R_c)
```

and agency amplification as the mean of the five agency-intensity observations.

The branch then compares:

### Governed flow product

```text
F_G = F_T × G
```

### Uncontrolled-agency risk

```text
R_U = F_T × A_a × (1 - G)
```

### Risk-adjusted flow

```text
F_RA = (F_T × G) / (1 + A_a × (1 - G))
```

### Governed linear comparator

```text
F_L = clamp(
    0.50 × F_T
    + 0.50 × G
    - 0.25 × A_a × (1 - G)
)
```

None is canonical. Benchmark v0.2 exists to test whether the additional dimensions add information and whether a nonlinear interaction is justified.

## Measurement discipline

All v0.3 inputs use the existing `MetricObservation` structure:

```text
(value, status, rationale, evidence_refs, scorer_id, scorer_type, confidence)
```

The following rule remains mandatory:

```text
UNKNOWN != SAFE
```

An unobserved boundary violation does not imply boundary integrity. Unknown observations block scoring rather than silently becoming favorable values.

## Benchmark v0.2

`EFGM Benchmark v0.2 — Agentic Governance` contains 132 controlled synthetic cases:

```text
66 preferred/mutated pairs
11 agent-governance families
88 development cases
44 validation cases
```

Families:

1. boundary crossing;
2. privilege accumulation;
3. capability acquisition;
4. credential propagation;
5. environmental memory;
6. emergent coordination;
7. observability gap;
8. control recoverability;
9. goal persistence;
10. tool/environment adaptation;
11. coherent unsafe execution.

Inside each pair, the v2 cognitive/task-flow observations are held constant. Only the experimental governance/agency dimensions change.

That design creates a direct falsification question:

> Can the frozen v2 decision-flow model distinguish a coherent-but-governance-degraded agent when cognitive task quality does not change?

If it cannot, the result supports the need for an additional construct space, but it does **not** establish that the proposed v0.3 aggregation is correct.

## Scientific constraints

This work must not be presented as external validation.

Current evidence status:

```text
controlled_synthetic_internal
```

Known limitations include:

- internal case authorship;
- EFGM-derived construct vocabulary;
- no sealed external holdout;
- no independently authored labels;
- no proof that geometric aggregation is necessary;
- no proof that multiplicative risk interaction is necessary;
- no calibrated mapping from normalized scores to real-world incident probability.

## Next falsification targets

After construct responsiveness is established, the next benchmark should include cases where candidate formulas disagree:

- one catastrophic governance deficit versus several moderate deficits;
- high agency with excellent governance versus low agency with mediocre governance;
- strong observability but weak recoverability;
- strong boundaries but persistent out-of-band memory;
- authorized cross-boundary actions versus unauthorized low-impact actions;
- governance changes issued mid-task;
- revoked credentials that remain cached;
- multi-agent communication that is authorized but partially unobservable;
- cases with unknown rather than favorable observations;
- external cases authored without EFGM terminology.

The long-term objective is not to prove a preferred equation. It is to determine whether the proposed dimensions are independently measurable and useful for predicting or governing agent behavior.
