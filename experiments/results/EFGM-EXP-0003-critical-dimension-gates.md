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

## Novel falsification cases

Cases were intentionally constructed outside the existing correlated-mutation pattern. Each case makes one semantically critical metric collapse while neighboring metrics remain strong.

### v2

- evidence validity collapse;
- rule-support collapse;
- factual-consistency collapse;
- traceability collapse.

Result: aggregate grounding remains high enough for reassuring classification in all deterministic central cases. With evidence validity at zero and otherwise strong factors, `G=0.7125`, `DQ≈0.8228`, classification=`Coherent and grounded`.

### v0.3 candidate

- trust-boundary adherence collapse;
- analogous single control/boundary collapse reasoning.

Result: one zero boundary metric yields boundary-family mean `0.75`, governance integrity `≈0.9532`, uncontrolled-agency risk `≈0.0239`, and classification=`Governed autonomous operation` for task flow `0.85` and agency `0.60`.

## Sensitivity

Analytic Monte Carlo perturbation tests used fixed seeds and did not touch holdout data.

- v2 evidence-validity collapse: reassuring classification in 78.84% of 10,000 trials;
- v2 rule-support collapse: 78.86%;
- v2 factual-consistency collapse: 95.45%;
- v0.3 trust-boundary collapse: reassuring governed classification in 100% of 10,000 trials.

## Ablation / candidate comparison

Aggregate-only classification fails because averaging is compensatory: strong neighboring metrics can offset a catastrophic critical metric.

Candidate ablation: retain all continuous scores unchanged and add only a component-level floor gate. On the constructed invariant-violation cases, the gate corrects the false reassurance by construction. This is not enough to claim general improvement because the cases were internally authored specifically to test that invariant.

No threshold has been promoted. `0.40` is recorded only as an initial candidate aligned with the existing aggregate critical-grounding threshold and must be swept on non-holdout development/validation data.

## Counterexample classification

**Material and reproducible.** The failure is structural and survives substantial perturbation. It is also distinct from the prior benchmarks because those benchmarks primarily mutate multiple correlated dimensions and therefore do not exercise sparse catastrophic failures.

## Rejected changes

- Replacing v2 DQ with a minimum-based formula: rejected as premature and would destroy baseline comparability.
- Replacing v0.3 governance geometric mean with a hard minimum: rejected as premature because it could overreact to noisy submetrics.
- Tuning the gate threshold on any sealed holdout: prohibited.
- Changing benchmark labels after observing model outputs: prohibited.

## Recommended next experiment

Build a dedicated sparse-failure development/validation suite with both invariant violations and benign low-score controls. Compare:

1. frozen aggregate-only classifier;
2. aggregate classifier + critical floor gate;
3. percentile/soft-min alternatives;
4. simple independent invariant checklist.

The gate should be promoted only if it reduces false reassurance without unacceptable false alarms and survives independently authored cases.
