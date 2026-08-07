# EFGM Validation Log

This log distinguishes exploratory tests from validation evidence. Exploratory/non-blinded results may generate hypotheses but must not be represented as independent scientific validation.

## 2026-05-21 — Initial Local Validation

Environment:

- Windows PowerShell
- Python 3.13.1
- pytest 9.0.3

Activities:

- installed the package in editable mode;
- ran the unit tests available at that time;
- ran the v1 weather-forecast demonstration.

Interpretation: implementation smoke test only.

## 2026-08-07 — Exploratory Model-Spec Mapping Pilot

Status: **exploratory / non-blinded / hypothesis-generating**.

A small five-family proof-of-concept compared EFGM v2 scoring behavior with externally documented desirable/undesirable response patterns from the public OpenAI Model Spec. Scenario families included:

- sycophancy;
- prompt injection / untrusted instructions;
- uncertainty calibration;
- coherent but ungrounded hallucination;
- ambiguous consequential action.

Observed exploratory pattern:

- EFGM ranked the intentionally spec-aligned candidate above the intentionally violating candidate in all five constructed pairs;
- dominant EFGM failure signals varied by scenario (behavioral entropy, output entropy/CRC, uncertainty calibration, grounding, and uncertainty/output entropy);
- score perturbation did not reverse those intentionally large pairwise separations in the exploratory setup.

Limitations:

- the EFGM scorer knew which candidate was intended to be preferred;
- metric values were assigned by the same analysis that constructed the comparison;
- the cases were not a random or representative Model Spec sample;
- the experiment therefore does **not** establish predictive validity.

Research consequence: proceed to blinded paired evaluation, inter-rater scoring, simpler baselines, ablation, and holdout testing rather than treating the pilot as confirmation.

## 2026-08-07 — Repository Stabilization Work

A dedicated research branch was created to prepare EFGM for autonomous falsification-oriented experimentation. The work includes:

- canonical v2 specification and scoring rubric;
- evidence-backed `MetricObservation` schema with legacy numeric compatibility;
- versioned external scoring weights/thresholds;
- critical grounding classification gate;
- expanded v2 invariant/edge-case tests;
- explicit DQ/CRC semantic separation and CRC range documentation;
- development/validation/holdout benchmark partitions;
- comparison-baseline requirements;
- experiment-manifest, counterexample, and rejected-candidate structure;
- v1 legacy documentation separation.

This stabilization work changes the research infrastructure and one classification safeguard. It does not claim the current mathematical form has been validated.
