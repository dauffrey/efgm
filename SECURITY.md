# EFGM Security Policy

## Purpose

This document defines security and information-handling expectations for the Entropy-Flow Governance Model (EFGM) repository and its experimental tooling.

EFGM is an experimental governance and measurement framework. It is not a production security control, compliance engine, autonomous approval system, or substitute for formal security review.

## Supported Research State

| Identity | Status | Notes |
|---|---:|---|
| EFGM v2 | Research baseline | Canonical decision-integrity model; not a production security product |
| Package `0.2.0` | Unreleased research package | Package identity, not a model version |
| Agent Governance v0.3 | Research candidate | Experimental autonomous-agent governance extension |
| Historical v1 | Compatibility / history | Not canonical for new research |

## Reporting a Security Issue

Report sensitive repository concerns privately through an appropriate authorized channel before opening a public issue.

Potential concerns include exposed credentials or secrets, client-sensitive or personal information, production architecture/access details, confidential incident information, unsafe prototype behavior, misleading governance recommendations, or sealed-holdout leakage into the tuning-visible repository.

Do not reproduce sensitive details in a public issue, pull request, discussion, commit message, benchmark, or example.

## Information That Must Not Be Committed

Do not commit:

- passwords, tokens, API keys, private keys, certificates, or connection secrets;
- privileged account details or production access instructions;
- confidential client or government information;
- personal information unless explicitly approved for publication;
- restricted incident timelines or exploit details;
- sensitive architecture, network, host, or security-zone information;
- proprietary third-party material without authorization;
- unredacted logs containing identifiers or restricted values;
- real sealed-holdout case contents or preferred labels visible to the tuning loop.

Use public, simulated, sanitized, or explicitly approved evidence.

## Canonical Evidence Vocabulary

| Status | Meaning |
|---|---|
| `observed` | Directly supported by evidence |
| `inferred` | Estimated from indirect evidence or reviewer judgment |
| `unknown` | Evidence is insufficient to characterize the metric |
| `not_applicable` | The construct genuinely does not apply |

Do not use a parallel canonical scoring vocabulary such as `verified` / `assumed` in `MetricObservation` records.

```text
unknown != safe
0.00 != unknown
not_applicable != unknown
```

## Safe Use of EFGM Scores

In security-relevant contexts:

1. Preserve evidence, rationale, scorer identity/type, and confidence.
2. Do not use a high aggregate score to bypass a critical security control.
3. Treat observation-floor, low-percentile, candidate-prerequisite, and future veto diagnostics as distinct research mechanisms.
4. Treat material unknowns conservatively and obtain evidence before relying on the result.
5. Keep accountable human/security ownership for consequential decisions.
6. Do not use EFGM as authorization to access, test, exploit, or modify systems.
7. Do not use EFGM to override existing security, privacy, architecture, legal, regulatory, or change-management gates.

## Autonomous-Agent Security Research

```text
G  = EFGM v2 Grounding
GI = Agent Governance v0.3 Governance Integrity
AE = Agency Exposure
CUE = Coherent Unsafe Execution
0 <= CUE <= AE <= 1
```

High privilege, connectivity, persistence, coordination, or action velocity is not automatically a security failure. The experimental question is whether consequential agency remains adequately governed, observable, bounded, and recoverable.

Unknown boundary state, persistence surfaces, credential propagation, or recoverability must not be interpreted as integrity.

Because `CUE <= AE` structurally, exposure and execution must not be treated as independent orthogonal risk axes.

## Critical-Dimension Limitation

Retained counterexamples show that aggregate means can hide a sparse catastrophic failure. Therefore:

- aggregate EFGM scores are not sufficient security approval;
- critical controls must remain visible individually;
- `governance_observation_floor` is a neutral diagnostic, not a hard prerequisite verdict;
- only explicitly configured candidate-prerequisite metric paths may produce candidate-prerequisite breaches;
- candidate prerequisites, low-percentile diagnostics, and possible future veto rules are research aids, not substitutes for security policy;
- a reassuring aggregate classification must not overrule an independently known security violation.

The current candidate prerequisite list is a falsifiable research hypothesis under `EFGM-EXP-0004`, not an established enterprise control set.

## N/A Semantics

Whole-family `not_applicable` is currently supported only for **coordination governance** in a strictly single-agent scenario. The family is excluded rather than assumed perfect, and results expose applicable/excluded family names and family count.

N/A must not be used to avoid assessing a control that actually applies.

For temporal verified-recovery assessment, `not_applicable` is an evidence-backed scope claim. It requires rationale, scorer identity/type, positive confidence, and evidence references; it cannot be used as an evidence-free way to clear a residual surface.

## Temporal Intervention and Recovery

A post-intervention score is not proof that control has been restored.

Temporal states carry an explicit `sequence_id`. States from different sequences are rejected as a single transition rather than interpreted as recovery evidence. Transition results retain candidate config identity/hash, before/after input hashes, and residual-state identity when residual evidence is supplied.

The temporal research scaffold distinguishes:

### Recovery progress

A same-sequence valid `pre_intervention → post_intervention` transition with a declared intervention, higher `GI`, and lower `AE`.

This indicates directional improvement only.

### Verified recovery signal

Recovery progress plus:

- the post-intervention state itself is classified as governed;
- no remaining candidate-prerequisite breach;
- no elevated AE/CUE diagnostic;
- complete residual-state evidence;
- no material residual state marked present.

Residual-state surfaces currently include:

- credentials;
- persistence;
- environmental memory;
- coordination;
- privileges;
- scheduled actions;
- irreversible side effects;
- rollback gaps.

For a verified-recovery candidate, `clear`, `present`, and `not_applicable` residual claims require rationale, scorer identity/type, positive confidence, and evidence references. A residual status of `unknown` prevents verified recovery.

Even `verified_recovery_signal` is **not a production containment attestation**; it is an experimental research signal to be falsified under `EFGM-EXP-0005`.

## Prototype Code Security

Prototype code should:

- avoid external system calls by default;
- avoid sensitive data processing by default;
- validate input structures;
- fail closed on unknown observations rather than invent favorable values;
- expose calculated scores, applicability coverage, and diagnostic inputs clearly;
- keep scoring configurations versioned and hashable;
- record code/config/input identity for experiments;
- avoid secrets in fixtures, examples, generated reports, and CI logs.

## Dependency and Supply-Chain Guidance

- Keep dependencies minimal.
- Prefer maintained packages.
- Document dependency purpose.
- Review licenses.
- Test built artifacts, not only editable/source-tree behavior.
- Add dependency scanning before operationally meaningful distribution.

## Security Review Triggers

A formal security review should occur before EFGM is used for production autonomous-agent governance, access-control approval, incident containment/restoration decisions, regulated/privacy-impacting workflows, production release approval, tooling that processes real confidential operational data, or external publication containing sensitive evidence.

## Current Security Status

Current status: **research prototype**.

EFGM must not be used as security certification, compliance attestation, authorization to take privileged action, autonomous production go/no-go authority, or proof that an agent/workflow is safe.

```text
Keep evidence sanitized.
Keep unknowns explicit.
Keep critical controls visible.
Keep formal security authority outside the EFGM score.
```
