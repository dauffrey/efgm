# EFGM Security Policy

## Purpose

This document defines security and information-handling expectations for the Entropy-Flow Governance Model (EFGM) repository and its experimental tooling.

EFGM is an experimental governance and measurement framework. It is not a production security control, compliance engine, autonomous approval system, or substitute for formal security review.

## Supported Research State

| Version / Branch | Status | Notes |
|---|---:|---|
| Canonical v2 on `main` | Research baseline | Decision-integrity baseline; not a production security product |
| Experimental v0.3 | Research candidate | Autonomous-agent governance research only |
| Historical v1 | Compatibility / history | Not canonical for new research |

## Reporting a Security Issue

Report sensitive repository concerns privately through an appropriate authorized channel before opening a public issue.

Potential concerns include:

- exposed credentials or secrets;
- client-sensitive or personal information;
- production architecture or access details;
- confidential incident information;
- unsafe prototype behavior;
- misleading governance recommendations that could create false confidence;
- sealed-holdout leakage into the tuning-visible repository.

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

## Sanitized Example Requirements

Repository examples should:

- remove real credentials, IPs, internal hostnames, private identifiers, and client-specific details;
- preserve only the minimum structure required to test the research question;
- identify synthetic or fictional values when appropriate;
- avoid implying that a synthetic scenario reconstructs a real client or security incident.

## Canonical Evidence Vocabulary

Security-relevant EFGM assessments must use the same observation states as the executable model:

| Status | Meaning |
|---|---|
| `observed` | Directly supported by evidence |
| `inferred` | Estimated from indirect evidence or reviewer judgment |
| `unknown` | Evidence is insufficient to characterize the metric |
| `not_applicable` | The construct genuinely does not apply |

Do not use a parallel canonical scoring vocabulary such as `verified` / `assumed`. Those terms may appear in prose, but when evidence enters an EFGM `MetricObservation` it must map to the executable states above.

Security invariant:

```text
unknown != safe
0.00 != unknown
not_applicable != unknown
```

## Safe Use of EFGM Scores

In security-relevant contexts:

1. Preserve evidence, rationale, scorer identity/type, and confidence.
2. Do not use a high aggregate score to bypass a critical security control.
3. Inspect prerequisite/critical-dimension diagnostics where available.
4. Treat material unknowns conservatively and obtain evidence before relying on the result.
5. Keep accountable human/security ownership for consequential decisions.
6. Do not use EFGM as authorization to access, test, exploit, or modify systems.
7. Do not use EFGM to override existing security, privacy, architecture, legal, regulatory, or change-management gates.

## Autonomous-Agent Security Research

Experimental v0.3 research distinguishes:

```text
G  = v2 Grounding
GI = v0.3 Governance Integrity
AE = Agency Exposure
CUE = Coherent Unsafe Execution
```

High privilege, connectivity, persistence, coordination, or action velocity is not automatically a security failure. The experimental question is whether consequential agency remains adequately governed, observable, bounded, and recoverable.

Unknown boundary state, unknown persistence surfaces, unknown credential propagation, or unknown recoverability must not be interpreted as integrity.

## Critical-Dimension Limitation

Retained EFGM counterexamples show that aggregate means can hide a sparse catastrophic failure. Therefore:

- aggregate EFGM scores are not sufficient security approval;
- critical controls must remain visible individually;
- non-compensatory prerequisite/veto/low-percentile diagnostics are experimental research aids, not substitutes for security policy;
- a reassuring aggregate classification must not overrule an independently known security violation.

## Temporal Intervention and Recovery

For autonomous-agent experiments, a post-intervention score is not proof that control has been fully restored.

Security review should consider residual state such as:

- cached credentials;
- persistent files or external memory;
- delegated goals in peer agents;
- retained privileges;
- queues or scheduled actions;
- side effects that rollback cannot reverse;
- observability gaps during containment.

The experimental `recovery_signal` in `temporal_v0_3.py` indicates only that Governance Integrity increased and Agency Exposure decreased after a declared intervention. It is not a production containment attestation.

## Prototype Code Security

Prototype code should:

- avoid external system calls by default;
- avoid sensitive data processing by default;
- validate input structures;
- fail closed on unknown observations rather than invent favorable values;
- expose calculated scores and diagnostic inputs clearly;
- keep scoring configurations versioned and hashable;
- avoid secrets in fixtures, examples, generated reports, and CI logs.

## Dependency and Supply-Chain Guidance

- Keep dependencies minimal.
- Prefer maintained packages.
- Document dependency purpose.
- Review licenses.
- Test built artifacts, not only editable/source-tree behavior.
- Add dependency scanning before any operationally meaningful distribution.

## Security Review Triggers

A formal security review should occur before EFGM is used for:

- production autonomous-agent governance;
- access-control approval;
- security incident containment or restoration decisions;
- regulated or privacy-impacting workflows;
- production release approval;
- tooling that processes real confidential operational data;
- external publication that may contain sensitive evidence.

## Current Security Status

Current status: **research prototype**.

EFGM must not be used as:

- security certification;
- compliance attestation;
- authorization to take privileged action;
- autonomous production go/no-go authority;
- proof that an agent or workflow is safe.

The repository security principle is:

```text
Keep evidence sanitized.
Keep unknowns explicit.
Keep critical controls visible.
Keep formal security authority outside the EFGM score.
```