# EFGM Benchmark v0.2 — Agentic Governance

## Status

Controlled synthetic internal benchmark for the experimental EFGM v0.3 agent-governance extension.

This benchmark does **not** modify the frozen v0.2 baseline and does **not** claim external predictive validity.

## Scope

The benchmark tests whether governance-specific dimensions add information when an autonomous agent remains cognitively coherent and task-effective.

Black Hat USA 2026 is used only as empirical inspiration for generic failure classes. No benchmark case is intended to reproduce, identify, or score that incident.

## Composition

- 132 cases
- 66 preferred/mutated pairs
- 11 scenario families
- 88 development cases
- 44 validation cases
- no external holdout

Canonical dataset SHA-256:

```text
d7495d203f8a9e37ab777b4f4bbf4395f43a4f7ed3e306f684dff65b41f4ca5b
```

## Scenario families

- `boundary_crossing`
- `privilege_accumulation`
- `capability_acquisition`
- `credential_propagation`
- `environmental_memory`
- `emergent_coordination`
- `observability_gap`
- `control_recoverability`
- `goal_persistence`
- `tool_environment_adaptation`
- `coherent_unsafe_execution`

## Controlled-pair design

Within each preferred/mutated pair:

- v2 task/decision observations are identical;
- the mutated case changes only experimental governance and agency-amplification observations;
- the preferred label reflects the more governed agent state;
- an independent six-criterion governance checklist is retained as a structurally simpler comparator.

This intentionally asks whether v2 task-flow quality alone can detect a governance failure that does not degrade cognitive coherence.

## Materialization

```bash
efgm-agent-experiment --materialize-dataset /tmp/efgm-benchmark-v0.2.jsonl --sensitivity-trials 1
```

Any case-content change changes the canonical hash and requires a new benchmark version or an explicit benchmark revision.
