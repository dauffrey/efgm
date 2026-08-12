# EFGM-EXP-0004 — Agent Governance critical-dimension diagnostics

## Decision

**Do not promote the current candidate prerequisite set.**

This development/validation cycle confirms that explicit non-compensatory prerequisites can expose sparse catastrophic failures that the aggregate Agent Governance classifier misses, but the current configured path set is incomplete and does not outperform the simpler aggregation-independent invariant checklist on validation. No sealed holdout was accessed.

## Execution lineage

EXP-0004 has two distinct execution records. The second is a **corrective reproducibility execution**, not a replacement for the first scientific run.

| Role | Head SHA | EFGM Check | Runner | Python | Purpose |
|---|---|---|---|---|---|
| Original scientific execution | `8c2df53760dc8a39ac2d802127a477d107f14102` | `#93` / `31430795539` | `0.2.0` | `3.12.13` | Produced the original development/validation scientific findings. |
| Corrective reproducibility execution | `2b41336e4411a3389d1ef22ba9f90687025a2b7a` | `#105` / `31497130999` | `0.2.1` | `3.12.13` | Added the promised per-case input identities and completed the preregistered ablation set. |

The original runner had two reproducibility defects discovered during review:

1. it did not emit each scorer result's `input_sha256` into the EXP-0004 output;
2. it did not execute the preregistered empty-set candidate-prerequisite ablation.

The corrective execution changed **no dataset cases, labels, candidate configuration, thresholds, perturbation parameters, seed, or holdout boundary**. The headline scientific metrics and promotion decision were unchanged. The historical #93 result is therefore preserved as the original scientific execution, while #105 supplies the missing reproducibility evidence rather than retroactively attributing it to #93.

## Frozen research identity

- Parent merged `main`: `fd70317e4bad193c00763a398f41db6e75700b55`
- Frozen EFGM v2 config: `efgm-v2.0-baseline`
- Frozen EFGM v2 config SHA-256: `0f55f6eabe97d0f365d1e45ba8f9d0fef67e9721a93e6eba8b0a364b612bafd0`
- Agent Governance candidate config: `efgm-v0.3-agent-governance-candidate-r2`
- Candidate config SHA-256: `af0b5540f28d4d65ae95929a855a168f9e7c286439d33d33e14ef167d808366c`
- Dataset version: `sparse-governance-failures-v0.3`
- Dataset SHA-256: `71b8534a2cc69e62c4375a100d85b40de1051ffbdf61bd9f035ce19728fdeb38`
- Development / validation / holdout cases: `12 / 15 / 0`
- Perturbation: `±0.10`, 200 trials per case, seed `20260810`

## Corrective assessment identity

The corrective #105 execution emitted scorer-produced `input_sha256` values for every generated assessment.

### Development

| Case | Input SHA-256 |
|---|---|
| `exp0004-dev-authority-borderline-benign` | `7c9aad80662ec0c4a185979bb2c93552688655850ed94afe4355ed2ba30d4c66` |
| `exp0004-dev-authority-collapse` | `fc6379f7815db765c01704c25bfc0da5a6084d4dba578fd92abb64f8516ac8d6` |
| `exp0004-dev-containment-collapse` | `4d6d157b2b5fae365de68cad5f491c5ae8a60fa6952dac2ee0cfd8468958c998` |
| `exp0004-dev-credential-scope-collapse` | `49aca7c9371bcf6951152cb74f5de51ddf420734b6fa463f225f0ecde2c1c686` |
| `exp0004-dev-low-action-trace-benign` | `01b41b25d8dadcc3a22d0deb3bca3d6f567ee0061f478ab66b69cc05b81db25b` |
| `exp0004-dev-low-message-trace-benign` | `c3765e593e5ddc9ca6e133b6676a3ac886cd31121f8e8f2c7b71d04421ab6c32` |
| `exp0004-dev-low-readback-trace-benign` | `42c7c8d1eebd167a68dbf68895ca120d5e182c65d2714a7cf94c4c99af8b6ee0` |
| `exp0004-dev-privilege-boundary-collapse` | `16810255bd0f7fd942744f450f6bee2dfab3e55458071adb1d777c7584c988e7` |
| `exp0004-dev-revocation-borderline-benign` | `bb5fd32d95c142561b7c101e879c9f005fc3bd542a42110c30f9a29a8c8593f5` |
| `exp0004-dev-revocation-collapse` | `9fa3acd5791dbdaef6bff0511896dd74795ed9781c9f20ec0ea3b347114bc286` |
| `exp0004-dev-trust-borderline-benign` | `e60c83b27815a260b68ae86d95b60bea69d2e0afc000f8dd725a4fe2bc0e0943` |
| `exp0004-dev-trust-boundary-collapse` | `9cf7e7ab553b77a20704a659e244e4a00bddc2b47befaf4eb09c0d92a6359dce` |

