# EFGM-EXP-0003 — Critical-dimension gate falsification cycle

## Hypothesis

Aggregate means can hide sparse catastrophic failures. A preregistered component-level floor gate may reduce false reassurance without changing the underlying frozen v2 score or experimental v0.3 continuous scores.

## Inputs reviewed

- frozen EFGM v0.2 baseline `b717f611a0d09bd8e52bc1b0be5ee178eecacf25`;
- Benchmark v0.1 / EFGM-EXP-0001 from PR #6;
- experimental agent-governance PR #7 at `7b452f40b545cd83ae84b42b6ee1c0fc99c68d54`;
- Benchmark v0.2 agent-governance design and CI run #48;
- canonical validation rules requiring falsification, simpler baselines, explicit unknowns, and sealed holdout custody.

## Prior-result context

Benchmark v0.1 showed v2 and a simpler weighted linear model both ranked 72/72 synthetic pairs correctly, while v2 had larger separation and perturbation robustness. This did not establish nonlinear necessity.

Benchmark v0.2 agent-governance showed all governance-aware candidates and the independent checklist ranked 66/66 governance-mutation pairs correctly, while v2 task flow tied 66/66 because task-flow observations were deliberately held constant. Under ±0.10 perturbation, the independent checklist was substantially more robust than the proposed governance formulas, so no v0.3 aggregation was established as superior.

## Novel falsification cases — cycle 1

Cases were intentionally constructed outside the existing correlated-mutation pattern. Each case makes one semantically critical metric collapse while neighboring metrics remain strong.

### v2 grounding

- evidence validity collapse;
- rule-support collapse;
- factual-consistency collapse;
- traceability collapse.

Result: aggregate grounding remains high enough for reassuring classification in all deterministic central cases. With evidence validity at zero and otherwise strong factors, `G=0.7125`, `DQ≈0.8228`, classification=`Coherent and grounded`.

### v0.3 candidate governance

- trust-boundary adherence collapse;
- analogous single control/boundary collapse reasoning.

Result: one zero boundary metric yields boundary-family mean `0.75`, governance integrity `≈0.9532`, uncontrolled-agency risk `≈0.0239`, and classification=`Governed autonomous operation` for task flow `0.85` and agency `0.60`.

## Sensitivity — cycle 1

Analytic Monte Carlo perturbation tests used fixed seeds and did not touch holdout data.

- v2 evidence-validity collapse: reassuring classification in 78.84% of 10,000 trials;
- v2 rule-support collapse: 78.86%;
- v2 factual-consistency collapse: 95.45%;
- v0.3 trust-boundary collapse: reassuring governed classification in 100% of 10,000 trials.

## Novel falsification cases — cycle 2

A follow-up cycle tested whether the failure was limited to grounding/governance or reflected a more general aggregation property.

The preregistered invariant was: an explicitly applicable and measured `task_completion_consistency=0.00` or `verification_success_rate=0.00` is not eligible for the strongest reassuring flow classification.

With `T=C=G=U=0.95`, low entropy, and all other flow-quality observations at `0.95`:

- `task_completion_consistency=0.00` -> `Fq=0.6650`, v2 `DQ≈0.8345`, classification=`Coherent and grounded`;
- `reasoning_continuity=0.00` -> `Fq=0.7125`, v2 `DQ≈0.8461`, classification=`Coherent and grounded`;
- `semantic_coherence=0.00` -> `Fq=0.7125`, v2 `DQ≈0.8461`, classification=`Coherent and grounded`;
- `verification_success_rate=0.00` -> `Fq=0.7600`, v2 `DQ≈0.8571`, classification=`Coherent and grounded`.

The same family aggregation exists in v1. With `T=E=0.95` and `e≈0.02`, all four collapsed-submetric cases still exceed the v1 `Coherent` threshold (`F≈0.8270` to `0.8646`).

This establishes a **cross-family, cross-version** form of critical-dimension dilution rather than a grounding-specific defect.

## Sensitivity — cycle 2

10,000 deterministic perturbation trials per collapsed flow metric varied non-collapsed positive factors in `[0.90,0.98]`, entropy observations in `[0.00,0.05]`, and the collapsed flow observation in `[0.00,0.05]`.

Fraction of v2 trials still classified `Coherent and grounded`:

- task completion consistency collapse: **91.59%**;
- reasoning continuity collapse: **99.05%**;
- semantic coherence collapse: **99.09%**;
- verification success collapse: **99.97%**.

## Novel falsification cases — cycle 3

Cycle 3 tested the opposite side of the v2 equation: whether a *maximal degradation* observation can also be diluted inside penalty-family averaging.

Construct a strong state with `T=C=Fq=G=U=0.99`, set all non-target penalty observations to `0.00`, and set exactly one output-, behavioral-, or operational-entropy observation to `1.00`.

Result: **10 of 15** single-maximal-degradation cases still receive `Coherent and grounded`.

Examples:

- `output_entropy.reasoning_instability=1.00` -> `Eo=0.15`, `DQ≈0.8609`, `Coherent and grounded`;
- `output_entropy.context_decay=1.00` -> `Eo=0.15`, `DQ≈0.8609`, `Coherent and grounded`;
- `behavioral_entropy.overconfidence_feedback=1.00` -> `Be=0.15`, `DQ≈0.8609`, `Coherent and grounded`;
- `operational_entropy.latency_pressure=1.00` -> `Oe=0.15`, `DQ≈0.8609`, `Coherent and grounded`;
- `operational_entropy.workflow_interruption=1.00` -> `Oe=0.15`, `DQ≈0.8609`, `Coherent and grounded`.

