# EFGM-EXP-0008 Phase 3 containment/readiness

## Purpose

Phase 3 readiness prepares the EXP-0008 laboratory for a later autonomous-development decision without running an autonomous model and without changing the frozen Phase-2 measurement instruments.

Passing this readiness work is necessary but not sufficient for autonomous execution.

## Frozen parent and runtime custody

Phase 3 readiness starts from the merged Phase-2 baseline:

`620dd9b85f7f05f0f04e4e34a69165510030535b`

Baseline reference:

`baseline/exp0008-phase2-instruments-2026-08-17`

The readiness evaluator verifies the Phase-2 freeze record and behavioral identities, then independently recomputes the Git blob identities of the **loaded** frozen environment/tool broker, telemetry, adapter, watchdog, detectors/comparator, and pre-execution materializer. It also verifies that the running Python major/minor is within the frozen 3.10-3.13 matrix and that Pydantic/Pydantic Core match the frozen dependency versions.

This closes the gap where a freeze artifact could remain unchanged while different runtime source or dependency versions were actually loaded.

Phase 3 does not retune S1-S5, B1-B5, equations, thresholds, candidate prerequisites, AE/CUE definitions, provenance semantics, or temporal identity semantics.

## Controller isolation

The future model is treated only as a producer of structured `SyntheticActionRequest` data. The model-facing parser rejects extra fields, so model output cannot supply trajectory identity, telemetry hashes, watchdog counters, credentials, network targets, or controller state.

The parser object deliberately owns no environment, watchdog, executor, provider client, credential, shell, network, browser, filesystem, package manager, Docker, or host-control handle.

Any tool request still enters the already-frozen synthetic policy/tool broker through the supervised controller path. An unknown tool is treated as a containment anomaly and latches both environment and supervised batch terminal.

## External containment preflight

The repository intentionally does **not** add live network or host-probing code. That preserves the preregistered boundary: containment evidence must be produced externally and consumed by the experiment harness.

The readiness evaluator validates the supplied containment vector and confirms that the attested environment/tool-broker, telemetry, adapter, and watchdog identities match the frozen Phase-2 identities. CI uses a deterministic `scripted_fixture` only to exercise this validator. That fixture describes synthetic expected controls; it is not an attestation about the GitHub runner that executes CI.

A caller may label a structurally valid candidate as `external_preflight`, but this readiness module deliberately cannot convert that label into trusted evidence. `external_containment_evidence_accepted` remains false. Trust/acceptance of real external evidence requires a separate, reviewable artifact after the evidence has actually been collected outside GitHub Actions.

## Hard budgets

The existing external watchdog remains authoritative. Model-call and retry budgets are reserved before any future provider call or retry. Wall time is monotonic. Action, state-write, output, and memory limits are preflighted. A budget failure latches terminal state for both trajectory and batch.

The readiness module contains no model-provider invocation. Its provider-call integration hook refuses before budget consumption because this PR cannot authorize execution.

## Adversarial boundary attacks

The Phase-3 readiness tests attack controller-field injection, runtime identity substitution, dependency substitution, containment-control failures, unknown tools, out-of-scope connectivity/persistence requests, hard-budget exhaustion, relabelled external evidence, human-record-only bypasses, and combined external-candidate-plus-human-record bypasses.

The expected behavior is fail-closed. In particular, even a structurally valid external candidate combined with a syntactically valid human record cannot make `authorization_eligible` or `autonomous_execution_authorized` true in this readiness implementation.

## Human safety and authorization gate

This PR can establish only readiness mechanics and the structural validity of an external containment **candidate**. It cannot accept that evidence as trusted and cannot authorize autonomous execution.

The sequence after this PR is therefore:

1. exact-head CI and adversarial review pass;
2. real external containment preflight is performed on an appropriate non-GitHub, non-network-connected host;
3. the evidence is reviewed and bound into a separate trusted evidence/authorization artifact;
4. the human makes an explicit authorization decision;
5. only an approved separate authorization artifact can unlock a future provider-call path.

This prevents the readiness evaluator, caller-created records, CI fixtures, or a relabelled evidence envelope from self-authorizing autonomous execution.

## Scientific boundary

No Phase-3 readiness output counts as EXP-0008 scientific evidence, development-trajectory evidence, or validation evidence. No autonomous model is invoked in this PR. GitHub Actions remains a deterministic test/calibration environment only and is not an authorized host for autonomous EXP-0008 trajectories.
