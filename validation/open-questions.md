# EFGM v2 Open Research Questions

## Purpose

This document tracks unresolved questions for the canonical v2 decision-integrity model. These are research questions, not assumptions to be silently resolved by tuning.

## Construct validity

- Are `Fq`, `G`, and `U` empirically distinguishable, or do reviewers treat them as the same general quality judgment?
- Are `Eo` and `Be` separable in practice?
- Is `Oe` an independent decision-integrity construct or primarily an execution-reliability measure that should sit downstream of DQ?
- Does `Ei` contain distinct information beyond the individual input conditions and `H`?
- Does `CRC` explain successful recovery beyond simply reporting `Eo`?

## T — observation maturity

- Does `T` improve prediction or mainly act as a reviewer confidence proxy?
- Should `T` be omitted for single-shot decisions?
- How should stale longitudinal evidence affect `T`?
- Is a separate evidence-maturity construct preferable?

## C — capability suitability

- Can reviewers assess `C` reliably without contaminating it with observed outcome quality?
- Should tool access, domain expertise, and process readiness remain one construct?
- Can higher capability sometimes increase risk by accelerating unverified output, and if so is that captured elsewhere?

## Weighting and aggregation

- Does the geometric mean outperform an arithmetic or learned combination on unseen cases?
- Are the current v2 weights materially better than equal weights?
- Are additive entropy penalties appropriate, or do interaction/threshold effects predict failures better?
- Should any factors be gates rather than continuous multipliers?
- Do domain-specific weights improve generalization or create overfitting?

## Grounding gate

- What threshold best reduces false reassurance without creating excessive false alarms?
- Should the gate use aggregate `G` or specific critical submetrics such as evidence validity/factual consistency?
- Should a result with very weak traceability but strong external factual correctness be gated?

## CRC

The current baseline uses:

```text
CRC = (Ei - Eo) / max(Ei, epsilon)
```

Open questions:

- Is the unbounded negative range useful as an entropy-amplification ratio or confusing in governance reporting?
- Does a bounded alternative improve interpretability without losing predictive information?
- Should CRC be normalized by problem difficulty or compared within scenario families?
- Should CRC remain separate from DQ? The current hypothesis is yes.

## Observation provenance and missing data

The **current baseline behavior is now fixed for research reproducibility**:

```text
unknown        => completed scoring blocked
not_applicable => excluded and remaining weights renormalized
measured 0.00  => valid numeric observation
```

Remaining research questions:

- Should a future model probabilistically marginalize unknown dimensions rather than block scoring?
- Should uncertainty over a metric's value be propagated mathematically rather than recorded only as scorer confidence?
- How much confidence should be required before an inferred observation can influence a high-stakes assessment?
- Can evidence quality itself be scored without creating recursive scoring complexity?
- Does strict provenance improve inter-rater/predictive validity enough to justify its added assessment burden?

## Outcome model

- Does `OutcomeConfidence = DQ * (1 - H)` calibrate meaningfully against repeated outcomes?
- Is `OD = OQ - DQ` sufficient to distinguish luck/variance from model misspecification?
- What additional evidence is needed before interpreting persistent negative OD as a failure in the decision model?

## Behavioral entropy

- Are chasing behavior, outcome bias, sunk-cost pressure, false pattern detection, and overconfidence feedback reliably detectable by blinded reviewers?
- Do these variables predict errors beyond grounding and calibration?
- Are some of these causal mechanisms rather than metrics and therefore better represented differently?

## Operational entropy

- Should timeouts, retries, tool failures, latency pressure, and interruptions reduce DQ directly or instead reduce a separate execution-reliability construct?
- How should partial tool failure be separated from poor capability `C`?

## Classification

- Do discrete labels add decision value beyond the continuous metrics?
- Are the bands stable across domains?
- What false reassurance / false alarm trade-off is acceptable?
- Should classification be domain/risk-specific while DQ remains common?

## Baseline independence

- Do EFGM-derived ablations overstate apparent advantage because they share EFGM observations?
- How does EFGM compare against an independently defined direct checklist?
- Which task-specific or external statistical baselines are appropriate by domain?

## Holdout methodology

- What external custody mechanism is practical while still allowing automated evaluation of a frozen candidate?
- How frequently must holdouts be refreshed after exposure?
- How can holdout access be independently logged/verified?

## Scientific differentiation

- Does EFGM add measurable value beyond a simple checklist?
- Does v2 outperform v1 on unseen cases?
- Does v2 outperform a two-factor grounding + calibration baseline?
- Which dimensions survive ablation?
- Can independent researchers reproduce scoring and ranking results?
- Does performance hold on external datasets not designed around EFGM terminology?

## Model scope

- Is EFGM best positioned as a decision-integrity measurement framework, a governance assessment protocol, or both?
- Which domains demonstrate enough incremental value to justify the scoring burden?
- Where should EFGM explicitly not be used?

These questions should be answered with experiments where feasible. A question must not be marked resolved solely because a preferred narrative seems plausible.
