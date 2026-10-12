# Interpretable and governable AI — falsification-first research program

**Status:** prospective research proposal and elementary evidence-packet gate; no scientifically validated explanation, complete introspection or autonomous authority. Created October 12, 2026.

## Central problem

No general method currently provides complete, uniquely causal, robust and independently verified explanations of arbitrary neural-network behavior. Model outputs, verbal explanations, reasoning traces and learned features are not themselves faithful causal explanations. Likewise an independent monitor cannot be assumed reliable merely because it is smaller, isolated or accurate on development cases.

**Ultimate aspiration:** explain relevant mechanisms, correctly anticipate consequential behavior under model/task changes, and enforce explicit external authority boundaries even when explanations or monitors fail. The phrase `100% solved` is **not an achieved status**; finite behavioral tests cannot justify an unrestricted guarantee over all models, inputs and environments.

## Two distinct propositions to test

1. **Explanation validity (EFGM-owned):** For a *specified* model, task distribution, intervention family and causal estimand, a frozen mechanistic explanation predicts changes under blinded, independent interventions better than preregistered simple/null baselines. Report fidelity, uncertainty, intervention-distribution sensitivity, counterexamples, unobserved mechanisms and model-change degradation. Support means local, scoped evidence, not exhaustive model understanding.
2. **Oversight/control validity (Cohervia-owned):** A separately evaluated monitor detects consequential degradation at a preregistered false-alarm budget and lead-time criterion. An independently enforced, deterministic policy rejects unauthorized actions even if the monitor or explanation fails. Assess intervention utility against shadow-only, action-only, invariant-checklist and abstention baselines; monitor/agent collusion, distribution shift and loss of evidence are explicit failure modes.

Do not reuse EFGM Decision Quality, CRC, Governance Integrity, Agency Exposure or Coherent Unsafe Execution as if they were validated causal interpretability metrics. Preserve EFGM v2, Agent Governance v0.3, negative EXP-0009/0010 findings, frozen hashes and previous experiment identities.

## Evidence strata and required controls

| Stratum | Available evidence | Permissible conclusion |
| --- | --- | --- |
| Schema/test only | Fabricated fixtures or untrusted self-reported packet | Implementation contract exercised; **no scientific finding** |
| Development causal probe | Instrumented open-weight model, targeted intervention, null control | Candidate local effect; no generalization |
| Independent validation | Frozen protocol/model, disjoint test distribution, blinded external evaluator, negatives, uncertainty | Scoped inference, subject to independent review |
| Sealed confirmation | Independent custody, approved preregistration, holdout accessed only after freeze | Scoped confirmatory result, positive, negative or inconclusive |
| Operational study | Explicit authorization, independent enforcement and resource/permission isolation | Evidence only for the tested deployment conditions |

A model that only exposes a text API generally does **not** expose hidden activations or weights needed to verify a mechanistic causal claim. Mark internals `unknown`; behavioral monitorability must not be relabeled mechanistic understanding.

## Mandatory prospective study design

- Freeze subject model/checkpoint and accessible representation, intervention types, estimand, data-generating process, seed/sample allocation, metrics, error bars, baselines, missingness and success/failure/inconclusive decision rules **before evaluation**.
- Include placebo/sham interventions, negative controls, ablations, surrogate-vs-original fidelity and backup-path tests.
- Check explanation prediction outside construction prompts, across tasks, checkpoints and plausible model updates, with counterexample retention.
- Measure false alarms, detection, lead time, intervention cost, completeness of available evidence and calibration. Do not combine these into one reassuring composite when critical dimensions fail.
- Require blinded independent evaluators; holdout cases/labels and reconstruction metadata remain inaccessible to research/autonomous agents until independently released after freeze.
- Admit failures and partial or unidentifiable explanations; neither a high AUC nor a complete packet proves full causal coverage.
- No automatic model, metric, threshold, label or policy changes from a failing experiment. Candidate revisions require new preregistration and human approval.

## Executable phase-0 infrastructure

`efgm.interpretability_evidence.assess_interpretability_claim` performs **mechanical checks of self-reported evidence-packet fields** only. It returns `INVALID`, `INSUFFICIENT_EVIDENCE`, or `READY_FOR_EXTERNAL_AUDIT`; the last is not a PASS or a scientific finding. The packet pins a subject model, protocol, development/evaluation dataset and evidence-manifest hash; it demands separately named proposer/evaluator, declared pre-evaluation freeze, zero *reported* known counterexamples and observed-status declarations for causal intervention, negative control, independent replication and held-out evaluation.

These are assertions, **not** authentication, raw evidence verification, distribution-disjointness proof, sealed-custody proof or estimation of causal effect. The function always returns `scientific_claim_validated=False` and `grants_authority=False`. Even an apparently complete packet may be fabricated or semantically wrong. External custody and independently executed evaluation remain mandatory.

## Next gated milestones

1. Implement a small, permitted open-weight-model causal intervention adapter in an isolated, approved development environment. Until then: no mechanistic result.
2. Preregister independent quantitative hypotheses and baselines with adversarial controls. Avoid inventing fixed universal thresholds.
3. Freeze the first public development run and preserve all counterexamples; follow with an independent validation set, then externally sealed confirmatory custody.
4. Transfer *reviewed, versioned, evidence-backed observations only* through a separately reviewed adapter into Cohervia's existing observation/audit core.
5. Evaluate Cohervia monitoring in shadow mode before any independent deterministic enforcement study. Cohervia Scientist has no holdout, permission or self-promotion authority.

## External literature (research context, not inherited evidence)

- Guan et al. (2026), *Monitoring Monitorability*, https://proceedings.mlr.press/v306/guan26h.html
- Asiaee (2026), *Certified Interventional Fidelity*, https://proceedings.mlr.press/v337/asiaee26d.html
- NIST CAISI (2026), *Challenges to the monitoring of deployed AI systems*, https://www.nist.gov/publications/challenges-monitoring-deployed-ai-systems-center-ai-standards-and-innovation

**Ownership boundary:** EFGM owns candidate measurement and causal-claim research. Cohervia owns independent monitoring/oversight architecture and future authority studies. Neither may self-certify unrestricted safety, completeness or universal correctness.
