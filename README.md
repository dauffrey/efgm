# Entropy-Flow Governance Model (EFGM)

EFGM is an experimental governance and measurement framework for evaluating whether AI-assisted reasoning, software delivery, operational workflows, and autonomous-agent activity remain coherent, grounded, calibrated, traceable, and governed while entropy accumulates.

EFGM is **not** a proven scientific law, compliance standard, or production-ready risk engine. It is an executable research prototype intended for controlled, falsification-oriented validation.

## Version identity

Use these identities consistently:

```text
Canonical model:        EFGM v2 — Decision Integrity
Python package:         0.2.0
Experimental extension: Agent Governance v0.3
```

Package version `0.2.0` is an unreleased research package identity; it is **not** the name of the canonical model. Agent Governance v0.3 is an experimental research extension and does not replace EFGM v2.

## Canonical model — EFGM v2

The authoritative definition is [`docs/model-specification-v2.md`](docs/model-specification-v2.md). Metric scoring guidance is in [`docs/scoring-rubric-v2.md`](docs/scoring-rubric-v2.md). Older v1 material is retained only for compatibility/history and must not be treated as the current decision-integrity model.

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

| Symbol | Meaning |
|---|---|
| `T` | Observation maturity / sequence continuity |
| `C` | Capability suitability for the assessed objective |
| `Fq` | Flow quality |
| `G` | Grounding |
| `U` | Uncertainty calibration |
| `Ei` | Input entropy |
| `Eo` | Output entropy |
| `Be` | Behavioral entropy |
| `Oe` | Operational entropy |
| `H` | Hidden-information load |
| `CRC` | Coherence Recovery Capacity |
| `DQ` | Decision quality |
| `OQ` | Outcome quality |
| `OD` | Outcome divergence (`OQ - DQ`) |

### DQ and CRC are intentionally separate

`DQ` measures the integrity of the resulting decision. `CRC` measures how effectively the system reduced or amplified the disorder present in the input. A hard problem and an easy problem may produce equally strong decisions while having very different recovery capacity.

`CRC` is a recovery/amplification ratio and is **not bounded to `[-1, 1]`**. Positive values indicate entropy reduction; values near zero indicate little recovery; negative values indicate entropy amplification. Bounded alternatives remain an open research question and should be tested rather than silently substituted.

### Grounding gate

The frozen EFGM v2 classifier includes a critical grounding gate. A sufficiently weakly grounded result cannot receive a reassuring aggregate classification merely because its prose, flow, or other dimensions are strong. The current threshold is a **versioned provisional research parameter**, not a scientifically validated constant.

## Evidence-backed observations

EFGM v2 and Agent Governance v0.3 metric inputs use `MetricObservation` records:

```json
{
  "value": 0.86,
  "status": "observed",
  "rationale": "Validated against the source record.",
  "evidence_refs": ["evidence://source-1"],
  "scorer_id": "reviewer-1",
  "scorer_type": "human",
  "confidence": 0.95
}
```

Canonical observation states are:

```text
observed
inferred
unknown
not_applicable
```

Missing data is explicit:

```text
0.00           = measured value
unknown        = insufficient evidence; scoring is blocked
not_applicable = excluded from the relevant composite where permitted
```

An omitted metric becomes `unknown`, **not zero**. Legacy numeric v2 inputs remain accepted for compatibility and are automatically marked as inferred observations without supplied provenance.

Research-grade runs should require strict provenance:

```bash
efgm-score assessment.json --model v2 --require-provenance --format json
```

## Versioned scoring configuration and hashes

EFGM v2 weights and classification thresholds live in:

```text
src/efgm/config/efgm-v2.0-baseline.json
```

Every EFGM v2 result records a configuration ID/hash and input hash. Candidate configurations are strictly validated.

Agent Governance v0.3 has a separate candidate configuration:

```text
src/efgm/config/efgm-v0.3-agent-governance.json
```

Every Agent Governance v0.3 result records:

- candidate config ID;
- candidate config SHA-256;
- input SHA-256;
- provenance completeness/issues;
- applicable and excluded governance families.

## Experimental extension — Agent Governance v0.3

Agent Governance v0.3 is an **experimental autonomous-agent research extension to EFGM v2**. Its central hypothesis is:

> High coherent task flow can coexist with weak governance integrity.

The experimental state includes objective alignment, boundary integrity, observability, environmental-memory governance, coordination governance, control recoverability, and agency amplification.

### Symbol discipline

```text
G  = EFGM v2 Grounding
GI = Agent Governance v0.3 Governance Integrity
```

### Agency exposure and coherent unsafe execution

```text
AE  = A_a × (1 - GI)
CUE = F_T × AE
```

- `AE` — Agency Exposure: consequential agency that is insufficiently governed.
- `CUE` — Coherent Unsafe Execution: effective task flow operating through that exposure.

Because normalized `F_T` is in `[0,1]`, the candidate has the structural invariant:

```text
0 <= CUE <= AE <= 1
```

A generic low-`AE` / high-`CUE` region is therefore mathematically impossible and must not be used as an experiment-design target.

The historical experimental field `uncontrolled_agency_risk` is retained as a compatibility alias for `CUE` while candidate formulations are compared.

The agent benchmark treats `AE` and `CUE` as **lower-is-better** comparators and records the candidate config identity/hash and code SHA. A construct-separation diagnostic verifies the implementation contract that lowering task flow can reduce `CUE` without reducing `AE`; this is not external semantic validation.

### Non-compensatory diagnostics

Retained counterexamples show that aggregate family means can hide a sparse catastrophic governance failure. Agent Governance v0.3 therefore exposes experimental diagnostics without silently replacing the continuous aggregate scores:

