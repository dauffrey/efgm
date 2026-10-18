# Native mechanisms first: prospective causal and predictive experiment

**Status:** proposed protocol, **not preregistered, frozen, run, replicated or validated**. No experiment number assigned pending registry review. This extends the [interpretability and governability research program](INTERPRETABILITY_AND_GOVERNABILITY_PROGRAM.md), not the historical EFGM findings.

## Source-derived motivation

Nick Cammarata, *Neural Networks Are Already Clean*, https://already-clean.goodfire.com/ (accessed 2026-10-17), argues as a working hypothesis that apparent polysemanticity in early examples often reflects recursive generalization, model architectural artifacts or flawed measurement/visualization rather than arbitrary superposition. The essay advocates starting with a network's native neurons and circuits, testing explanations by intervention, and inspecting both directions of neuron response and upstream/downstream relations. Its reported interpretability estimates are preliminary, rubric-dependent, and **not** evidence that all behavior is causally understood.

**Our inference, not a result of the essay:** EFGM entropy, coherent-flow, Decision Quality or governance measurements may correlate with separately measured mechanistic organization or may add no predictive information. The null is entirely plausible given existing EFGM negative incremental-value findings (EXP-0009 and EXP-0010). The test must permit a negative outcome.

## Core scientific question

For a fixed, permitted, inspectable model and explicitly specified behavioral task, do **pre-action** EFGM measurements add independently reproducible prediction of *held-out causal intervention outcomes* beyond simpler native-circuit and behavioral baselines?

This is **not** testing whether EFGM can read hidden weights of a remote API-only model. The model must permit genuine native activation/weight access and reproducible perturbations. Unknown internals remain unknown.

## Hypotheses and falsifiers

- **H-N (native explanation):** a frozen, human- and/or model-proposed native-neuron/circuit hypothesis predicts intervention direction and magnitude on independent held-out inputs better than a preregistered placebo/permuted-feature control. A vague plausible verbal story is insufficient.
- **H-E (incremental EFGM value):** a prespecified EFGM-derived signal predicts held-out causal outcome or detection lead time *better than* both a no-EFGM native circuit baseline and a cheap behavior-only baseline, with a prespecified minimum effect and confidence interval. Zero gain or negative gain rejects this hypothesis for the scope.
- **H-R (robustness):** native explanations and incremental signals retain specified performance across task families, perturbation strengths, model checkpoints and carefully documented distribution shifts. Performance deterioration must be reported, not pooled away.

## Proposed study units and observational limits

Use a small public, permitted, open-weight model capable of activation hooks; begin with a small vision or language model that is feasible to run with bounded compute. Choose **one** architecture, checkpoint, dataset provenance, task, target layer, activation nonlinearity and run configuration before making any observations used for evaluation.

Observation unit: `(model checkpoint, prompt/input, target native unit or circuit, intervention, output/behavior)`. Preserve raw pre-intervention activations, negative/positive response separately when meaningful, upstream weights/inputs, downstream reader connections, intervention dose, predictions **made before** intervention, actual outcome, and reasons for missingness.

**Avoid assuming scalar "neuron meaning".** Consider linked concepts, positive/negative polarity, upstream/downstream context, and activation gating; distinguish semantic grouping from causal contribution. Do not confuse feature visualization or SAE reconstruction quality with causal predictive fidelity.

## Independent evaluation and baselines

1. **Exploration only:** document activations, native neuron hypotheses, pathway tracing, testable mechanism claims and initial counterexamples on a **development** partition. Record possible measurement artifacts.
2. **Freeze before evaluation:** register exact code revision, model digest, prompts/input-generator version, target neurons/circuits, proposed interventions, predicted effects, metrics, EFGM operationalization, statistical intervals, the baseline suite and exclusion rules. A holdout custodian confirms isolation.
3. **Intervene causally:** predeclare ablation, activation steering/patching or other valid model-specific interventions; include sham interventions, random comparable neurons, dose variation and off-target checks. Nonlinear compensation and off-manifold interventions must be treated as threats to interpretation.
4. **Evaluate blindly:** an evaluator independent of the claimant executes test predictions. Keep prediction timestamps/hashes prior to revealing the outcome. Never retrospectively label discovered effects preregistered.
5. **Compare with:** behavior-only baseline, native-activation-only baseline, static/frozen native explanation, random/permuted targets, intervention control, and optionally SAE explanations under matched reconstruction/computation budgets.
6. **Assess incremental EFGM signal:** record EFGM input provenance, temporal availability, missingness and frozen metric construction; use nested development-only tuning and evaluation-only scoring. Evaluate differences in predictive loss, calibration and AUROC or other preregistered proper metrics (when meaningful), with uncertainty and per-scenario failures.
7. **Publish:** reproducible artifacts, independent audit, all negative outcomes, leakage checks, failure analyses and a decision `SUPPORTED_IN_SCOPE` / `NOT_SUPPORTED` / `INVALID` / `INCONCLUSIVE`. No self-selected post-hoc threshold or universal conclusion.

## Leakage and construct validity

Do not predict an intervention from a score computed using that intervention's outcome or later-stage artifacts. Do not treat a model-generated explanation as observed ground truth. Holdouts must be disjoint by the **relevant unit** (not merely different file hash); separate prompt templates, concept clusters and correlated trajectories where required. An explanatory label is not the measured intervention response.

Define what EFGM's variables actually measure in this study, with exact collection timing and measurement uncertainty. A score's convenient name (e.g., coherence) does not confer causal interpretation. If EFGM's metrics fail baseline comparison, retain that falsification unchanged.

## Delivery boundaries

Phase 0: protocol design and controlled fixture tests (this document). Phase 1: open-weight instrumented development pilot. Phase 2: frozen blinded independent validation. Phase 3: external replication and reported generalization boundaries. Only then may **reviewed** typed observations be proposed for a Cohervia read-only adapter.

No automated deployment, permissions, governor enablement, holdout inspection, threshold promotion or claim of solving mechanistic interpretability. Do not assign an experiment registry ID until conflicts and sequencing are checked.
