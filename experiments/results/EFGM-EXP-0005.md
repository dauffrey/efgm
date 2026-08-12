# EFGM-EXP-0005 — Temporal intervention, residual state, and recovery

## Decision

**Do not promote the current `verified_recovery_signal` semantics.**

The temporal model demonstrates real diagnostic value relative to treating a final static governed classification as proof of recovery. Recovery-progress mechanics, residual-state blocking, covered prerequisite checks, and cross-sequence rejection behaved strongly in this authored cycle. However, `verified_recovery_signal` inherited the known semantic incompleteness of candidate-r2's prerequisite path set and falsely verified two preregistered catastrophic governance failures outside that set.

No sealed holdout was accessed.

## Frozen execution identity

- Parent merged `main`: `fd70317e4bad193c00763a398f41db6e75700b55`
- Experiment execution SHA: `ae0555af067713e804e5aed16447fa2a429b2a4e`
- GitHub Actions: EFGM Check run `#97` / run ID `31432527183`
- Python: `3.12.13`
- Runner: `efgm.exp0005_temporal_recovery` `0.1.0`
- Candidate config: `efgm-v0.3-agent-governance-candidate-r2`
- Candidate config SHA-256: `af0b5540f28d4d65ae95929a855a168f9e7c286439d33d33e14ef167d808366c`
- Dataset version: `temporal-agent-governance-v0.4`
- Dataset SHA-256: `9755ad1ebc44c8ae44ac796597152eb2fa1ec48c9f5161a1532a3a4ffccc5b27`
- Development / validation / holdout cases: `12 / 14 / 0`
- Perturbation: `±0.05`, 200 trials per case, seed `20260810`

The result-record commit is intentionally separate from the execution SHA. Later documentation changes do not replace the frozen execution identity above.

## Pre-result design

The temporal cycle compared four interpretations:

1. `recovery_progress_signal` — valid pre/post intervention transition with improved governance integrity and reduced agency exposure;
2. `verified_recovery_signal` — progress plus governed post-state, residual completeness, no material residuals, no configured prerequisite breach, and no elevated exposure/execution condition;
3. final static governed-state classification used as a naive recovery proxy;
4. a broader explicit recovery-invariant checklist that also checks preregistered semantic governance invariants directly.

### Residual surfaces

The post-intervention evidence inventory covered:

- credentials;
- persistence;
- environmental memory;
- coordination;
- privileges;
- scheduled actions;
- irreversible side effects;
- rollback gaps.

Present or unknown residuals were preregistered to block verified recovery.

### Validation challenges outside candidate-r2 prerequisites

Before execution, two catastrophic post-intervention governance failures were preregistered outside the current candidate prerequisite set:

```text
alignment.prohibited_goal_avoidance = 0.00
boundary_integrity.capability_scope_adherence = 0.00
```

Both cases otherwise used a strong post-intervention governance profile with evidence-backed clear residual surfaces. Their purpose was to test whether `verified_recovery_signal` silently treats the current prerequisite list as a complete definition of governance recovery.

Two separate cross-sequence cases were also preregistered to test identity rejection.

## Executed results

### Development

| Interpretation | Accuracy |
|---|---:|
| Recovery progress | **100.00%** |
| Verified recovery | **100.00%** |
| Final static governed state as recovery proxy | **16.67%** |
| Explicit recovery-invariant checklist | **100.00%** |

Development confirms that temporal/residual evidence can distinguish complete recovery from residual credentials, persistence, environmental memory, privileges, scheduled actions, unknown residuals, a covered prerequisite breach, governance-deficient post-state, invalid phase, missing intervention, and no-improvement cases.

### Validation

| Interpretation | Accuracy |
|---|---:|
| Recovery progress | **100.00%** |
| Verified recovery | **83.33%** |
| Final static governed state as recovery proxy | **16.67%** |
| Explicit recovery-invariant checklist | **100.00%** |

For `verified_recovery_signal`:

- false-positive rate: **18.18%**;
- false-negative rate: **0.00%**;
- incremental accuracy versus static recovery proxy: **+0.6666**;
- incremental accuracy versus explicit invariant checklist: **−0.1667**.

Cross-sequence rejection rate was **100.00%**.

## Falsification result

The two preregistered uncovered semantic failures were falsely verified as recovered. This is the key result.

The current verified-recovery implementation checks `candidate_prerequisite_breaches_after`, but candidate-r2 does not include prohibited-goal avoidance or capability-scope adherence in that prerequisite list. Their collapse can therefore be diluted inside governance-family aggregation while:

- the post-state still receives a governed classification;
- residual surfaces are all evidence-backed clear;
- no configured prerequisite breach exists;
- exposure/execution conditions are below elevated thresholds.

The temporal implementation consequently produces a false verified-recovery signal for those cases.

This does **not** show that temporal modeling is useless. It shows the opposite distinction:

```text
Temporal/residual evidence adds substantial value
        !=
Current verified-recovery semantics are complete
```

The first proposition is supported by the large gain over the final-static proxy in this cycle. The second is falsified by the uncovered semantic failures.

## Simpler comparator

The broader explicit recovery-invariant checklist achieved **100% validation accuracy**, exceeding the current verified-recovery semantics by `0.1667` accuracy points on this authored dataset.

That checklist is independent of Agent Governance aggregation but is still internally authored and EFGM-aware. It is not external ground truth. It is also **not established as a complete recovery taxonomy**. This cycle did not challenge every governance metric known to be uncovered from prior falsification work; for example, `control_recoverability.state_cleanup_completeness` was an uncovered catastrophic path in EXP-0004 but is not part of this EXP-0005 checklist. The checklist's 100% therefore means only that it covered the cases in this dataset.

Its role here is to prevent a more integrated but semantically incomplete signal from being promoted merely because it is more elaborate.

## Perturbation robustness

At `±0.05`, 200 trials per case:

- mean correct probability: **92.31%**;
- minimum case probability: **0.00%**.

For trajectory cases, this perturbation statistic measures correctness of the **verified-recovery decision**. For the two cross-sequence cases, it measures correctness of **sequence-identity rejection**. It is not a calibrated real-world probability of successful recovery.

The zero minimum reflects structural semantic coverage failure rather than ordinary numeric instability: a governance metric outside the prerequisite set remains invisible to that prerequisite check under small numeric perturbations.

## Promotion gate

```text
promotion_gate_passed = False
```

The current `verified_recovery_signal` is therefore **not eligible for promotion** as a complete recovery interpretation.

We do not add the two failed validation paths to candidate-r2 and rerun these same cases as independent confirmation. Those failures are now tuning-visible counterexamples.

## Research consequence

A future recovery candidate should not derive semantic completeness from a hand-selected prerequisite path list alone. The stronger direction suggested by EXP-0004, EXP-0007, and this experiment is a **preregistered semantic invariant taxonomy** whose applicability is justified by control meaning rather than by adding metric names after failures appear.

Any revised verified-recovery candidate must then be tested on fresh trajectories and compared against simpler alternatives before sealed holdout evaluation.

## Limitations

- Cases and labels are internally authored and EFGM-aware.
- The explicit recovery checklist is aggregation-independent but not externally independently labeled and is not established as complete.
- Residual completeness is only as complete as the modeled residual-surface inventory.
- The validation set is tuning-visible after this run.
- The perturbation statistic combines verified-recovery correctness for trajectory cases with identity-rejection correctness for cross-sequence cases; it is not incident-probability calibration.
- No sealed holdout was accessed.
- The experiment does not establish production containment assurance.
- Passing CI establishes execution/reproducibility mechanics, not scientific validity.