### Validation

| Case | Input SHA-256 |
|---|---|
| `exp0004-val-authority-near-threshold` | `5a0c87bb6564c0826c8db115125445090023c61fc92a0c29c0183de67561dee9` |
| `exp0004-val-capability-scope-uncovered` | `262d5f9b01b02acf5c9a6717a9c741664662b2f1e1f498e9dd86eac6746bc979` |
| `exp0004-val-containment-borderline-benign` | `8c01a17d3e49ae7f352c3043a0332b1de4b53365a8fcf4d5d15002310ac41bdd` |
| `exp0004-val-containment-near-threshold` | `3552cf5cdd45bb25b1da1576b2ab1df48325f32dc32f90c7f20ff4b6c218775d` |
| `exp0004-val-credential-borderline-benign` | `d77918624715fb54b5b8c197c94ac5390c8dd9bc6fa19f71f2c4ccce41b3e3fd` |
| `exp0004-val-credential-near-threshold` | `c8794a002d798aebcdf906f6cdf206cb3b49413bfedee8f6638afdd7c2cfd4c8` |
| `exp0004-val-low-cross-agent-trace-benign` | `fccdb059b89c7d9dfafeec90b05abba28cd05a98fdaaed1c2cc4c033428f8ede` |
| `exp0004-val-low-peer-discovery-benign` | `ccdddf1e6ba9252dfc439d8432dd6b5931e41a8dc931cc6f6ace1db6ab88b772` |
| `exp0004-val-low-write-inventory-benign` | `f8db3fde253e52e9e8ecf39a562f996eaaa785012430ff49f11b785aeb9f1b23` |
| `exp0004-val-privilege-borderline-benign` | `b2a9a695c602e2834b91658afe7ff07cc172be05a44db2b57292caf92c588be0` |
| `exp0004-val-privilege-near-threshold` | `997228f24e95461bcabd588882fe8d855e2b3e8add4be0fbe7ca76abbd82397d` |
| `exp0004-val-prohibited-goal-uncovered` | `b69c766bcc6b13f6dc9528e9b3a6f51715c9a1167e0c5139cdc01f98c93106da` |
| `exp0004-val-revocation-near-threshold` | `2af6901f3f69ee05f476ceeeacba1c62914dfe32d210716391d0576416f7465d` |
| `exp0004-val-state-cleanup-uncovered` | `77b75491bc41349ec6f69c8746a48c95bc1cc2b13217a5b58dd20e4026fe061e` |
| `exp0004-val-trust-near-threshold` | `cb7a22eb216580835dc0a544cd25d90b4cd7d74b7b9de3559d247b2aa6bcc244` |

## Pre-result design hardening

Before reading the original EXP-0004 output, the experiment was strengthened in two ways:

1. The invariant checklist threshold was frozen separately at `0.40` rather than inherited from the candidate configuration. This keeps it independent of the candidate threshold, although it remains an internally authored comparator rather than an externally independent label source.
2. Three catastrophic validation challenges were added outside the configured candidate-prerequisite path set:
   - `alignment.prohibited_goal_avoidance`
   - `boundary_integrity.capability_scope_adherence`
   - `control_recoverability.state_cleanup_completeness`

These design changes predate the original #93 result. The later corrective #105 execution did not modify them.

## Dataset design

### Development — 12 cases

- 6 complete sparse failures (`0.00`) on configured candidate prerequisite paths;
- 3 low non-prerequisite benign controls (`0.15`);
- 3 configured prerequisite-path borderline controls (`0.45`).

### Validation — 15 cases

- 6 configured candidate prerequisite paths at `0.35`;
- 3 low non-prerequisite benign controls at `0.10`;
- 3 configured prerequisite-path borderline controls at `0.45`;
- 3 catastrophic failures at `0.00` on preregistered paths outside the configured prerequisite set.

All cases are synthetic, internally authored, and tuning-visible. They are not holdout evidence.

## Executed results

The corrective execution reproduced the original headline results.

### Development

| Diagnostic | Detection | False alarms |
|---|---:|---:|
| Aggregate-only classifier | 0.00% | — |
| Configured candidate prerequisites | 100.00% | 0.00% |
| Governance observation floor | 100.00% | 50.00% |
| Governance low percentile | 0.00% | 0.00% |
| Aggregation-independent invariant checklist | 100.00% | 0.00% |

The aggregate-only false-reassurance rate was **100.00%** on development catastrophic cases.

### Validation

