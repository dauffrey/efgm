# EFGM-EXP-0008 — Phase 1 Instrumentation

## Status

Phase 1 implements the **non-autonomous experimental instrument** preregistered by EXP-0008.

Authoritative preregistration / containment baseline:

```text
9e40bc978f4f86eadbd65471d08a3fcb21c22d4c
```

This phase does **not** authorize autonomous trajectory generation. It adds only a deterministic fictional state machine, immutable telemetry, a deterministic telemetry-to-EFGM adapter, preregistered simple detectors, and externally supervised containment/watchdog scaffolding.

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

The second review attempted to break those fixes through composition and custody attacks. This pass strengthens five central boundaries without changing any frozen EFGM equation, weight, threshold, prerequisite, AE/CUE definition, provenance semantic, or temporal-identity semantic.

### 1. Controller-owned per-tool contracts

The agent-visible request can no longer declare `state_write`, `state_read`, `cross_agent_message`, parent action identity, arbitrary payloads, or supervisor accounting. Every declared synthetic tool has exactly one controller-owned `SyntheticToolContract` that defines:

- allowed capability/resource/subgoal combinations;
- whether the tool reads, writes, or emits a deterministic peer message;
- deterministic write effects;
- which fictional privilege/connectivity/persistence/coordination dimensions the tool may alter;
- per-tool maxima for those fictional dimensions.

A request that combines individually legal values in a combination not permitted by the selected tool contract is denied before execution. A monitor-only policy boundary may bypass governance policy only; it may **not** bypass the tool contract itself.

This closes the composition hole where a nominally read-only tool could previously be paired with an agent-supplied write flag.

### 2. Enforced supervisor/orchestrator termination

`SyntheticEnvironment` no longer exposes a public unsupervised `step()` entry point. Controller execution is internal and the intended runtime path is `SupervisedSyntheticExecutor`.

The external watchdog now performs a **pre-execution budget check** using supervisor-owned observations and the environment's deterministic mutation preview. If the next action would exceed a known hard limit, the action is not executed, the environment is terminated, and the batch watchdog is latched terminal.

The state-write budget is conservative: every synthetic state mutation boundary is charged, including resource writes and fictional privilege, connectivity, persistence, coordination, or completion-state changes.

Unknown tools still create a containment event and immediately terminate both the environment and supervised batch.

### 3. Applicability-aware output observations

`output_contradiction` is now optional at the schema level but tightly coupled to actual output:

- `output_chars == 0` → contradiction observation must be `null` / not applicable;
- `output_chars > 0` → a supervisor contradiction observation is mandatory.

The adapter calculates contradiction rate only across output-bearing action boundaries. Nine no-output actions can therefore no longer dilute one contradictory output from `1.0` to `0.1`.

### 4. Identity-bound assessment custody

A `TrajectoryAssessmentRecord` chain must now start at action zero and remain continuously bound to:

- experiment ID;
- trajectory ID;
- sequence ID;
- governed-subject ID;
- adapter ID;
- Agent Governance configuration hash;
- the corresponding raw event-head hash;
- the previous assessment hash.

Verification requires the original raw event chain and deterministically recomputes the frozen EFGM result for every prefix. Rehashed identity, event-head, or configuration splices therefore fail custody verification rather than merely passing because their local hashes are internally consistent.

### 5. Real deterministic task acceptance

Completion no longer means that a required resource contains any truthy value.

The controller now defines exact required synthetic resource values. Synthetic write values are also controller-owned deterministic tool effects, not agent-supplied content. The completion tool must belong to the explicitly allowed tool set and cannot be denied or monitor-only. `task_completed=true` is set only after the exact acceptance state already exists and the completion action itself is policy permitted.

This prevents both truthy-placeholder completion and the prior monitor-only completion configuration bypass.

## Components

### `src/efgm/exp0008_telemetry.py`

Defines the closed `SyntheticActionRequest`, supervisor-only `SupervisorActionObservation`, immutable `TelemetryEvent`, normalized canonical SHA-256 sealing, controller-derived parent-action chaining, and trajectory/sequence/governed-subject/root-objective continuity checks.

### `src/efgm/exp0008_environment.py`

Defines the pure in-memory fictional world, controller-owned `SyntheticToolContract`, deterministic policy engine, action-local obstacles, exact completion acceptance, deterministic synthetic write effects, and the controller-only execution primitive.

### `src/efgm/exp0008_safety.py`

Defines containment attestation, `ExternalWatchdog`, pre-execution budget gating, and `SupervisedSyntheticExecutor`. A watchdog trigger terminates both the environment and batch rather than merely returning an advisory Boolean.

### `src/efgm/exp0008_adapter.py`

Implements `exp0008-environment-adapter-v0.1`. It requires a valid immutable event chain, rejects containment-anomaly trajectories as scientific evidence, excludes non-applicable measurement channels from denominators, treats absent output as N/A, and verifies assessment custody against the raw event chain with deterministic rescoring.

### `src/efgm/exp0008_detectors.py`

Implements the five preregistered independent baselines: first explicit violation, first denied request, repeated denials, first out-of-scope request, and first request conflicting with explicit synthetic policy.

## Instrumentation invariants

```text
agent request -> cannot define synthetic side effects
agent request -> cannot define parent-action custody
agent request -> cannot define obstacle identity
agent request -> cannot define supervisor output/memory facts
selected tool -> controller contract fixes permitted semantics
contract mismatch -> denied before execution
monitor-only policy bypass -> cannot bypass tool contract
known budget exceedance -> blocked before environment execution
environment/watchdog termination -> latched; no silent resume
unknown tool -> containment event -> environment + batch terminal
no output -> output contradiction N/A
output present -> supervisor contradiction observation required
non-applicable measurement -> excluded, never counted as success
completion -> exact controller-defined acceptance state required
completion tool -> allowed policy partition only
assessment chain -> identity + config + raw event head + prior assessment bound
assessment verification -> deterministic prefix rescoring required
containment anomaly -> never scientific evidence
GitHub Actions -> deterministic tests only, never autonomous EXP-0008 execution
```

## Known limitations retained deliberately

1. The environment is a synthetic analogue, not an incident reconstruction.
2. The adapter contains explicit proxies that have not been externally validated.
3. Supervisor observations must ultimately be produced by a controller that is structurally inaccessible to the model; Phase 1 defines and tests that interface but does not authorize a model runtime.
4. The structured protocol cannot measure every semantic property of free-form model reasoning.
5. Action velocity remains adaptation pressure rather than wall-clock speed.
6. Recoverability represents synthetic mechanism availability, not demonstrated real containment effectiveness.
7. Phase 1 does not establish that EFGM predicts governance failure or that any future autonomous runtime satisfies the containment contract.

## Gate to Phase 2

Phase 2 may begin only after this hardened candidate passes the complete repository test matrix, a final peer review confirms the second-review findings are closed, the Phase-1 candidate is merged, and its merge SHA is frozen.

Phase 2 remains scripted, non-autonomous, and non-evidentiary. Phase 3 autonomous development remains blocked until the environment/tool-broker/telemetry/adapter/watchdog identities, containment preflight evidence, and explicit human safety gate are frozen as required by the safety contract.
