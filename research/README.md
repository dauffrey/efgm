# EFGM Research Laboratory

This directory defines the operating rules for falsification-oriented EFGM research.

## Research loop

```text
Generate hypothesis/counterexample
        ↓
Score frozen baseline(s)
        ↓
Analyze failure mechanism
        ↓
Propose one justified candidate change
        ↓
Run development tests + ablations
        ↓
Run validation tests
        ↓
Freeze candidate
        ↓
Evaluate sealed holdout
        ↓
Accept / reject / remain inconclusive
```

## Non-negotiable controls

- The objective is to find where EFGM fails, not to manufacture confirming examples.
- Do not alter gold-standard labels because EFGM disagrees with them.
- Do not use holdout cases to design, tune, or select a candidate.
- Do not merge autonomous candidate changes directly into `main`.
- Keep the current canonical baseline available for comparison.
- Preserve counterexamples, failed candidates, and regressions.
- Record model/config/code identifiers for every experiment.
- Compare against simpler baselines.
- Prefer one structural change at a time when causal interpretation matters.

## Autonomous researcher permissions

An automated researcher may:

- read repository code/docs/results;
- create novel public/simulated/sanitized test cases;
- score baselines and candidate configurations;
- run perturbation, sensitivity, mutation, and ablation analyses;
- identify counterexamples and regressions;
- prepare experimental branches or pull requests;
- document proposed changes with evidence.

It must not:

- expose or tune on sealed holdouts;
- redefine labels to improve EFGM performance;
- claim scientific proof from internal tests;
- merge a candidate into the canonical baseline without human approval.

## Directory roles

```text
benchmarks/development/      tuning-visible cases
benchmarks/validation/       periodic candidate comparison
benchmarks/holdout/          sealed cases
baselines/                   simpler comparison models
experiments/manifests/       preregistered experiment metadata
experiments/results/         immutable result summaries
experiments/counterexamples/ retained failures
experiments/rejected-candidates/ failed model/config proposals
```

## Required experiment metadata

Use `experiments/manifests/template.yaml` as the minimum record. Results should state whether they are exploratory, blinded, non-blinded, internally labeled, externally labeled, or independently replicated.
