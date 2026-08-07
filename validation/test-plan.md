# EFGM v2 Validation Test Plan

## Purpose

This plan governs validation of the **EFGM v2 decision-integrity model**. The goal is not to prove EFGM correct. The goal is to determine whether its constructs are measurable, reproducible, diagnostically useful, and predictive of independently defined decision quality better than simpler alternatives.

The canonical model is `docs/model-specification-v2.md` and the scoring anchors are `docs/scoring-rubric-v2.md`.

## Core principles

1. **Falsification first** — actively search for cases where EFGM ranks decisions incorrectly or produces misleading explanations.
2. **Evidence first** — applied scores require rationale and evidence references.
3. **No outcome leakage** — decision-time metrics must use only information available at decision time.
4. **Unknown is explicit** — missing evidence blocks a completed score; it must never silently become zero or another favorable value.
5. **N/A is explicit** — not-applicable metrics are excluded and remaining weights renormalized; omission is not N/A.
6. **Holdouts stay sealed** — real holdout cases/labels remain outside the tuning-visible repository until a candidate is frozen.
7. **Gold labels are independent** — EFGM disagreement is not a reason to rewrite the answer key.
8. **Simpler baselines compete** — EFGM must add value beyond checklists or smaller formulas.
9. **Version and hash everything** — configuration ID/hash, input hash, code SHA, dataset version, scorers, and experiment manifest.
10. **Human promotion gate** — autonomous research may propose candidates but may not promote them to the canonical baseline without review.

## Validation questions

The program should answer:

- Can independent reviewers score the same evidence with acceptable agreement?
- Are `Fq`, `G`, `U`, `Ei`, `Eo`, `Be`, `Oe`, and `CRC` empirically distinguishable?
- Does higher `DQ` predict independently preferred decisions?
- Does `CRC` identify successful entropy recovery beyond what `Eo` alone explains?
- Does the grounding gate reduce false reassurance from coherent hallucinations?
- Does v2 outperform v1?
- Does v2 outperform simpler EFGM-derived ablations?
- Does v2 outperform an **independent** checklist established without EFGM composite scores?
- Which variables are redundant, unstable, or domain-dependent?
- Do improvements survive data not used for tuning?

## Dataset partitions

Use three logical partitions:

```text
benchmarks/development/   # visible to the research/tuning loop
benchmarks/validation/    # used for periodic candidate comparison
benchmarks/holdout/       # metadata only; actual cases/labels externally sealed
```

The repository's holdout directory must not contain the real case text or preferred labels when an autonomous researcher can read Git. Use external custody or equivalent access control and commit only non-revealing manifests/hashes.

A case exposed from holdout must not later be treated as unseen evidence for the same candidate-generation cycle.

## Initial scenario families

At minimum include:

- sycophancy / preference pressure;
- prompt injection / untrusted instructions;
- factual grounding / coherent hallucination;
- uncertainty calibration;
- contradictory evidence;
- missing context and hidden information;
- goal conflict and ambiguous authorization;
- context decay;
- agent/tool failure;
- behavioral feedback pressure;
- lucky bad decisions and unlucky good decisions;
- software/release/incident scenarios using sanitized evidence.

## Controlled mutation tests

Create paired cases in which one property changes while the rest remains as constant as practical.

Examples:

- remove evidence while preserving fluent prose → `G` should fall;
- inflate certainty without adding evidence → `U` should fall / uncertainty mismatch should rise;
- add a contradiction → `Eo` should rise;
- add user-pressure agreement without evidence change → behavioral entropy should rise;
- remove an earlier valid constraint → context decay should rise;
- add tool failures while preserving intended reasoning → `Oe` should rise.

Selective response of the intended dimension is evidence for construct validity. Broad indiscriminate movement is evidence of poor construct separation.

## Missing-data and provenance tests

The executable baseline must also demonstrate:

```text
omitted metric         => unknown, not 0
unknown metric         => completed scoring blocked
explicit 0.00          => accepted as a measured value
not_applicable metric  => excluded; remaining weights renormalized
all N/A Be or Oe       => zero penalty only when explicitly declared N/A
legacy numeric input   => inferred / provenance incomplete
strict research mode   => incomplete provenance rejected
```

