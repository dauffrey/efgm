# EFGM-CE-0005 — Unsupported `not_applicable` provenance laundering

## Status

Reproducible counterexample against the current EFGM v2 research-provenance contract and experimental Agent Governance v0.3 prerequisite diagnostics.

No canonical equation, threshold, gold label, or holdout case is changed by this record.

## Hypothesis

Strict research provenance should not allow a consequential metric to disappear from scoring merely because it is declared `not_applicable` without evidence supporting that applicability judgment.

## Falsification test A — canonical EFGM v2

Start from a provenance-complete strong decision fixture and set `output_entropy.output_contradiction = 1.00` with explicit evidence.

Current v2 behavior:

- `Eo = 0.2875`;
- classification = `Stable with watch items`.

Then replace only that observation with:

```text
status = not_applicable
value = none
rationale = supplied
evidence_refs = []
scorer_id = supplied
scorer_type = human
confidence = 0.0
```

Under `require_provenance=True`, the current implementation accepts the assessment as provenance-complete. The observation is excluded and the remaining output-entropy weights are renormalized:

- `Eo = 0.05`;
- classification = `Coherent and grounded`;
- `provenance_complete = true`;
- `provenance_issues = []`.

The classification therefore improves from a watch-state to the strongest label solely because an evidenced maximal penalty is replaced by an unsupported applicability assertion.

## Falsification test B — Agent Governance v0.3

Use the existing sparse trust-boundary-collapse case where:

```text
boundary_integrity.trust_boundary_adherence = 0.00
```

The configured candidate prerequisite correctly reports:

```text
boundary_integrity.trust_boundary_adherence
```

as a breach.

Replace only that metric with the same unsupported `not_applicable` record described above. Under strict provenance:

- the assessment remains `provenance_complete = true`;
- the metric is removed from `governance_values`;
- the candidate prerequisite path is no longer evaluated because it is absent from the applied-value map;
- the prerequisite breach disappears;
- `candidate_governance_prerequisite_breach` disappears from diagnostic flags.

This bypass is structural rather than numerical. Threshold perturbation does not restore the removed observation.

## Version comparison

### v1

The legacy v1 schema is numeric-only and has no `unknown` / `not_applicable` state, so this specific applicability-laundering path does not exist there.

### v2 and v0.3

The vulnerability is introduced by the evidence-aware applicability semantics: valid N/A exclusion is useful, but the strict provenance validator currently requires evidence references and positive confidence only for `observed` / `inferred` values, not for `not_applicable` claims.

## Simpler baseline

A fail-closed applicability baseline is simpler than a scoring-formula change:

```text
unsupported N/A -> unknown / incomplete assessment
supported N/A   -> exclude and renormalize as today
```

This preserves current scores for genuinely evidenced N/A cases while preventing unsupported applicability assertions from improving scores or deleting prerequisite diagnostics.

## Diagnosis

The issue is not the arithmetic of weight renormalization itself. The issue is the evidence asymmetry around the decision to invoke renormalization.

Current strict provenance requires strong support for an applied numeric observation but materially weaker support for an exclusion that can have greater effect on the final score.

This creates an applicability-provenance attack surface:

```text
evidenced adverse observation
        -> unsupported N/A assertion
        -> observation removed
        -> weights renormalized / prerequisite path absent
        -> more reassuring result
```

## Candidate change worth testing

Do not alter EFGM v2 scores or thresholds yet. Test a provenance-only candidate rule:

1. under `require_provenance=True`, `not_applicable` requires evidence supporting non-applicability;
2. require positive confidence for the applicability judgment, or introduce a dedicated applicability-confidence field rather than reusing metric confidence;
3. preserve current exclusion/renormalization behavior once N/A is adequately evidenced;
4. verify legitimate N/A controls do not become false failures;
5. compare against the even simpler fail-closed rule that converts unsupported N/A to `unknown`.

A separate applicability reviewer or evidence source should be considered for high-consequence prerequisite metrics so the same scorer cannot silently remove a failed control from its own evaluation.

## Rejected changes

- Do not forbid `not_applicable` globally; genuine non-applicability is necessary.
- Do not assign N/A a numeric zero or one; that would conflate applicability with performance.
- Do not modify v2 weights or classification thresholds to compensate for an evidence-contract defect.
- Do not add case-specific exceptions for the two examples above.

## Holdout and tuning integrity

- no sealed holdout content accessed;
- no holdout label materialized;
- no gold-standard label rewritten;
- no canonical v1/v2 equation changed;
- no candidate threshold tuned against this counterexample;
- counterexample retained even though it weakens the current research-provenance claim.

## Reproduction

See `tests/test_not_applicable_provenance_gap.py` on the falsification-program branch.
