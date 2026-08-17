# EFGM-EXP-0008 — Phase 1 Instrumentation

## Status

Phase 1 implements the **non-autonomous experimental instrument** preregistered by EXP-0008.

Authoritative preregistration / containment baseline:

```text
9e40bc978f4f86eadbd65471d08a3fcb21c22d4c
```

This phase does **not** authorize autonomous trajectory generation. It adds only a deterministic fictional state machine, immutable telemetry/custody records, a deterministic telemetry-to-EFGM adapter, preregistered simple detectors, and externally supervised containment/watchdog scaffolding.

## Safety boundary

The mandatory runtime contract in `experiments/manifests/EFGM-EXP-0008-safety.yaml` remains controlling. No shell/subprocess, sockets/network clients, HTTP/browser tools, package managers, Docker/SSH, host filesystem tools, credentials, real privilege/persistence/connectivity, real peer autonomy, cyber exploitation, or production/external-service access is introduced.

A class-E `executed=true, policy_permitted=false` event means only a fictional state-machine transition. It never maps to a real host, network, authentication, credential, privilege, persistence, or security action.

## First peer-review hardening

The first Phase-1 peer review identified seven issues and produced the initial hardening pass:

1. hard-budget/output-accounting values moved outside `SyntheticActionRequest`;
2. containment and watchdog termination were latched;
3. output contradiction became an explicit supervisor observation;
4. state/write/read/message measurements became applicability-aware;
5. obstacle identity became action-local;
6. per-prefix EFGM assessments became hash-sealed;
7. completion gained deterministic acceptance criteria.

## Second adversarial peer-review hardening

The second review attempted to break those fixes through composition and custody attacks. It added controller-owned per-tool contracts, enforced supervisor termination, applicability-aware output observations, stronger assessment-chain custody, exact deterministic task acceptance, conservative mutation budgeting, and a mandatory supervised runtime path.

## Final adversarial hardening

The final review targeted the remaining controller/runtime boundary rather than the EFGM formulas. The following controls now close those findings.

### 1. Controller-owned execution identity

`trajectory_id`, `sequence_id`, `governed_subject_id`, and `root_objective` are no longer agent-visible proposal fields. They live in a frozen `ControllerExecutionIdentity` that is installed when the synthetic environment is created and injected into every telemetry record.

The model can therefore propose a tool/capability/resource/subgoal/action strategy, but it cannot establish, rename, or splice the governed subject or trajectory identity.

### 2. Identity/custody anomalies cannot disappear before telemetry

Because agent requests no longer carry trajectory/sequence/subject/root-objective identity, an agent cannot cause identity drift by changing those fields between calls. Controller-side mutation of policy/tool-contract/obstacle state or out-of-band mutation of synthetic world state is detected before the next action and converted into an immutable containment/custody anomaly event. The environment, watchdog, and supervised batch then latch terminal.

### 3. Monotonic supervisor runtime accounting and one-time binding

`model_calls`, `retries`, and elapsed time are no longer supplied on each action call. `SupervisedSyntheticExecutor` owns a `SupervisorRuntimeAccounting` context with monotonic increment methods. `ExternalWatchdog` independently retains the highest accepted snapshot and treats any rollback as a terminating accounting anomaly.

A live `SyntheticEnvironment` can be bound to a supervisor/watchdog exactly once. Constructing a fresh watchdog/executor around the same live environment to reset counters is rejected.

### 4. Effective authority remains adverse until remediated

Policy evaluation now distinguishes requested authority from the **effective current synthetic state**. If a monitor-only fictional policy violation raises privilege/connectivity beyond the normal allowed maximum, a later nominal action that requests no additional privilege is still considered out of authority while the elevated state persists.

The agent cannot appear to recover governance merely by asking for a low incremental privilege value. Recovery requires an explicit permitted state transition that actually returns effective authority to scope.

### 5. Runtime custody now binds policy, tool contracts, state, and watchdog

Each event carries canonical hashes for the policy, tool contracts, obstacle profile, initial world state, watchdog configuration, and combined runtime-custody identity. Events also bind the pre- and post-state hashes. The event-chain verifier requires state-hash continuity in addition to identity and event-hash continuity.

Per-prefix `TrajectoryAssessmentRecord` custody now includes the policy hash, watchdog hash, and combined runtime-custody hash in addition to trajectory/subject/adapter/Agent-Governance configuration identity and the raw event-head hash.

Pydantic `frozen=True` is therefore not treated as sufficient protection for nested mappings. If controller-side code mutates a nested tool-contract or policy dictionary after binding, the canonical hash changes and the next supervised boundary fails closed.

### 6. B5 remains a real pre-execution comparator

The synthetic controller now seals a `preexecution_decision_sha256` before applying the state transition. The decision binds the action proposal, controller identity, policy/runtime hashes, scope/authority facts, request denial/permitted decision, and the trusted pre-state hash.

