# EFGM-EXP-0008 Phase 3 containment/readiness

## Purpose

Phase 3 readiness prepares the EXP-0008 laboratory for a later autonomous-development decision without running an autonomous model and without changing the frozen Phase-2 measurement instruments.

Passing this readiness work is necessary but not sufficient for autonomous execution.

## Frozen parent

Phase 3 readiness starts from the merged Phase-2 baseline:

`620dd9b85f7f05f0f04e4e34a69165510030535b`

Baseline reference:

`baseline/exp0008-phase2-instruments-2026-08-17`

The Phase-2 freeze record, runtime instrument-set identity, and canonical report identity are checked before authorization can become possible. Phase 3 does not retune S1-S5, B1-B5, equations, thresholds, candidate prerequisites, AE/CUE definitions, provenance semantics, or temporal identity semantics.

## Controller isolation

The future model is treated only as a producer of structured `SyntheticActionRequest` data. The model-facing parser rejects extra fields, so model output cannot supply trajectory identity, telemetry hashes, watchdog counters, credentials, network targets, or controller state.

The parser object deliberately owns no environment, watchdog, executor, provider client, credential, shell, network, browser, filesystem, package manager, Docker, or host-control handle.

Any tool request still enters the already-frozen synthetic policy/tool broker through the supervised controller path.

## External containment preflight

The readiness evaluator consumes an externally produced containment attestation. All required containment booleans must pass and the attested environment/tool-broker, telemetry, adapter, and watchdog identities must match the frozen Phase-2 identities.

CI uses a deterministic `scripted_fixture` only to exercise the validator. That fixture is explicitly inadmissible as real external containment evidence and can never authorize autonomy.

## Hard budgets

The existing external watchdog remains authoritative. Model-call and retry budget is reserved before a future provider call or retry. Wall time is monotonic. Action, state-write, output, and memory limits are preflighted. A budget failure latches terminal state for both trajectory and batch.

The readiness module contains no model-provider invocation.

## Adversarial boundary attacks

The Phase-3 readiness test suite attempts to inject controller-only fields through model output, request unknown or out-of-scope synthetic actions, tamper with frozen identities, fail containment controls, exceed hard budgets, and bypass the authorization gates.

The expected behavior is fail-closed. An unknown synthetic tool is treated as a containment anomaly and terminates the supervised batch rather than merely returning a soft denial.

## Human safety and authorization gate

Readiness evaluates whether the prerequisite conditions for a later authorization decision are present. External containment evidence and explicit human safety approval are both required before `authorization_eligible` can become true.

Even if those prerequisites are eventually satisfied, **this readiness implementation is deliberately unable to set `autonomous_execution_authorized` to true**. It always remains false. A separate, explicit authorization artifact/change is required after the human reviews the real external containment evidence and makes the authorization decision.

This prevents the readiness evaluator, caller-created records, CI fixtures, or a relabelled evidence envelope from self-authorizing autonomous execution.

After exact-head CI and adversarial review pass, the next operational step is to obtain and review real external containment-preflight evidence on an appropriate non-GitHub, non-network-connected host. Only after that evidence passes should the explicit human authorization decision be requested and, if approved, recorded separately.

## Scientific boundary

No Phase-3 readiness output counts as EXP-0008 scientific evidence, development-trajectory evidence, or validation evidence. No autonomous model is invoked in this PR. GitHub Actions remains a deterministic test/calibration environment only and is not an authorized host for autonomous EXP-0008 trajectories.
