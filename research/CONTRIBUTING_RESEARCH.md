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
- code/config SHA or diff;
- development results;
- validation results when available;
- ablation or sensitivity evidence appropriate to the change;
- known counterexamples and regressions;
- simpler-baseline comparison;
- whether holdout data was accessed;
- limitations and unresolved questions.

## Promotion

Do not merge a behavior-changing candidate to `main` solely because it improves one example or development benchmark. Promotion should follow the rule in `validation/test-plan.md` and retain rejected candidates/results.

Autonomous research agents may prepare experiment branches and pull requests but should not self-promote a candidate to the canonical baseline.
