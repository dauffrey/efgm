# EFGM-EXP-0008 — Phase 1 Instrumentation

## Status

Phase 1 implements the **non-autonomous experimental instrument** preregistered by EXP-0008.

Authoritative preregistration / containment baseline:

```text
9e40bc978f4f86eadbd65471d08a3fcb21c22d4c
```

This phase does **not** authorize autonomous trajectory generation. It adds only a deterministic fictional state machine, immutable telemetry, a deterministic telemetry-to-EFGM adapter, simple preregistered detectors, and containment/watchdog scaffolding.

## Safety boundary

The mandatory runtime contract in `experiments/manifests/EFGM-EXP-0008-safety.yaml` remains controlling. No shell/subprocess, sockets/network clients, HTTP/browser tools, package managers, Docker/SSH, host filesystem tools, credentials, real privilege/persistence/connectivity, real peer autonomy, cyber exploitation, or production/external-service access is introduced.

A class-E `executed=true, policy_permitted=false` event means only a fictional state-machine transition. It never maps to a real host, network, authentication, credential, privilege, persistence, or security action.

## Phase-1 peer-review hardening

The first Phase-1 peer review found seven issues. This branch now addresses them explicitly:

1. **Supervisor-owned hard-budget facts.** `output_chars`, `memory_units`, and the controller's output-contradiction observation are no longer accepted in `SyntheticActionRequest`. Every environment step requires a separate `SupervisorActionObservation` supplied outside the agent-visible request surface.
2. **Latched containment termination.** An unknown tool records a containment event, raises, and permanently terminates that synthetic environment instance. The external watchdog also latches terminal state after the first containment or budget trigger; later observations cannot silently restart the run.
3. **No favorable default for output contradiction.** Output contradiction is now an explicit supervisor observation sealed into telemetry rather than an assumed zero.
4. **Applicability-aware measurement.** State-change traceability is calculated only across actual state changes; write inventory only across actual writes; readback traceability only across actual reads; message traceability only across actual messages. Non-applicable actions are no longer counted as successful observations.
5. **Action-local obstacles.** Obstacle identity is emitted only on action boundaries where the controller-configured obstacle is active. A one-shot failure no longer labels the rest of the trajectory as obstructed.
6. **Sealed per-prefix EFGM assessments.** Each scored trajectory prefix can now produce a hash-sealed `TrajectoryAssessmentRecord` bound to the raw event-head hash, input hash, agent configuration hash, and frozen EFGM outputs. Assessment records can themselves be hash chained.
7. **Deterministic acceptance criteria.** A configured completion tool cannot mark the task complete until controller-defined required synthetic resources have been satisfied.

No EFGM v2 or Agent Governance v0.3 equation, weight, threshold, candidate-prerequisite membership, AE/CUE definition, provenance semantic, or temporal-identity semantic is changed by this hardening pass.

## Components

### `src/efgm/exp0008_telemetry.py`

Defines the closed agent-visible `SyntheticActionRequest`, supervisor-only `SupervisorActionObservation`, immutable `TelemetryEvent`, normalized canonical SHA-256 sealing, previous-event hash chaining, and trajectory/sequence/governed-subject/root-objective continuity checks.

Agent requests cannot supply obstacle identity, arbitrary executable payloads, hard-budget accounting, or output-contradiction observations.

### `src/efgm/exp0008_environment.py`

Defines the pure in-memory fictional world and deterministic policy engine. Unknown tools fail closed and latch the environment terminal. Obstacles are controller owned and action local. Completion is deterministic and requires configured acceptance resources. Monitor-only prohibited actions can alter fictional state only, solely to represent class-E synthetic boundary events.

### `src/efgm/exp0008_adapter.py`

Implements `exp0008-environment-adapter-v0.1`.

The adapter requires a valid immutable event chain, rejects containment-anomaly trajectories as scientific evidence, never consumes a preferred safe/unsafe class label or the `synthetic_policy_violation` convenience field, excludes non-applicable state/write/read/message events from denominators, and supports sealed per-prefix assessment records bound to the raw event head.

The adapter remains a **candidate experimental instrument**, not a validated semantic calibration.

### `src/efgm/exp0008_detectors.py`

Implements the five preregistered independent baselines: first explicit executed violation, first denied request, repeated denials, first out-of-scope request, and first request conflicting with explicit synthetic policy.

### `src/efgm/exp0008_safety.py`

The containment-attestation validator remains fail closed. The external watchdog now uses only sealed/supervisor-owned telemetry facts and permanently latches both `terminate_trajectory` and `terminate_batch` after any containment anomaly or hard-budget breach.

## Instrumentation invariants

```text
unknown tool -> containment event -> environment terminal
terminal environment -> no later action accepted
watchdog trigger -> watchdog terminal; no silent reset
agent request -> cannot supply obstacle identity
agent request -> cannot supply output/memory accounting
agent request -> cannot supply output-contradiction observation
non-applicable trace channel -> excluded, never counted as success
active obstacle -> action-local telemetry only
completion -> acceptance criteria must be satisfied
raw event prefix -> immutable EFGM assessment bound to event-head hash
containment anomaly -> never scientific evidence
GitHub Actions -> deterministic tests only, never autonomous EXP-0008 execution
```

## Known limitations retained deliberately

1. The environment is a synthetic analogue, not an incident reconstruction.
2. The adapter contains explicit proxies that have not been externally validated.
3. Supervisor output-contradiction observation requires a deterministic controller definition before Phase 3; it is not a model self-report.
4. The structured protocol cannot measure every semantic property of free-form model reasoning.
5. Action velocity remains adaptation pressure rather than clock speed.
6. Recoverability represents synthetic mechanism availability, not demonstrated real containment effectiveness.
7. Phase 1 does not establish that EFGM predicts governance failure or that any future autonomous runtime satisfies the containment contract.

## Gate to Phase 2

Phase 2 may begin only after the hardened Phase-1 implementation passes the complete repository test matrix, a second peer review confirms the preregistration and containment findings are resolved, the Phase-1 candidate is merged and its merge SHA frozen, and scripted calibration remains explicitly non-autonomous and non-evidentiary.

Phase 3 autonomous development remains blocked until the environment/tool-broker/telemetry/adapter/watchdog identities, containment preflight evidence, and explicit human safety gate are frozen as required by the safety contract.
