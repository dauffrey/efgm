# Entropy-Flow Governance Model (EFGM)

EFGM is an experimental governance framework for evaluating whether AI-assisted reasoning, software delivery, and operational workflows remain coherent, grounded, calibrated, and traceable while entropy accumulates.

EFGM is not a proven scientific law, trained AI model, compliance standard, or production-ready risk engine. It is an executable research prototype intended for controlled validation.

## Model versions

### v2 — Decision integrity model

v2 is the primary model in package version `0.2.0`. It separates input conditions, output degradation, grounding, uncertainty calibration, behavioural effects, operational effects, decision quality, and outcome variance.

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
| `T` | Continuity or observation maturity |
| `C` | Capability or suitability of tools/rules |
| `Fq` | Flow quality |
| `G` | Grounding |
| `U` | Uncertainty calibration |
| `Ei` | Input entropy |
| `Eo` | Output entropy |
| `Be` | Behavioural entropy |
| `Oe` | Operational entropy |
| `H` | Hidden-information load |
| `CRC` | Coherence recovery capacity |
| `DQ` | Decision quality |
| `OQ` | Outcome quality |
| `OD` | Outcome divergence (`OQ - DQ`) |

### v1 — Coherent-flow compatibility model

v1 remains available for existing inputs and demonstrations.

```text
Q = (T × E × Fq)^(1/3)
F = Q / (1 + e)
```

The geometric mean is the implemented v1 formula. The earlier raw-product expression is retained only as historical context and is not used by the package.

## Installation

```bash
python -m pip install -e .
```

## Command line

v2 is the default:

```bash
efgm-score examples/decision_integrity_demo/input.json --format markdown
```

Select v1 explicitly for compatibility inputs:

```bash
efgm-score examples/weather_forecast_demo/input.json --model v1 --format markdown
```

Write JSON or Markdown to a file:

```bash
efgm-score assessment.json --model v2 --format json --output reports/assessment.json
```

## Python API

```python
from efgm import EFGMDecisionInput, score_decision_efgm

assessment = EFGMDecisionInput.model_validate(payload)
result = score_decision_efgm(assessment)
```

The v1 API remains available as `EFGMInput` and `score_efgm`.

## Governance loop

```text
Detect entropy → Protect verified flow → Restore coherence
```

## Validation expectations

Every applied score should eventually be backed by evidence, rationale, scorer identity, observation status, and confidence. Numeric output is a governance indicator, not exact truth.

EFGM should advance only if controlled testing shows that it is understandable, repeatable, evidence-traceable, actionable, and more useful than informal review or a simpler checklist. It should be simplified or retired if reviewers cannot score it consistently, it creates false confidence, or it does not add practical value.

See:

- `docs/EFGM_v0.2_recommendations.md` for the v2 formula reference
- `validation/test-plan.md` for the validation approach
- `examples/decision_integrity_demo/` for a v2 input
- `examples/weather_forecast_demo/` for a v1 compatibility input

## Information handling

Use public, simulated, or sanitized examples. Do not add credentials, personal information, restricted architecture, confidential incident data, or unapproved client material.

## Status

Current status: **experimental v0.2 research prototype**.
