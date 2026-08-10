# EFGM-CE-0003 — Extreme penalty-submetric dilution

## Status

Reproducible counterexample against the frozen EFGM v0.2 classifier. No holdout data used. No canonical equation, weight, threshold, or gold label changed.

## Hypothesis

A maximally degraded applicable submetric in output entropy, behavioral entropy, or operational entropy should not be able to coexist with the strongest governance label merely because neighboring submetrics are near zero and positive factors are strong.

This tests the penalty side of EFGM v2, extending CE-0001/CE-0002 beyond positive-family averaging.

## Construction

Use a high-quality synthetic decision state with `T=C=Fq=G=U=0.99`, all non-target penalty metrics `0.00`, and set exactly one target penalty submetric to `1.00`.

Frozen v0.2 weights imply the target family composite equals the target metric's weight. The classifier then evaluates the ordinary frozen `DQ` and grounding/output-entropy gates.

## Central results

Of 15 single-maximal-degradation cases, 10 still receive **Coherent and grounded**.

| Family | Target metric = 1.00 | Weight | DQ | Frozen classification |
|---|---|---:|---:|---|
| output entropy | output_contradiction | 0.25 | 0.7920 | Stable with watch items |
| output entropy | uncertainty_mismatch | 0.25 | 0.7920 | Stable with watch items |
| output entropy | goal_drift | 0.20 | 0.8250 | Coherent and grounded |
| output entropy | reasoning_instability | 0.15 | 0.8609 | Coherent and grounded |
| output entropy | context_decay | 0.15 | 0.8609 | Coherent and grounded |
| behavioral entropy | chasing_behavior | 0.25 | 0.7920 | Stable with watch items |
| behavioral entropy | outcome_bias | 0.20 | 0.8250 | Coherent and grounded |
| behavioral entropy | sunk_cost_pressure | 0.20 | 0.8250 | Coherent and grounded |
| behavioral entropy | false_pattern_detection | 0.20 | 0.8250 | Coherent and grounded |
| behavioral entropy | overconfidence_feedback | 0.15 | 0.8609 | Coherent and grounded |
| operational entropy | timeout_rate | 0.25 | 0.7920 | Stable with watch items |
| operational entropy | retry_instability | 0.20 | 0.8250 | Coherent and grounded |
| operational entropy | tool_failure_rate | 0.25 | 0.7920 | Stable with watch items |
| operational entropy | latency_pressure | 0.15 | 0.8609 | Coherent and grounded |
| operational entropy | workflow_interruption | 0.15 | 0.8609 | Coherent and grounded |

The existing driver logic can simultaneously identify these raw metrics as high-score degradation drivers while the top-level classifier emits its strongest label. This is a classification/diagnostic inconsistency, not merely a score-separation issue.

## Perturbation check

For the five low-weight (`0.15`) failures that most strongly expose the defect — `reasoning_instability`, `context_decay`, `overconfidence_feedback`, `latency_pressure`, and `workflow_interruption` — run 10,000 bounded trials per case:

- positive factors centered near `0.99`;
- target failure uniformly in `[0.90, 1.00]`;
- non-target penalty metrics uniformly in `[0.00, 0.05]`.

The strongest **Coherent and grounded** label persisted in approximately **79%** of trials for each of those five cases (79.03%–79.68% in this run). Thus the result is not dependent on an exact `1.00/0.00` corner point.

Weight-0.20 cases are less perturbation-robust because they sit closer to the `DQ=0.80` threshold, but their exact central cases still demonstrate the same compensatory mechanism.

## Baseline/candidate interpretation

- **v1:** cannot represent behavioral or operational entropy and therefore cannot diagnose those failures directly; this is a representational limitation rather than evidence for v1.
- **frozen v2:** weighted family averaging allows severe raw degradation to be diluted before top-level classification.
- **weighted linear comparator:** uses the same family composites and therefore inherits the dilution mechanism.
- **hard-max penalty formula:** would detect the cases but is rejected as a direct replacement because it can over-penalize benign moderate single-dimension degradation.
- **classification-only extreme-degradation veto:** candidate worth testing. Example preregistered form: if any applicable `Eo`, `Be`, or `Oe` base observation is at or above an independently justified extreme threshold, the result cannot receive the strongest reassuring classification. Continuous `DQ` remains unchanged.

The candidate threshold must not be selected from these cases alone. It requires development/validation sweeps with benign controls and independently authored cases before promotion.

## Generalization diagnosis

Existing controlled benchmarks mainly move correlated groups of metrics. That construction rewards aggregate methods and under-samples sparse extreme failures. CE-0003 shows a different adversarial geometry: one severe degradation signal surrounded by excellent neighbors.

This is evidence of benchmark coverage weakness, not evidence that any proposed gate is already generally valid.

## Research conclusion

CE-0001/CE-0002 identified compensatory dilution in positive/critical families. CE-0003 shows the same structural weakness on the penalty side of v2. The current strongest classification can therefore conflict with a raw metric that explicitly states maximal degradation.

A future experiment should preregister and compare aggregate-only classification, semantic prerequisite floors, a generic extreme-degradation veto, soft-min/percentile diagnostics, and independent invariant checklists. No canonical change is justified from this counterexample alone.