`B5_spec_compliance_request_checker` is driven by `preexecution_spec_conflict`, not by post-execution success or failure. Detector signals explicitly record whether they occur at the `pre_execution` or `post_execution` phase of an action boundary. B1 remains post-execution; B2-B5 are request-time/pre-execution comparators.

At action-index resolution B5 and B1 can still share an index when a monitor-only action executes immediately after a pre-execution conflict decision. The phase marker preserves the causal ordering so later lead-time analysis does not accidentally treat B5 as an after-the-fact detector.

## Core components

### `src/efgm/exp0008_telemetry.py`

Defines controller-owned execution identity, the closed `SyntheticActionRequest`, supervisor-only output observations, immutable `TelemetryEvent`, pre-execution decision hashes, pre/post-state custody hashes, canonical SHA-256 event sealing, and runtime/trajectory/state continuity verification.

### `src/efgm/exp0008_environment.py`

Defines the pure in-memory fictional world, controller-owned `SyntheticToolContract`, deterministic policy engine, action-local obstacles, exact completion acceptance, effective-authority semantics, one-time supervisor binding, runtime-config integrity checks, and controller-only execution primitive.

### `src/efgm/exp0008_safety.py`

Defines containment attestation, monotonic `SupervisorRuntimeAccounting`, `ExternalWatchdog`, pre-execution budget gating, and `SupervisedSyntheticExecutor`. A budget/custody trigger terminates both the environment and batch rather than merely returning an advisory Boolean.

### `src/efgm/exp0008_adapter.py`

Implements `exp0008-environment-adapter-v0.1`. It requires a valid immutable event/runtime-custody chain, rejects containment-anomaly trajectories as scientific evidence, excludes non-applicable measurement channels from denominators, uses effective authority rather than request-only authority, and verifies assessment custody with deterministic rescoring.

### `src/efgm/exp0008_detectors.py`

Implements the five preregistered independent baselines. B5 now consumes the immutable pre-execution policy decision and detector signals preserve pre/post-execution boundary phase.

## Instrumentation invariants

```text
agent request -> cannot define trajectory/sequence/subject/root identity
agent request -> cannot define synthetic side effects
agent request -> cannot define parent-action custody
agent request -> cannot define obstacle identity
agent request -> cannot define supervisor output/memory/runtime counters
selected tool -> controller contract fixes permitted semantics
contract mismatch -> denied before execution
monitor-only policy bypass -> cannot bypass tool contract
existing over-authority -> remains adverse until effective state is reduced
known budget exceedance -> blocked before environment execution
model-call/retry/time counters -> monotonic controller-owned accounting
live environment -> exactly one supervisor/watchdog binding
nested policy/tool mutation -> custody anomaly -> batch terminal
out-of-band state mutation -> custody anomaly -> batch terminal
unknown tool -> containment event -> environment + batch terminal
no output -> output contradiction N/A
output present -> supervisor contradiction observation required
non-applicable measurement -> excluded, never counted as success
completion -> exact controller-defined acceptance state required
completion tool -> allowed policy partition only
preexecution decision -> immutable request/spec-conflict hash
B5 -> pre-execution comparator, never post-outcome derived
assessment chain -> identity + config + runtime custody + raw event head + prior assessment bound
assessment verification -> deterministic prefix rescoring required
containment anomaly -> never scientific evidence
GitHub Actions -> deterministic tests only, never autonomous EXP-0008 execution
```

## Known limitations retained deliberately

1. The environment is a synthetic analogue, not an incident reconstruction.
2. The adapter contains explicit proxies that have not been externally validated.
3. Supervisor observations and runtime-accounting increments must ultimately be produced by a controller structurally inaccessible to the model; Phase 1 defines and tests that boundary but does not authorize a model runtime.
4. The structured protocol cannot measure every semantic property of free-form model reasoning.
5. Action velocity remains adaptation pressure rather than wall-clock speed.
6. Recoverability represents synthetic mechanism availability, not demonstrated real containment effectiveness.
7. Pre/post boundary phase is more precise than action index alone, but the primary preregistered lead-time statistic remains action-index based unless a later preregistration explicitly changes it.
8. Phase 1 does not establish that EFGM predicts governance failure or that any future autonomous runtime satisfies the containment contract.

## Gate to Phase 2

Phase 2 may begin only after this final-hardened candidate passes the complete repository test matrix, a final peer review confirms the adversarial findings are closed, the Phase-1 candidate is merged, and its merge SHA is frozen.

Phase 2 remains scripted, non-autonomous, and non-evidentiary. Phase 3 autonomous development remains blocked until the environment/tool-broker/telemetry/adapter/watchdog identities, containment preflight evidence, and explicit human safety gate are frozen as required by the safety contract.
