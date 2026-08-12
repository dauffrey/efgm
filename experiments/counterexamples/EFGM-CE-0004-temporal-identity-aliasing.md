# EFGM-CE-0004 — Temporal identity aliasing

## Status

Material falsification counterexample for the experimental Agent Governance v0.3 temporal-recovery layer. This does **not** modify canonical EFGM v2 and does not promote a model change.

## Hypothesis challenged

The temporal layer treats a shared `sequence_id` as sufficient evidence that two states belong to one recovery trajectory.

The intended semantic claim is stronger: recovery should compare two states of the **same governed subject/agent trajectory**, not merely two assessments carrying the same caller-supplied string.

## Reproduction

Starting from the known complete-recovery trajectory used by EFGM-EXP-0005:

1. build a degraded `pre_intervention` state and a governed `post_intervention` state;
2. retain the same `sequence_id`;
3. replace the post-state assessment `task_id` (and nested decision `task_id`) with unrelated identifiers;
4. keep the otherwise valid intervention, provenance, governance improvement, exposure reduction, and clear residual-state evidence;
5. call `score_state_transition(...)`.

The current implementation records the different `from_task_id` and `to_task_id` but performs no continuity check beyond `before.sequence_id == after.sequence_id`.

The falsification test is preserved in:

`tests/test_temporal_identity_continuity.py`

It asserts the observed current behavior: different assessment identities can still yield `verified_recovery_signal == True` when they share the same sequence label.

## Why this matters

This is not another compensatory-aggregation failure. It is a **trajectory identity / evidence-binding failure**.

A verified-recovery signal is meaningful only if the before and after observations are attributable to the same governed subject. Otherwise an unrelated clean state can be paired with a degraded state and described as recovery.

The current EFGM-EXP-0005 identity tests only reject **different sequence IDs**. They do not falsify false continuity produced by reusing one sequence ID across different assessment identities.

## Diagnosis

Current structural guard:

```text
before.sequence_id == after.sequence_id
```

Current missing invariant:

```text
same sequence label != demonstrated same governed subject
```

`task_id` equality is not necessarily the correct production rule because state-specific task identifiers may legitimately change across a trajectory. The underlying requirement is a separately modeled, evidence-backed subject/agent identity that remains stable across the transition.

## Candidate research change

Do **not** silently equate `task_id` with subject identity.

Test an explicit temporal identity binding such as:

```text
subject_id / agent_instance_id
identity evidence reference(s)
identity provenance
```

with transition rules requiring before/after identity continuity before either recovery signal can be true.

Competing alternatives should include:

- current `sequence_id`-only behavior;
- strict task-ID equality (simple but potentially over-restrictive baseline);
- explicit subject identity continuity;
- evidence-backed subject identity continuity.

## Required falsification cases

A future experiment should include:

- same subject, changed task ID — should remain comparable;
- different subject, same sequence ID — must be rejected;
- same subject, ambiguous identity evidence — verified recovery must be blocked;
- recycled/restarted agent identity after intervention;
- delegated successor agent with inherited residual capability;
- cloned process/session sharing sequence metadata;
- benign state renaming to measure false rejection.

## Holdout discipline

No holdout case was accessed or materialized. This counterexample is internally authored development evidence and cannot establish external validity.

## Decision

The current temporal verified-recovery candidate should remain ineligible for promotion. Existing EXP-0005 semantic-completeness failures remain valid; this counterexample adds an independent identity-continuity failure mode.
