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
Freeze candidate + record hashes
        ↓
Evaluate externally sealed holdout
        ↓
Accept / reject / remain inconclusive
```

## Current execution sequence

The post-PR-#9 research program is deliberately sequenced so that discovered failures are tested before new model promotion:

1. **EFGM-EXP-0004** — execute Agent Governance sparse-failure diagnostics against development and validation controls.
2. **EFGM-EXP-0007** — test non-compensatory diagnostics for the canonical EFGM v2 sparse-failure problem exposed by EXP-0003 while preserving frozen `DQ`.
3. **EFGM-EXP-0005** — evaluate temporal intervention, residual state, recovery progress, and verified recovery after the prerequisite semantics have been tested.
4. **EFGM-EXP-0006** — require independently authored labels to test whether Agency Exposure and Coherent Unsafe Execution add semantic value beyond their algebraic definitions.
5. Freeze only surviving candidates before any sealed-holdout access.

The current merged research baseline is `dbbb152306c589ffb7e7f02b5b6189da737f107e` (PR #10). The earlier `fd70317e4bad193c00763a398f41db6e75700b55` commit remains the historical parent baseline for the post-PR-#9 execution program and must not be substituted for individual experiment execution SHAs. Future experiment branches should start from the current merged baseline unless explicitly reconstructing historical lineage; experiment execution SHAs must still be frozen separately.

## Non-negotiable controls

- The objective is to find where EFGM fails, not to manufacture confirming examples.
- Do not alter gold-standard labels because EFGM disagrees with them.
- Do not use holdout cases to design, tune, or select a candidate.
- **Do not store real holdout case contents or labels in a repository readable by the autonomous researcher.**
- Do not merge autonomous candidate changes directly into `main`.
- Keep the current canonical baseline available for comparison.
- Preserve counterexamples, failed candidates, and regressions.
- Record model/config/code/input identifiers for every experiment.
- Compare against both EFGM-derived ablations and independent baselines.
- Prefer one structural change at a time when causal interpretation matters.
- Never interpret an omitted metric as zero. `unknown`, `not_applicable`, and measured `0.00` are different states.
- Research-grade scoring must use strict provenance validation (`require_provenance=True` or equivalent).

## Autonomous researcher permissions

An automated researcher may:

- read repository code/docs/results;
- create novel public/simulated/sanitized development and validation test cases;
- score baselines and candidate configurations;
- run perturbation, sensitivity, mutation, and ablation analyses;
- identify counterexamples and regressions;
- prepare experimental branches or pull requests;
- document proposed changes with evidence.

It must not:

- receive or inspect sealed holdout contents before a candidate is frozen;
- redefine labels to improve EFGM performance;
- fill unknown observations with favorable defaults;
- claim scientific proof from internal tests;
- merge a candidate into the canonical baseline without human approval.

## Holdout custody

`benchmarks/holdout/` contains metadata/templates only. Real holdout cases and labels require external custody or equivalent access controls. A frozen candidate may be evaluated against a holdout only after:

1. experiment hypothesis and success/failure criteria are recorded;
2. code commit SHA is frozen;
3. scoring configuration ID and SHA-256 are recorded;
4. candidate selection is complete;
5. an access log identifies the holdout release/evaluation event.

Once exposed, those cases are no longer unseen for that tuning lineage.

## Directory roles

```text
benchmarks/development/      tuning-visible cases
benchmarks/validation/       periodic candidate comparison
benchmarks/holdout/          metadata only; actual holdout externally sealed
baselines/                   derived ablations + independent comparators
experiments/manifests/       preregistered experiment metadata
experiments/results/         immutable result summaries
experiments/counterexamples/ retained failures
experiments/rejected-candidates/ failed model/config proposals
docs/legacy/v1/              verbatim historical v1 documents
```

## Required experiment identity

At minimum preserve:

```text
code_sha
input_sha256
config_id
config_sha256
dataset_version
label_source
scorer identities/types
holdout access state
```

A human-readable config name is not enough. If two files have the same `config_id` but different SHA-256 values, they are different experimental conditions.

For post-PR-#9 experiments also preserve the **parent merged baseline SHA** separately from the **execution code SHA**. This prevents a stable parent lineage from being confused with the exact code that produced an experimental result.

## Required experiment metadata

Use `experiments/manifests/template.yaml` as the minimum record. Results should state whether they are exploratory, blinded, non-blinded, internally labeled, externally labeled, or independently replicated.

## Missing-data discipline

The autonomous researcher must never optimize EFGM by exploiting missing observations. Completed scores require no `unknown` values. Explicit `not_applicable` values may be excluded according to the canonical specification, but their rationale and scorer provenance must be retained.
