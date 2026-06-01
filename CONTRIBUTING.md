# Contributing to EFGM

## Purpose

This repository is an investigation workspace for the **Entropy-Flow Governance Model (EFGM)**.

Contributions should help reviewers evaluate, challenge, refine, or validate the model. The goal is not to defend the model as complete. The goal is to improve its clarity, usefulness, evidence basis, and practical governance value.

EFGM is currently an early-stage conceptual and operational framework. Contributions should preserve that positioning.

---

## Contribution Principles

Contributions should follow these principles:

1. **Be evidence-based**  
   Prefer examples, observed patterns, test results, reviewer feedback, or traceable rationale over unsupported claims.

2. **Avoid overclaiming**  
   Do not present EFGM as a proven scientific law, production-ready risk engine, trained AI model, or replacement for existing governance frameworks.

3. **Preserve model clarity**  
   Changes should make the model easier to understand, test, or apply.

4. **Separate fact from interpretation**  
   Clearly distinguish verified evidence, inference, assumptions, unknowns, and open questions.

5. **Protect sensitive information**  
   Do not contribute client-sensitive, confidential, restricted, personal, credential, or production operational information.

6. **Support practical validation**  
   The strongest contributions are those that help test whether EFGM works in real scenarios.

---

## Evidence Labels

When adding analysis, examples, or review comments, use the following labels where appropriate.

| Label | Meaning |
|---|---|
| Verified | Supported by direct evidence, source material, test output, or reviewer-confirmed fact |
| Inferred | Reasonable conclusion based on available evidence |
| Assumed | Working assumption used for analysis but not independently verified |
| Unknown | Not enough evidence available to determine |
| Not Applicable | Metric, assumption, or concern does not apply in the current context |

Example:

```text
Status: Inferred
Rationale: The deployment checklist is complete, but rollback validation evidence was not available in the reviewed package.
```

---

## What to Contribute

Useful contributions include:

- clarifications to model terminology;
- improvements to metric definitions;
- better scoring examples;
- additional validation scenarios;
- reviewer questions or critique;
- assumptions that should be made explicit;
- evidence of where the model succeeds or fails;
- comparisons with related governance, risk, AI, resilience, or systems frameworks;
- corrections to unclear, duplicated, or inconsistent documentation;
- improvements to templates and scorecards;
- prototype input or output schema refinements.

---

## What Not to Contribute

Do not contribute:

- credentials, secrets, tokens, or private keys;
- production incident details that are not approved for sharing;
- client-sensitive architecture diagrams or system records;
- personal information;
- confidential government, CGI, vendor, or third-party material;
- unapproved screenshots from restricted systems;
- claims that EFGM is proven beyond its current validation state;
- unmarked assumptions presented as fact.

Use sanitized examples wherever possible.

---

## Repository Areas

| Area | Purpose |
|---|---|
| `docs/` | Core model documentation, glossary, white paper, definitions, and positioning |
| `examples/` | Worked examples showing how EFGM may be applied |
| `governance/` | Responsible-use principles and governance boundaries |
| `references/` | Related frameworks and comparison material |
| `templates/` | Reusable assessment and scorecard templates |
| `validation/` | Test plans, assumptions, open questions, and validation artifacts |

---

## Contribution Workflow

### 1. Review Existing Material

Before proposing a change, review the relevant existing files.

For example:

- model changes should be checked against `docs/model-definition.md`;
- metric changes should be checked against `docs/metric-definitions.md`;
- terminology changes should be checked against `docs/glossary.md`;
- validation comments should be checked against `validation/test-plan.md`, `validation/assumptions.md`, and `validation/open-questions.md`.

### 2. Identify the Type of Change

Classify your contribution as one of the following:

| Change Type | Description |
|---|---|
| Documentation | Clarifies or improves explanatory content |
| Metric | Adds, removes, or changes a metric definition |
| Model | Changes formula, variables, classification bands, or governance loop |
| Example | Adds or improves a worked scenario |
| Validation | Adds test results, assumptions, open questions, or reviewer feedback |
| Governance | Improves responsible-use guidance or limitations |
| Reference | Adds comparison with related frameworks |
| Maintenance | Fixes formatting, links, typos, or repository structure |

### 3. Explain the Rationale

Each meaningful change should explain:

- what changed;
- why it changed;
- what evidence or reasoning supports it;
- whether it affects scoring, interpretation, or governance action;
- whether it introduces a new assumption or open question.

### 4. Submit the Change

Use a branch and pull request where possible.

Suggested branch naming:

```text
feature/add-incident-example
fix/metric-definition-clarity
docs/update-glossary
validation/add-reviewer-feedback
```

Suggested commit format:

```text
Add incident review example
Refine context decay definition
Update validation assumptions
Fix README repository structure
```

---

## Pull Request Checklist

Before submitting a pull request, confirm:

- [ ] The change is aligned with the current EFGM positioning.
- [ ] The change avoids overclaiming or false certainty.
- [ ] Any assumptions are clearly marked.
- [ ] Any evidence is traceable or described.
- [ ] No sensitive, confidential, or restricted information is included.
- [ ] Markdown formatting is clean and readable.
- [ ] Links and file paths are correct.
- [ ] Related documents are updated if necessary.
- [ ] New metrics or scoring changes include rationale.
- [ ] New examples are sanitized.

---

## Adding or Changing Metrics

Metric changes require extra care because they affect scoring and interpretation.

When proposing a metric change, include:

| Field | Required Information |
|---|---|
| Metric Name | Name of the metric |
| Category | Entropy or Flow Quality |
| Direction | Higher is better or higher is worse |
| Definition | Clear operational definition |
| Evidence | How the metric can be observed |
| Formula | Suggested calculation, if applicable |
| Scoring Range | Expected `0.00–1.00` interpretation |
| Rationale | Why the metric matters |
| Risks | Where the metric may be subjective or misleading |

Avoid adding metrics that significantly overlap with existing metrics unless the distinction is clear.

---

## Adding Examples

Examples should be practical, sanitized, and structured.

Recommended example format:

```markdown
# Example Title

## Scenario
## Objective
## Evidence Reviewed
## Entropy Assessment
## Flow-Quality Assessment
## Score Calculation
## Classification
## Recommended Governance Action
## Lessons Learned
## Limitations
```

Examples should show how the model behaves, including where the model may be uncertain or limited.

---

## Validation Contributions

Validation contributions are especially valuable.

Useful validation inputs include:

- scenario test results;
- reviewer scoring comparisons;
- disagreements between reviewers;
- false positives;
- false negatives;
- unclear scoring cases;
- domain-specific weighting observations;
- cases where EFGM added value;
- cases where EFGM added unnecessary overhead.

Validation updates should usually be added under `validation/`.

---

## Style Guidelines

Use clear, direct Markdown.

Preferred style:

- concise headings;
- short paragraphs;
- tables for structured definitions;
- code blocks for equations, JSON, YAML, or command examples;
- plain operational language;
- careful distinction between proposed, assumed, and validated claims.

Avoid:

- excessive abstraction;
- unsupported certainty;
- promotional language;
- unnecessary jargon;
- claims that the framework is final or proven.

---

## Terminology Consistency

Before introducing a new term, check `docs/glossary.md`.

Use existing terms where possible, including:

- coherent flow;
- entropy load;
- flow quality;
- contradiction density;
- uncertainty variance;
- memory fragmentation;
- recursion instability;
- context decay;
- alignment;
- misalignment;
- governance intervention.

If a new term is necessary, add it to the glossary with a concise definition.

---

## Information Handling

This repository should use sanitized, non-sensitive examples.

Do not include:

- passwords;
- usernames tied to real incidents unless approved;
- internal IP addresses;
- client-sensitive server names;
- restricted system diagrams;
- non-public operational data;
- personal information;
- unapproved screenshots;
- proprietary third-party material.

If uncertain, do not include the information. Replace it with a sanitized placeholder.

Example:

```text
Original: PROD-SERVER-123 processed client transaction ABC-123.
Sanitized: A production application server processed a representative transaction.
```

---

## Review Expectations

Reviewers should evaluate contributions against the following questions:

1. Does the change improve clarity, usefulness, or testability?
2. Does it preserve the early-stage status of the model?
3. Does it avoid false precision?
4. Does it distinguish evidence from assumptions?
5. Does it help validate or challenge the model?
6. Does it reduce ambiguity or introduce new ambiguity?
7. Does it create operational value without unnecessary complexity?

---

## Decision Outcomes

A proposed change may be:

| Outcome | Meaning |
|---|---|
| Accepted | Change is incorporated |
| Accepted with Revision | Change is useful but requires edits |
| Deferred | Change may be useful later but is not needed now |
| Rejected | Change does not fit current model direction |
| Moved to Open Questions | Change raises a useful unresolved issue |
| Moved to Assumptions | Change depends on an unvalidated assumption |

---

## Current Project Status

EFGM should currently be treated as:

```text
Status: Early-stage governance framework and prototype scoring concept.
Purpose: Investigation, review, testing, and refinement.
```

Contributions should help determine whether EFGM should become:

- a conceptual model;
- a checklist;
- a scorecard;
- a lightweight assessment method;
- a prototype scoring engine;
- a broader governance framework;
- or a retired experiment.

---

## Summary

Contributions should make EFGM clearer, safer, more testable, and more useful.

The preferred contribution pattern is:

```text
Clarify the model → Test the model → Challenge assumptions → Improve evidence → Refine governance action
```

The most valuable contributions are those that help answer the central question:

> Does EFGM help identify when a system, workflow, decision, or reasoning chain is no longer coherent enough to proceed without verification, correction, or escalation?