Research-grade runs must use `require_provenance=True` or an equivalent validation gate.

## Mathematical invariant tests

The executable baseline should preserve these expectations while all else is held constant:

```text
G increases  => DQ must not decrease
Fq increases => DQ must not decrease
U increases  => DQ must not decrease
Eo increases => DQ must not increase
Be increases => DQ must not increase
Oe increases => DQ must not increase
H increases  => OutcomeConfidence must not increase
OQ changes   => DQ must remain unchanged
```

`CRC` expectations:

```text
Eo < Ei  => CRC positive
Eo = Ei  => CRC approximately zero
Eo > Ei  => CRC negative
```

The current CRC ratio may be below `-1`; bounded alternatives are candidates for comparison, not implicit replacements.

## Baselines

Every serious benchmark should distinguish **EFGM-derived ablations** from genuinely independent comparators.

EFGM-derived ablations:

1. EFGM-threshold checklist over existing composites;
2. grounding + calibration (`G + U`) baseline;
3. weighted linear aggregation of EFGM composites;
4. EFGM v1 compatibility model where inputs permit;
5. frozen EFGM v2 baseline;
6. any proposed v2 candidate.

Independent comparators:

1. a small checklist whose criteria are established before EFGM scoring and do not consume EFGM composite values;
2. external human/expert preference labels;
3. external statistical or task-specific metrics where available.

A candidate should not be accepted merely because it is more elaborate.

## Primary evaluation metrics

- pairwise ranking accuracy against independent labels;
- mean/median `DQ` separation between preferred and non-preferred decisions;
- calibration error where probabilistic confidence is available;
- inter-rater agreement for metric observations;
- driver agreement for dominant failure mechanisms;
- false reassurance rate, especially for weak grounding;
- false alarm rate;
- sensitivity to score perturbation;
- performance by scenario family/domain;
- incremental value versus simpler and independent baselines.

Confidence intervals should accompany aggregate results when sample size permits.

## Configuration/reproducibility tests

Candidate configurations must be rejected if they contain:

- missing or unexpected metric names;
- negative or non-finite weights;
- weight sections that do not normalize to 1.0;
- invalid/unknown schema version;
- `epsilon <= 0`;
- thresholds outside `[0,1]`;
- logically disordered classification thresholds.

Every result must record `config_id`, configuration SHA-256, and input SHA-256. Every experiment manifest must also record the code commit SHA.

## Ablation tests

Test the contribution of each major construct by removing or neutralizing it:

- no `T`;
- no `C`;
- no `G`;
- no `U`;
- no `Be`;
- no `Oe`;
- `Eo` only versus `Eo + Be + Oe`;
- DQ with and without the grounding gate;
- CRC versus output entropy alone.

A construct that does not add stable explanatory or predictive value should be simplified, merged, or removed.

## Inter-rater validation

For a meaningful subset, use at least two independent scorers who do not know the preferred answer label while scoring EFGM observations.

Record:

- scorer ID/type;
- evidence reviewed;
- each observation value/status/confidence;
- classification;
- recommendation.

Disagreement is validation data. Do not average it away before examining the cause.

## Candidate promotion rule

A candidate configuration/model may be proposed when development evidence improves. It may be promoted only if:

1. the hypothesis and change were recorded before final evaluation;
2. development results improve or reveal a clear diagnostic benefit;
3. validation results do not show material regression;
4. ablation supports the claimed mechanism;
5. simpler or independent baselines do not provide equivalent benefit at materially lower complexity;
6. a genuinely sealed holdout evaluation supports generalization;
7. material counterexamples and regressions are disclosed;
8. result/input/config/code identities are reproducible;
9. human review approves promotion.

A failed candidate remains recorded under `experiments/rejected-candidates/`.

## Packaging/CI requirement

CI must test both source/editable development behavior and the built distributable wheel. The wheel test must run outside the repository working directory so missing package data (such as the baseline JSON config) cannot be masked by the source tree.

## Scientific claim discipline

Passing this plan does not make EFGM a scientifically proven law. A defensible claim is narrower:

> Under specified tested conditions, a particular version of EFGM demonstrated reproducible measurement and/or predictive value relative to stated baselines.

Stronger claims require independent replication across datasets, scorers, domains, and research teams.
