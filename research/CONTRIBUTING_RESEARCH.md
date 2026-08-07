# EFGM Research Contribution Workflow

## Branch model

`main` represents the accepted canonical repository state.

Research changes should use branches such as:

```text
research/efgm-lab
experiment/<experiment-id>
candidate/<config-or-model-id>
```

The current stabilization branch is itself a research branch and should be reviewed before promotion.

## Candidate change requirements

A research PR that changes model behavior should include:

- hypothesis and null hypothesis;
- exact baseline and candidate configuration IDs;
- baseline/candidate configuration SHA-256 values;
- repository code SHA;
- assessment/dataset version and relevant input hashes;
- confirmation that research-grade scoring used strict provenance validation;
- development results;
- validation results when available;
- ablation or sensitivity evidence appropriate to the change;
- known counterexamples and regressions;
- both EFGM-derived ablation and independent-baseline comparison;
- holdout ID/custodian/hash, whether it was accessed, and confirmation that real holdout cases/labels were not tuning-visible before the candidate was frozen;
- limitations and unresolved questions.

## Missing-data discipline

A candidate must not gain apparent performance by exploiting missing observations. `unknown`, `not_applicable`, and measured `0.00` are distinct states under the canonical v2 specification. Research code must preserve that distinction.

## Promotion

Do not merge a behavior-changing candidate to `main` solely because it improves one example or development benchmark. Promotion should follow the rule in `validation/test-plan.md` and retain rejected candidates/results.

Autonomous research agents may prepare experiment branches and pull requests but should not self-promote a candidate to the canonical baseline.
