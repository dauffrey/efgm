# EFGM v2 Scoring Rubric

## Purpose

This rubric defines provisional scoring anchors for EFGM v2 so different reviewers can apply the model more consistently. These anchors are research hypotheses and should be refined from inter-rater and predictive-validity evidence.

Every applied score should be supported by a `MetricObservation`. A reviewer should prefer `unknown`/low-confidence evidence over invented precision.

## Common normalized anchors

Unless a metric has a stronger domain-specific formula, use these anchors:

| Value | Positive metric | Entropy metric |
|---:|---|---|
| `0.00` | absent / unusable | no observable entropy |
| `0.25` | weak | low entropy |
| `0.50` | partial / mixed | moderate entropy |
| `0.75` | strong | high entropy |
| `1.00` | fully demonstrated | severe entropy |

Intermediate values are allowed only when the rationale explains why.

## T — Observation maturity / sequence continuity

`T` is **not literal elapsed clock time**. It measures how mature and continuous the available observation sequence is for the assessed decision.

| Score | Anchor |
|---:|---|
| `0.00` | isolated unsupported snapshot |
| `0.25` | minimal observation; unstable or discontinuous sequence |
| `0.50` | multiple observations but meaningful gaps remain |
| `0.75` | repeated observations with strong continuity |
| `1.00` | mature, stable, well-observed sequence with no material continuity gap |

Do not increase `T` merely because time passed. Stale or fragmented observation should not receive a high score.

## C — Capability suitability

`C` measures whether the tools, rules, evidence access, expertise, and execution mechanisms available are suitable for the specific objective.

| Score | Anchor |
|---:|---|
| `0.00` | no usable capability for the objective |
| `0.25` | major capability mismatch or missing critical tools |
| `0.50` | partial capability; important gaps constrain the decision |
| `0.75` | strong fit with manageable limitations |
| `1.00` | required capability is fully available and demonstrated |

High raw compute or staff count does not automatically mean high `C`.

## Flow quality (`Fq`) metrics

### Task completion consistency

Score the proportion and correctness of required steps, not mere activity volume.

### Reasoning continuity

Score whether later conclusions preserve and correctly use earlier verified facts, constraints, and assumptions.

### Semantic coherence

Score whether terminology, categories, claims, and conclusions retain consistent meaning.

### Verification success rate

Where a denominator is available, prefer:

```text
verified verifiable claims / total verifiable claims
```

Do not penalize claims that are genuinely not reasonably verifiable.

## Input entropy (`Ei`) metrics

### Input contradiction

Score conflict among incoming claims, requirements, rules, or evidence before the assessed reasoning/output acts on them.

### Input ambiguity

Score unresolved multiplicity of plausible interpretations relevant to the decision.

### Input goal conflict

Score tension among objectives that cannot all be optimized simultaneously without trade-offs.

### Missing context

Score relevant information known to be unavailable or omitted at decision time.

### Hidden-information load (`H`)

Score relevant state that cannot be observed or is materially inaccessible, rather than information simply not yet retrieved.

## Output entropy (`Eo`) metrics

### Output contradiction

Score incompatible claims or decisions introduced or retained by the output.

### Uncertainty mismatch

Score mismatch between stated/implied confidence and evidentiary support.

### Goal drift

Score departure from the authorized/intended objective.

### Reasoning instability

Score unexplained reversals, non-convergence, or internally unstable decision progression.

### Context decay

Score loss, weakening, or contradiction of previously valid context.

## Grounding (`G`) metrics

### Rule support

Does the decision align with applicable rules, constraints, specifications, or authorized procedures?

### Evidence validity

Are the supporting evidence sources relevant, authentic enough for the use, and methodologically appropriate?

### Traceability

Can material claims and decisions be linked back to identifiable evidence or requirements?

### Factual consistency

Do claims match verified external facts/ground truth where such facts are available?

### Domain calibration

Does the reasoning use concepts, thresholds, and assumptions appropriately for the domain rather than importing unsuitable generic logic?

## U — Uncertainty calibration

`U` is high when confidence is proportional to evidence and low when the system is overconfident, unjustifiably underconfident, or inconsistent without new evidence.

Suggested anchors:

| Score | Anchor |
|---:|---|
| `0.00` | confidence behavior is grossly inconsistent with evidence |
| `0.25` | substantial mismatch |
| `0.50` | mixed calibration |
| `0.75` | generally proportionate confidence |
| `1.00` | consistently well-calibrated confidence under the assessed conditions |

Where repeated probabilistic predictions exist, empirical calibration metrics should replace subjective judgment.

## Behavioral entropy (`Be`) metrics

Score only behavioral distortion relevant to the decision, not generic undesirable behavior.

- chasing behavior: changing decisions primarily in reaction to recent outcomes rather than evidence;
- outcome bias: judging a decision mainly by the result rather than decision-time information;
- sunk-cost pressure: preserving a course because of prior investment despite contrary evidence;
- false pattern detection: asserting structure unsupported by the evidence;
- overconfidence feedback: confidence escalating because of prior confidence/success rather than new evidence.

## Operational entropy (`Oe`) metrics

Use observed execution evidence where possible:

- timeout rate;
- retry instability;
- tool failure rate;
- latency pressure when it materially changes decisions/actions;
- workflow interruption.

## Observation status

| Status | Meaning |
|---|---|
| `observed` | directly supported by evidence |
| `inferred` | estimated from indirect evidence or reviewer judgment |
| `unknown` | evidence is insufficient to characterize the metric reliably |
| `not_applicable` | metric does not meaningfully apply to the scenario |

The current scorer still requires a numeric value. For `unknown` observations, reviewers must document any placeholder/estimate and assign low confidence. A future model may formally marginalize or exclude unknown observations; that is an open research question.

## Evidence quality rules

1. Cite evidence that existed at the decision time when scoring decision quality.
2. Do not leak outcome information into decision-time metrics.
3. Separate direct observation from inference.
4. Do not improve a score because the eventual outcome happened to be good.
5. Record scorer identity/type so inter-rater behavior can be analyzed.
6. If a score cannot be defended in one or two evidence-based sentences, treat it as insufficiently supported.

## Classification caution

Classification thresholds are provisional parameters in the versioned configuration, not intrinsic meanings of the metric scale. Research should test whether the bands improve decisions versus reporting continuous scores alone.