| Diagnostic | Detection | False alarms |
|---|---:|---:|
| Aggregate-only classifier | 0.00% | — |
| Configured candidate prerequisites | **66.67%** | **0.00%** |
| Aggregation-independent invariant checklist | **66.67%** | **0.00%** |

The aggregate-only false-reassurance rate remained **100.00%** on validation catastrophic cases. The three intentionally uncovered catastrophic paths were not detected by the configured prerequisite set, so validation detection was **6/9 = 66.67%**.

```text
incremental balanced accuracy vs checklist = +0.0000
```

The current candidate therefore did not provide incremental validation value over the simpler aggregation-independent comparator.

## Threshold sensitivity and complete candidate ablation

Threshold sensitivity on the combined development+validation cases remains:

- threshold `0.40`: detection `80.00%`, false alarms `0.00%`;
- threshold `0.30`: detection `40.00%`;
- threshold `0.50`: false alarms `50.00%`.

The corrective runner completed every preregistered candidate-prerequisite path-set comparison:

| Ablation | Detected catastrophic cases | Detection rate |
|---|---:|---:|
| Full candidate set | 12 / 15 | 80.00% |
| Empty candidate set | 0 / 15 | 0.00% |
| Remove `alignment.authority_precedence` | 10 / 15 | 66.67% |
| Remove `boundary_integrity.trust_boundary_adherence` | 10 / 15 | 66.67% |
| Remove `boundary_integrity.privilege_boundary_adherence` | 10 / 15 | 66.67% |
| Remove `boundary_integrity.credential_scope_adherence` | 10 / 15 | 66.67% |
| Remove `control_recoverability.revocation_effectiveness` | 10 / 15 | 66.67% |
| Remove `control_recoverability.containment_effectiveness` | 10 / 15 | 66.67% |

The empty-set result establishes the intended no-prerequisite comparison explicitly instead of inferring it from leave-one-out behavior.

## Perturbation robustness

With `±0.10` perturbation and 200 trials per case:

- mean correct classification probability: **77.65%**;
- minimum case probability: **0.00%**.

The zero minimum is structural: preregistered catastrophic validation paths outside the candidate set remain undetectable by that candidate prerequisite mechanism.

## Promotion gate

```text
promotion_gate_passed = False
```

The candidate prerequisite concept demonstrates value against aggregate-only false reassurance on covered paths, but the **current path set is not eligible for promotion** because:

1. semantic coverage is incomplete on preregistered validation challenges;
2. the simpler invariant checklist provides the same covered-path validation decisions;
3. there is no positive incremental balanced accuracy;
4. perturbation robustness contains structurally undetectable cases;
5. the evidence is internally authored and no sealed holdout has been used.

## Scientific impact of the corrective execution

The corrective execution repaired experiment provenance without tuning the experiment to its result:

- no gold-standard or semantic labels were changed;
- no candidate prerequisite paths were added after observing validation failures;
- no threshold was changed;
- no dataset case was changed;
- no holdout case was accessed;
- no original metric was rewritten;
- the original failed promotion decision was preserved.

The result therefore remains negative evidence against promotion of candidate-r2 rather than a post-hoc attempt to improve it.

## What we do not do next

We do **not** append the three failed validation paths to the prerequisite list and rerun the same evaluation as though that were confirmation. That would tune the candidate directly to observed validation failures and erase the value of the counterexample.

A future candidate may propose a semantically justified broader control invariant, but it must be preregistered and evaluated against fresh cases and simpler alternatives.

## Implications for the research program

EXP-0004 supports three conclusions:

1. **Aggregate-only Agent Governance remains vulnerable to sparse critical failures.** Every catastrophic case in this cycle was reassuring under aggregate-only classification.
2. **Non-compensatory semantics matter, but a hand-selected prerequisite list is not enough.** The current candidate succeeds exactly where it has explicit coverage and fails outside it.
3. **Simpler comparators remain serious competitors.** The candidate prerequisite layer did not outperform the simpler aggregation-independent checklist on validation.

## Limitations

- Cases and labels are internally authored and EFGM-aware.
- The invariant checklist is independent of EFGM aggregation but not independently labeled by an external scorer.
- The validation split is tuning-visible after the original run and must not be reused as unseen evidence for a modified prerequisite path set.
- No sealed holdout was accessed.
- The original #93 execution record was incomplete; the missing assessment identities and empty-set ablation are explicitly supplied by corrective run #105 rather than attributed retroactively to #93.
- Passing CI establishes implementation/reproducibility behavior, not scientific validity.
- This result rejects promotion of the **current candidate prerequisite set**; it does not reject every possible non-compensatory governance design.
