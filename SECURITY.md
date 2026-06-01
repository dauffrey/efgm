# Security Policy

## Purpose

This document defines security and information-handling expectations for the Entropy-Flow Governance Model (EFGM) repository.

EFGM is currently an early-stage governance framework and prototype scoring concept. The repository may contain model definitions, examples, validation material, templates, and future prototype code. Contributors and reviewers should treat the repository as a shared investigation space and avoid adding sensitive, confidential, or operationally restricted material.

---

## Supported Versions

EFGM is currently in early investigation status. No production release or formally supported version is available yet.

| Version / Branch | Supported | Notes |
|---|---:|---|
| `main` | Yes | Current investigation and review branch |
| Prototype branches | Limited | Reviewed case by case |
| Archived drafts | No | Retained for reference only |

---

## Reporting a Security Issue

If you identify a security concern in this repository, report it privately through the appropriate internal channel before opening a public issue.

Security concerns may include:

- exposed credentials;
- client-sensitive information;
- production system details;
- confidential incident information;
- sensitive architecture details;
- personal information;
- unsafe prototype behavior;
- misleading governance recommendations that could create operational risk;
- misuse of the model in a way that creates false confidence.

Do not disclose sensitive details in a public GitHub issue, pull request, discussion, commit message, or example file.

---

## Information That Must Not Be Committed

Do not commit any of the following:

| Restricted Information | Examples |
|---|---|
| Credentials | Passwords, tokens, API keys, certificates, private keys |
| Production access details | Connection strings, privileged accounts, firewall rules, VPN details |
| Client-sensitive information | Client names, internal system details, confidential workflows, unapproved documentation |
| Personal information | Names, contact details, user identifiers, employment or HR information unless explicitly approved |
| Incident-sensitive material | Raw incident timelines, security findings, exploit details, breach information |
| Restricted architecture details | Network diagrams, security zones, internal IP mappings, privileged system topology |
| Proprietary material | Vendor documentation, third-party confidential content, restricted screenshots |
| Unredacted logs | Application logs, database logs, audit logs, monitoring exports, stack traces with identifiers |

Use sanitized examples wherever possible.

---

## Sanitized Example Requirements

Examples in this repository should be generalized and safe to share.

A sanitized example should:

- remove real names, credentials, IP addresses, hostnames, client identifiers, and ticket numbers unless approved;
- avoid production-specific architecture details;
- avoid copying restricted email, chat, or incident content;
- preserve only the minimum structure needed to demonstrate the EFGM concept;
- clearly indicate when values are fictional or illustrative;
- avoid implying that the example represents an actual client or production incident.

Recommended language:

```text
This example is fictional and uses sanitized values for demonstration only.
```

---

## Model-Specific Security Considerations

EFGM is intended to support governance judgment, not replace it. Security-sensitive use of EFGM should be handled conservatively.

Do not use EFGM as:

- a substitute for security review;
- a substitute for privacy review;
- a substitute for architecture review;
- a substitute for threat modeling;
- a substitute for change management approval;
- a substitute for incident response procedures;
- a guarantee that a system is safe, correct, or compliant.

EFGM scores should be treated as decision-support signals. They should not be treated as authoritative proof of safety or readiness.

---

## Safe Use of EFGM Scores

When using EFGM in security-relevant contexts:

1. Preserve evidence and rationale for each score.
2. Distinguish verified facts from assumptions.
3. Mark unknown evidence explicitly.
4. Escalate high-entropy or low-verification cases for human review.
5. Avoid presenting provisional scores as final approval.
6. Do not use the model to override required enterprise controls.
7. Do not use a high score to bypass formal security, architecture, privacy, or change-management gates.

Recommended evidence labels:

| Label | Meaning |
|---|---|
| Verified | Supported by evidence |
| Inferred | Reasonable conclusion from available evidence |
| Assumed | Working assumption that needs validation |
| Unknown | Evidence is missing or insufficient |
| Not Applicable | Metric does not apply in the current context |

---

## Prototype Code Security

If prototype code is added to this repository, contributors should follow these rules:

- do not hard-code credentials;
- do not call external systems without explicit approval;
- do not process sensitive data by default;
- do not upload logs or datasets containing restricted information;
- validate input files before processing;
- handle errors without exposing sensitive paths, values, or system details;
- document any third-party dependencies;
- keep generated outputs sanitized.

If a prototype scoring engine is later added, it should clearly distinguish between:

- calculated scores;
- reviewer-entered scores;
- inferred scores;
- missing data;
- confidence values;
- recommended governance actions.

---

## Dependency and Supply Chain Guidance

If software dependencies are introduced later:

- use minimal dependencies;
- prefer well-maintained packages;
- document dependency purpose;
- pin versions where appropriate;
- review licenses;
- scan dependencies before release if the prototype becomes operationally relevant.

---

## Handling Sensitive Findings in Reviews

If a reviewer discovers sensitive or restricted information in this repository:

1. Do not quote the sensitive content in a public issue.
2. Notify the repository owner or responsible maintainer through an approved private channel.
3. Identify the file path and general issue type without repeating the secret or sensitive content.
4. Remove or rotate exposed credentials if applicable.
5. Replace the material with a sanitized example if the content is still useful for model validation.

Example safe report wording:

```text
Potential sensitive information found in docs/example-file.md. The file appears to include environment-specific operational details. Recommend private review and sanitization.
```

---

## Security Review Triggers

A security review should be considered before EFGM is used for any of the following:

- production release decisions;
- security incident review;
- privacy-impacting workflows;
- autonomous or semi-autonomous agent governance;
- access-control review;
- regulated data handling;
- client-facing reporting;
- external publication;
- tooling that processes real operational data.

---

## Responsible Disclosure Expectations

Contributors and reviewers are expected to act responsibly when identifying potential security concerns.

Do:

- report sensitive issues privately;
- minimize disclosure;
- preserve evidence safely;
- avoid spreading restricted information;
- support remediation and sanitization.

Do not:

- post secrets in issues or comments;
- commit unredacted logs;
- publish exploit details;
- use the repository to test unauthorized access;
- use EFGM scores to bypass required governance controls.

---

## Current Security Status

Current status: **Early-stage investigation**

EFGM is not currently a production security tool, compliance tool, or risk engine. Any security-related use should be limited, reviewed, and supported by existing enterprise governance processes.

---

## Summary

The EFGM repository should remain safe, sanitized, and reviewable.

Security expectations are simple:

```text
Do not commit sensitive information.
Do not treat EFGM scores as security approval.
Use sanitized examples.
Escalate sensitive concerns privately.
Preserve human review and formal governance controls.
```
