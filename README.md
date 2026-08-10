# Entropy-Flow Governance Model (EFGM)

EFGM is an experimental governance and measurement framework for evaluating whether AI-assisted reasoning, software delivery, operational workflows, and autonomous-agent activity remain coherent, grounded, calibrated, traceable, and governed while entropy accumulates.

EFGM is **not** a proven scientific law, compliance standard, or production-ready risk engine. It is an executable research prototype intended for controlled, falsification-oriented validation.

## Canonical model

**EFGM v2 is the primary research baseline in package version `0.2.0`.** There are currently no repository tags or releases establishing a stable public Python API; `0.2.0` is an unreleased research baseline.

The authoritative v2 definition is [`docs/model-specification-v2.md`](docs/model-specification-v2.md). Metric scoring guidance is in [`docs/scoring-rubric-v2.md`](docs/scoring-rubric-v2.md). Older v1 material is retained only for compatibility/history and must not be treated as the current decision-integrity model.

### v2 — Decision integrity model

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

The baseline v2 classifier includes a critical grounding gate. A sufficiently weakly grounded result cannot receive a reassuring aggregate classification merely because its prose, flow, or other dimensions are strong. The current threshold is a **versioned provisional research parameter**, not a scientifically validated constant.

## Evidence-backed observations

V2 and experimental v0.3 metric inputs use `MetricObservation` records:

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

V2 weights and classification thresholds live in:

```text
src/efgm/config/efgm-v2.0-baseline.json
```

Candidate configs are strictly validated. Every v2 result records:

- human-readable `config_id`;
- SHA-256 of the canonicalized scoring configuration;
- SHA-256 of the canonicalized input assessment;
- provenance completeness and any provenance issues.

This prevents two different parameter files from masquerading as the same experiment merely because they reuse a config name.

Use an alternate candidate configuration with:

```bash
efgm-score assessment.json --model v2 --config path/to/candidate.json --require-provenance --format json
```

## Experimental v0.3 — Governed Agentic Flow

EFGM v0.3 is an **experimental autonomous-agent research candidate**. It does not modify or replace the frozen v2 baseline.

Its central hypothesis is:

> High coherent task flow can coexist with weak governance integrity.

The experimental state includes objective alignment, boundary integrity, observability, environmental-memory governance, coordination governance, control recoverability, and agency amplification.

### Symbol discipline

Canonical v2 reserves:

```text
G = Grounding
```

Experimental v0.3 uses:

```text
GI = Governance Integrity
```

### Agency exposure and coherent unsafe execution

The experimental v0.3 candidate now separates:

```text
AE  = A_a × (1 - GI)
CUE = F_T × AE
```

- `AE` — Agency Exposure: consequential agency that is insufficiently governed.
- `CUE` — Coherent Unsafe Execution: effective task flow operating through that exposure.

The historical v0.3 result field `uncontrolled_agency_risk` is retained as a compatibility alias for `CUE` while candidate formulations are compared.

The v0.3 parameters are versioned independently in:

```text
src/efgm/config/efgm-v0.3-agent-governance.json
```

Every v0.3 result records the candidate config ID and SHA-256.

### Non-compensatory diagnostics

Retained counterexamples show that aggregate family means can hide a single catastrophic governance failure. The v0.3 scorer therefore exposes experimental diagnostics without changing the continuous aggregate scores:

- governance prerequisite floor;
- low-percentile governance diagnostic;
- explicit prerequisite breaches;
- diagnostic flags.

These diagnostics are research candidates. They do not yet override the aggregate v0.3 classification.

### Temporal governance research

A static snapshot is not sufficient for autonomous-agent governance. Experimental transition support lives in:

```text
src/efgm/temporal_v0_3.py
```

It compares changes in `GI`, `AE`, and `CUE` before and after agent actions or governance interventions. The initial recovery signal is deliberately narrow and is not proof that all residual state has been removed.

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

Full historical v1 documents are preserved under `docs/legacy/v1/` for reproducible comparison. V1 is **not** the canonical model for new decision-integrity validation.

## Installation

```bash
python -m pip install -e .
```

## Command line

V2 is the default:

```bash
efgm-score examples/decision_integrity_demo/input.json --format markdown
```

Write JSON or Markdown to a file:

```bash
efgm-score assessment.json --model v2 --require-provenance --format json --output reports/assessment.json
```

Run the experimental agent-governance benchmark:

```bash
efgm-agent-experiment --sensitivity-trials 100 --perturbation 0.10 --format markdown
```

## Python API

```python
from efgm import EFGMDecisionInput, score_decision_efgm

assessment = EFGMDecisionInput.model_validate(payload)
result = score_decision_efgm(assessment, require_provenance=True)
```

The v1 API remains available as `EFGMInput` and `score_efgm`.

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

- `EFGM-EXP-0004` — critical governance prerequisite/low-percentile diagnostics;
- `EFGM-EXP-0005` — temporal intervention and recovery.

See [`research/README.md`](research/README.md) and [`validation/test-plan.md`](validation/test-plan.md).

## Governance loop

```text
Detect entropy → Protect verified flow → Restore coherence → Reassess
```

## Information handling

Use public, simulated, or sanitized examples. Do not add credentials, personal information, restricted architecture, confidential incident data, real sealed-holdout contents/labels, or unapproved client material.

## Status

Current status: **experimental v0.2 research baseline with an experimental v0.3 autonomous-agent research track**.
