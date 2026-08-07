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

## 2026-08-07 — Draft PR #5 Independent Review Corrections

Status: **repository/research-control hardening; not model validation**.

A second-pass review identified several ways the initial stabilization could bias or weaken autonomous experiments. The branch was corrected before merge:

- omitted metric observations now become explicit `unknown` values rather than favorable zero defaults;
- `unknown` blocks completed scoring; explicit `not_applicable` observations are excluded with weight renormalization;
- research-grade provenance can be enforced with `require_provenance=True`;
- result artifacts now include canonical input/configuration SHA-256 hashes and provenance status;
- candidate configuration validation now rejects malformed metric keys, negative/non-finite weights, non-normalized weight sets, invalid epsilon/schema versions, and invalid classification thresholds;
- real holdout contents/labels are prohibited from the tuning-visible repository and require external custody/access control;
- verbatim v1 model, metric, and validation documents were preserved from the PR base commit under `docs/legacy/v1/`;
- baseline documentation now separates EFGM-derived ablations from an independent direct checklist comparator;
- CI was expanded to test strict-provenance scoring, Python 3.13, and the built wheel outside the source tree so packaged configuration data is verified.

Interpretation: these changes reduce false reassurance, missing-data bias, configuration drift, benchmark leakage, and reproducibility risk. They do not provide evidence that the EFGM equations themselves are correct.
