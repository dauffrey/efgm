# EFGM v2 Validation Test Plan

## Purpose

This plan governs validation of the **EFGM v2 decision-integrity model**. The goal is not to prove EFGM correct. The goal is to determine whether its constructs are measurable, reproducible, diagnostically useful, and predictive of independently defined decision quality better than simpler alternatives.

The canonical model is `docs/model-specification-v2.md` and the scoring anchors are `docs/scoring-rubric-v2.md`.

## Core principles

1. **Falsification first** — actively search for cases where EFGM ranks decisions incorrectly or produces misleading explanations.
2. **Evidence first** — applied scores require rationale and evidence references.
3. **No outcome leakage** — decision-time metrics must use only information available at decision time.
4. **Unknown is explicit** — missing evidence must not be silently converted into certainty.
5. **Holdouts stay sealed** — tuning processes must not inspect sealed holdout cases.
6. **Gold labels are independent** — EFGM disagreement is not a reason to rewrite the answer key.
7. **Simpler baselines compete** — EFGM must add value beyond checklists or smaller formulas.
8. **Version everything** — model configuration, code SHA, dataset version, scorers, and experiment manifest.
9. **Human promotion gate** — autonomous research may propose candidates but may not promote them to the canonical baseline without review.

## Validation questions

The program should answer:

- Can independent reviewers score the same evidence with acceptable agreement?
- Are `Fq`, `G`, `U`, `Ei`, `Eo`, `Be`, `Oe`, and `CRC` empirically distinguishable?
- Does higher `DQ` predict independently preferred decisions?
- Does `CRC` identify successful entropy recovery beyond what `Eo` alone explains?
- Does the grounding gate reduce false reassurance from coherent hallucinations?
- Does v2 outperform v1?
- Does v2 outperform simpler baselines?
- Which variables are redundant, unstable, or domain-dependent?
- Do improvements survive data not used for tuning?

## Dataset partitions

Use three explicit partitions under `benchmarks/`:

```text
benchmarks/development/   # visible to the research/tuning loop
benchmarks/validation/    # used for periodic candidate comparison
benchmarks/holdout/       # sealed from tuning; opened only for frozen candidates
```

A case moved into holdout must not later be used for tuning that candidate generation.

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

## Mathematical invariant tests

The executable baseline should preserve these baseline expectations while all else is held constant:

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

Every serious benchmark should compare at least:

1. simple pass/fail checklist;
2. small grounding + calibration baseline;
3. weighted linear baseline;
4. EFGM v1 compatibility model where inputs permit;
5. frozen EFGM v2 baseline;
6. any proposed v2 candidate.

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
- incremental value versus simpler baselines.

Confidence intervals should accompany aggregate results when sample size permits.

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
5. simpler baselines do not provide equivalent benefit at materially lower complexity;
6. a sealed holdout evaluation supports generalization;
7. material counterexamples and regressions are disclosed;
8. human review approves promotion.

A failed candidate remains recorded under `experiments/rejected-candidates/`.

## Scientific claim discipline

Passing this plan does not make EFGM a scientifically proven law. A defensible claim is narrower:

> Under specified tested conditions, a particular version of EFGM demonstrated reproducible measurement and/or predictive value relative to stated baselines.

Stronger claims require independent replication across datasets, scorers, domains, and research teams.