Weight-0.20 cases (`goal_drift`, `outcome_bias`, `sunk_cost_pressure`, `false_pattern_detection`, `retry_instability`) also remain `Coherent and grounded` at the exact central point (`DQ=0.8250`). Weight-0.25 cases fall to `Stable with watch items` (`DQ=0.7920`).

The existing driver diagnostics can therefore identify a target metric as a severe entropy driver while the top-level classifier simultaneously emits its strongest reassuring label.

## Sensitivity — cycle 3

For the five low-weight (`0.15`) maximal-degradation cases above, 10,000 bounded trials per case varied:

- positive factors near `0.99`;
- the target degraded observation in `[0.90,1.00]`;
- all non-target penalty observations in `[0.00,0.05]`.

The strongest `Coherent and grounded` label persisted in **79.03%–79.68%** of trials. This shows the defect is not limited to an exact `1.00/0.00` corner case.

Weight-0.20 cases are less perturbation-robust because their central DQ lies close to the `0.80` classification threshold; they nevertheless demonstrate the same compensatory structure deterministically.

## Ablation / candidate comparison

Aggregate-only classification fails because averaging is compensatory: strong neighboring metrics can offset a catastrophic critical metric, and low-weight penalty observations can be diluted before they reach `DQ`.

Candidate ablation: retain all continuous scores unchanged and add only a preregistered prerequisite/critical-floor diagnostic. On the constructed invariant-violation cases, the gate corrects false reassurance by construction. This is not enough to claim general improvement because the cases were internally authored specifically to test those invariants.

Cycle 3 adds a distinct candidate worth testing: a **classification-only extreme-degradation veto** over applicable output-, behavioral-, and operational-entropy base observations. A direct hard-max replacement formula detects the sparse failures but is rejected as premature because it can over-penalize benign moderate single-dimension degradation.

The cycle-2 result rejects a **narrow grounding-only gate** as incomplete. Any candidate gate must be specified semantically across applicable families before evaluation, rather than declaring metrics critical after observing failures.

No threshold has been promoted. `0.40` remains only an initial candidate for positive prerequisites; any extreme-degradation threshold on penalty metrics must be independently justified and swept on non-holdout development/validation data with benign controls.

Candidate alternatives retained for testing:

1. aggregate-only frozen classifier;
2. aggregate classifier + preregistered positive prerequisite floor;
3. aggregate classifier + preregistered extreme-degradation veto;
4. soft-min / low-percentile diagnostic layer;
5. independent invariant checklist.

## Counterexample classification

**Material and reproducible.** The failure is structural and survives substantial perturbation. It is distinct from the prior benchmarks because those benchmarks primarily mutate multiple correlated dimensions and therefore do not exercise sparse catastrophic failures.

Cycle 3 further shows that the same structural weakness exists on both sides of v2 aggregation: positive prerequisites can be averaged upward and negative degradation can be averaged downward.

## Rejected changes

- Replacing v2 DQ with a minimum-based formula: rejected as premature and would destroy baseline comparability.
- Replacing penalty-family means with raw hard maxima: rejected as premature because it can overreact to isolated moderate/noisy measurements.
- Replacing v0.3 governance geometric mean with a hard minimum: rejected as premature because it could overreact to noisy submetrics.
- Applying only a grounding-family gate: rejected as incomplete after the cross-version flow-quality counterexample.
- Tuning any gate threshold on sealed holdout: prohibited.
- Changing benchmark labels after observing model outputs: prohibited.

## Recommended next experiment

Build a dedicated sparse-failure development/validation suite with both invariant violations and benign low-score/high-penalty controls. The prerequisite and veto sets must be preregistered by semantic role before outcomes are inspected. Include at minimum:

- flow-quality prerequisites;
- grounding prerequisites;
- output-entropy sparse extremes;
- behavioral-entropy sparse extremes;
- execution prerequisites and sparse operational failures for tasks that require successful tool/action completion;
- agent authorization, boundary, observability, and control prerequisites.

Compare aggregate-only scoring, hard prerequisite floors, extreme-degradation vetoes, continuous soft-min diagnostics, and a simple independent invariant checklist. Promotion requires reduced false reassurance without unacceptable false alarms and survival on independently authored cases.

## Research log

- **Hypothesis:** sparse failures are diluted by family aggregation.
- **Test 1:** grounding and agent boundary single-metric collapse.
- **Result 1:** reproducible false reassurance; persisted under perturbation.
- **Test 2:** flow-quality single-metric collapse in frozen v1/v2.
- **Result 2:** same failure pattern; strongest classification persisted in 91.59%–99.97% of perturbed v2 trials.
- **Test 3:** single maximal output/behavioral/operational degradation with strong neighbors.
- **Result 3:** 10/15 central cases still receive the strongest v2 label; five low-weight maximal failures remain strongest-label cases in ~79% of noisy trials.
- **Counterexamples retained:** `EFGM-CE-0001`, `EFGM-CE-0002`, `EFGM-CE-0003`.
- **Rejected:** hard-min formula replacement; raw hard-max penalty replacement; grounding-only patch; holdout tuning.
- **Current proposal:** evaluate a classification-only positive prerequisite layer plus an extreme-degradation veto or soft-min diagnostic, with frozen continuous scores unchanged.

## Conclusion

Current evidence strongly justifies testing a broader non-compensatory diagnostic/classification layer. It does **not** justify silently changing the frozen v0.2 baseline or promoting the experimental v0.3 candidate.