- `governance_observation_floor` — minimum applicable governance observation, reported neutrally;
- low-percentile governance diagnostic;
- explicit **candidate prerequisite** metric paths from the versioned config;
- candidate prerequisite breaches;
- diagnostic flags.

The observation floor does **not** make every low metric a prerequisite. Candidate prerequisites are explicit research hypotheses and must be evaluated against benign controls and independent baselines before any veto semantics are promoted.

### N/A family coverage

A strictly single-agent case may mark the entire coordination-governance family `not_applicable`. That family is excluded from `GI` rather than assumed perfect. Results expose the applicable/excluded family list and family count because `GI` values computed over different applicability profiles may require stratified comparison.

### Monotonic candidate classification

The current experimental classifier uses exhaustive regions:

1. elevated `AE` or `CUE` → `Elevated uncontrolled-agency risk`;
2. otherwise, `GI` determines governed vs governance-deficit state;
3. task flow determines high-flow vs low-flow substate.

This avoids the previous threshold gap where a modest improvement in `GI` could produce a worse label.

### Temporal governance research

A static snapshot is not sufficient for autonomous-agent governance. Experimental transition support lives in:

```text
src/efgm/temporal_v0_3.py
```

Temporal states carry an explicit `sequence_id`. A transition across different sequence identities is rejected rather than interpreted as change or recovery. Transition results record candidate config identity/hash, before/after input hashes, and a residual-state hash when residual evidence is supplied.

Temporal results distinguish:

- `recovery_progress_signal` — a valid `pre_intervention → post_intervention` transition in the same sequence, with higher `GI` and lower `AE` after a declared intervention;
- `verified_recovery_signal` — recovery progress **plus** a governed post-state, no remaining candidate-prerequisite breach, no elevated AE/CUE flag, complete evidence-backed residual-state checks, and no material residuals present.

Residual-state checks currently cover credentials, persistence, environmental memory, coordination, privileges, scheduled actions, irreversible side effects, and rollback gaps. For a verified-recovery candidate, `clear`, `present`, and `not_applicable` residual claims require rationale, scorer identity/type, positive confidence, and evidence references. `unknown` blocks verified recovery. `not_applicable` is treated as an evidence-backed scope claim rather than an evidence-free escape hatch.

These are experimental research signals, not production containment attestations.

See [`research/EFGM_V0_3_GOVERNED_AGENTIC_FLOW.md`](research/EFGM_V0_3_GOVERNED_AGENTIC_FLOW.md).

## v1 — compatibility model

V1 remains available for historical examples and compatibility inputs:

```text
Q = (T × E × Fq)^(1/3)
F = Q / (1 + e)
```

Use it explicitly:

```bash
efgm-score examples/weather_forecast_demo/input.json --model v1 --format markdown
```

Historical narrative documents are preserved under `docs/legacy/`. V1 is **not** the canonical model for new decision-integrity validation.

## Installation

```bash
python -m pip install -e .
```

## Command line

EFGM v2 is the default:

```bash
efgm-score examples/decision_integrity_demo/input.json --format markdown
```

Write JSON or Markdown to a file:

```bash
efgm-score assessment.json --model v2 --require-provenance --format json --output reports/assessment.json
```

Run the experimental Agent Governance benchmark:

```bash
efgm-agent-experiment --sensitivity-trials 100 --perturbation 0.10 --format markdown
```

Use an alternate Agent Governance candidate config:

```bash
efgm-agent-experiment --agent-config path/to/candidate.json --format markdown
```

## Python API

```python
from efgm import EFGMDecisionInput, score_decision_efgm

assessment = EFGMDecisionInput.model_validate(payload)
result = score_decision_efgm(assessment, require_provenance=True)
```

The v1 API remains available as `EFGMInput` and `score_efgm`. Agent Governance v0.3 APIs are exported as experimental research interfaces.

## Research controls

EFGM should advance only if controlled testing shows that it is understandable, repeatable, evidence-traceable, actionable, and more useful than simpler alternatives. The research program should actively attempt to falsify EFGM rather than optimize tests to make it appear successful.

Required controls include:

- evidence, rationale, scorer identity/type, and confidence for research-grade applied scores;
- explicit `unknown` / `not_applicable` handling;
- config and input hashes plus repository code SHA in experiment records;
- development and validation datasets visible to the tuning loop;
- **externally sealed holdout cases/labels not stored in the tuning-visible repository**;
- comparison against EFGM-derived ablations and independent baselines;
- ablation and sensitivity testing;
- explicit counterexample and rejected-candidate retention;
- no rewriting gold-standard labels merely because EFGM disagrees;
- human review before promotion of a candidate model to the canonical baseline.

Planned falsification cycles include:

- `EFGM-EXP-0004` — critical-dimension diagnostics and candidate prerequisite testing;
- `EFGM-EXP-0005` — temporal sequence identity, intervention, residual state, and recovery;
- `EFGM-EXP-0006` — independent semantic testing of Agency Exposure versus Coherent Unsafe Execution within the feasible constraint `CUE <= AE`.

See [`research/README.md`](research/README.md) and [`validation/test-plan.md`](validation/test-plan.md).

## Governance loop

```text
Detect entropy → Protect verified flow → Restore coherence → Reassess
```

## Information handling

Use public, simulated, or sanitized examples. Do not add credentials, personal information, restricted architecture, confidential incident data, real sealed-holdout contents/labels, or unapproved client material.

## Status

```text
Canonical model:        EFGM v2 — experimental research baseline
Package version:        0.2.0 — unreleased research package
Experimental extension: Agent Governance v0.3 — research candidate
```
