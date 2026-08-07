# EFGM v2 Model Specification

## Status and authority

This document is the **canonical specification** for the EFGM v2 decision-integrity research baseline in package version `0.2.0`.

If another repository document conflicts with this specification, this document and the executable v2 implementation take precedence until the conflict is resolved. V1 documents are historical/compatibility material.

EFGM v2 is experimental. Its constructs, equations, weights, and thresholds are hypotheses to be tested, not established scientific constants.

## Research objective

EFGM v2 evaluates whether a decision process preserves coherent, grounded, calibrated, and operationally reliable flow while facing uncertainty, contradiction, incomplete information, behavioral pressure, and execution disturbance.

The model deliberately separates:

1. conditions present in the input;
2. degradation introduced or retained in the output;
3. positive decision-quality factors;
4. behavioral and operational degradation;
5. the quality of the decision itself;
6. the quality of the eventual outcome.

## Variables

| Symbol | Definition | Direction |
|---|---|---|
| `T` | Observation maturity / sequence continuity | higher is better |
| `C` | Capability suitability for the assessed objective | higher is better |
| `Fq` | Flow quality | higher is better |
| `G` | Grounding | higher is better |
| `U` | Uncertainty calibration | higher is better |
| `Ei` | Input entropy | higher is worse input condition |
| `Eo` | Output entropy | higher is worse output condition |
| `Be` | Behavioral entropy | higher is worse |
| `Oe` | Operational entropy | higher is worse |
| `H` | Hidden-information load | higher means less outcome certainty |
| `CRC` | Coherence Recovery Capacity | positive is recovery; negative is amplification |
| `Q` | Positive-factor quality composite | higher is better |
| `DQ` | Decision quality | higher is better |
| `OQ` | Outcome quality | higher is better |
| `OD` | Outcome divergence (`OQ - DQ`) | descriptive, not inherently good/bad |

All base observations are normalized to `[0, 1]`. `CRC` and `OD` are derived values and are not constrained to that same interpretation.

## Equations

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

The baseline weights and thresholds are versioned in `src/efgm/config/efgm-v2.0-baseline.json`.

## Input entropy

```text
Ei = w1*IC + w2*IA + w3*IG + w4*MC + w5*H
```

| Metric | Meaning |
|---|---|
| `IC` | Input contradiction |
| `IA` | Input ambiguity |
| `IG` | Input goal conflict |
| `MC` | Missing context |
| `H` | Hidden-information load |

Input entropy describes the difficulty/disorder presented to the decision process. It does **not** directly penalize `DQ` in the baseline. Instead, it provides the reference state from which recovery can be measured.

## Output entropy

```text
Eo = w1*OC + w2*UM + w3*GD + w4*RI + w5*CD
```

| Metric | Meaning |
|---|---|
| `OC` | Output contradiction |
| `UM` | Uncertainty mismatch |
| `GD` | Goal drift |
| `RI` | Reasoning instability |
| `CD` | Context decay |

Output entropy directly degrades `DQ`.

## Flow quality

`Fq` measures coherent progression toward the intended objective through task completion consistency, reasoning continuity, semantic coherence, and verification success rate.

## Grounding

`G` measures whether an apparently coherent result is actually supported by valid rules/evidence and remains factually/domain consistent.

Grounding is separate from semantic coherence because a fluent, internally consistent answer can still be invented or false.

Baseline grounding metrics:

- rule support;
- evidence validity;
- traceability;
- factual consistency;
- domain calibration.

## Uncertainty calibration

`U` measures whether expressed confidence is proportionate to evidence. High confidence with weak evidence should score poorly even if the response is otherwise fluent.

## Behavioral entropy

`Be` captures decision distortion arising from feedback pressure rather than ordinary semantic inconsistency:

- chasing behavior;
- outcome bias;
- sunk-cost pressure;
- false pattern detection;
- overconfidence feedback.

## Operational entropy

`Oe` captures execution degradation that can reduce decision reliability even when reasoning is sound:

- timeout rate;
- retry instability;
- tool failure rate;
- latency pressure;
- workflow interruption.

## DQ versus CRC

These constructs are intentionally different.

### Decision Quality (`DQ`)

`DQ` measures the integrity of the resulting decision after accounting for positive factors and degradation introduced/retained in the decision process.

### Coherence Recovery Capacity (`CRC`)

`CRC` measures how much of the input disorder was removed or amplified:

```text
CRC = (Ei - Eo) / max(Ei, ε)
```

- positive `CRC`: the process reduced entropy;
- near-zero `CRC`: little net recovery;
- negative `CRC`: the process amplified entropy.

The baseline `CRC` is intentionally unbounded below. For example, a low-entropy input followed by a highly disordered output can produce a value below `-1`. Bounded alternatives are legitimate candidate models but must be evaluated experimentally rather than substituted silently.

## Outcome separation

EFGM v2 explicitly rejects the assumption that decision quality and outcome quality are identical.

```text
Good decision != guaranteed good outcome
Bad decision != guaranteed bad outcome
```

`OQ` is observed after the fact. `OD = OQ - DQ` helps identify favorable or unfavorable variance, hidden information, or possible model misspecification.

`OutcomeConfidence = DQ * (1 - H)` reduces confidence in outcome expectations when hidden information is high without automatically declaring the decision itself poor.

## Classification

The baseline classifier is a provisional governance interpretation layer, not a scientific law. Exact thresholds live in the versioned scoring configuration.

A critical grounding gate is applied before ordinary `DQ` bands so a severely weakly grounded result cannot be labeled stable merely because other aggregate dimensions are strong.

Current labels are:

- Coherent and grounded
- Coherent but weakly grounded
- Weakly grounded - verification required
- Stable with watch items
- Degraded but usable
- High entropy
- Misaligned

Thresholds must be evaluated against blinded validation evidence and may only change through a versioned candidate configuration.

## Observation provenance

Each research-grade metric should be represented by a `MetricObservation` containing:

- normalized value;
- observation status;
- rationale;
- evidence references;
- scorer identity;
- scorer type;
- scorer confidence;
- timestamp when available.

Raw numeric v2 inputs are accepted only for compatibility and are automatically identified as inferred observations without supplied provenance.

## Scope limits

EFGM v2 must not be represented as:

- proof of objective truth;
- a validated physical law;
- an autonomous compliance decision engine;
- a replacement for domain experts;
- a substitute for security, safety, privacy, architecture, or regulatory review.

## Falsification requirement

A proposed EFGM improvement is not accepted merely because it raises scores or fixes a known example. Candidate models must be compared against the frozen baseline, simpler baselines, counterexamples, and data not used for tuning. Sealed holdouts must not be exposed to the tuning loop.
