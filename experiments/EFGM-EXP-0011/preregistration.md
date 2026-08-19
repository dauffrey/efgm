# EFGM-EXP-0011 — Coupled State Early Coherence Detection

Status: PREREGISTERED — execution not yet interpreted

## Historical context

EFGM-EXP-0010 tested whether trajectory-history derivatives (flow slope, entropy slope, recovery-after-peak) added discriminative power beyond contemporaneous flow. The primary hypothesis FALSIFIED at step 12 (only 0.0264 AUC improvement over F-only, below preregistered 0.05 threshold).

However, an incidental preregistered comparator in EXP-0010—a simple current-state joint of `(E, Et, F, e)` using equal-weight geometric composition—outperformed the trajectory-dynamics score at all three checkpoints:
- Step 6: joint 0.9533 vs trajectory 0.9056
- Step 12: joint 0.9662 vs trajectory 0.9548  
- Step 18: joint 0.9835 vs trajectory 0.9651

This observation suggests that **state coupling itself**, not temporal derivatives, may carry genuine early coherence information.

## Research question

Does a coherent coupling of normalized reserve, transfer, flow, and entropy complement provide discriminative early-detection capability for terminal Alignment (A) versus Misalignment (M), and is this capability robust across multiple aggregation schemes?

## Why this follows EXP-0010

EXP-0010 falsified trajectory-history derivatives. EXP-0011 does not retry or modify EXP-0010. It asks a new, narrower question: **can the frozen four-variable joint predefined in EXP-0010 as a comparator establish itself as a standalone candidate through preregistered robustness criteria?**

This avoids post-hoc hypothesis generation by using only the comparator that was explicitly included in EXP-0010's design.

## Design

- **Dataset:** Reuse the immutable EXP-0010 synthetic trajectories (240 scenarios, 24 steps, dataset SHA `752a333cc2a89eb554ea81761d4a64568f793d8ee940cbab5e03f9afe53fdbe6`)
- **Frozen measurements:** Same as EXP-0010 checkpoint observations: `T`, `E`, `Et`, `F`, `e`
- **Prediction task:** Binary classification of terminal outcome (A vs M) at checkpoints 6, 12, 18
- **No parameter fitting:** All composite coefficients are preregistered in source. No tuning on the evaluation dataset.

## Three preregistered aggregation schemes

All schemes are frozen **before first scientific execution**. No coefficients may be modified to rescue results.

### Scheme 1: Equal-weight geometric mean

```
C_geometric = (E × Et × F × (1-e))^(1/4)
```

Rationale: Multiplicative coupling; proportional weighting; captures balance without directional bias.

### Scheme 2: Weighted linear

```
C_linear = 0.30×E + 0.35×Et + 0.20×F + 0.15×(1-e)
```

Rationale: Priority to transfer efficiency (Et) and reserve (E); secondary weight to entropy complement; allows asymmetric emphasis.

Coefficients normalize to 1.0 and are frozen in source.

### Scheme 3: Harmonic mean

```
C_harmonic = 4 / (1/E + 1/Et + 1/F + 1/(1-e))
```

Rationale: Sensitive to bottlenecks; any weak variable suppresses the composite; captures tight coupling requirement.

## Robustness sub-questions

At each checkpoint (6, 12, 18), compute ROC-AUC for:

1. **Single variables:** `E`, `Et`, `F`, `1-e`
2. **Three schemes:** geometric, linear, harmonic
3. **Best single variable:** max AUC among E, Et, F, 1-e

## Primary hypotheses (step 12 only)

At the 50% checkpoint (step 12):

- **H1:** All three schemes achieve ROC-AUC ≥ 0.92
- **H2:** Each scheme beats the best single-variable baseline by ≥ 0.02
- **H3:** The three schemes produce consistent rankings (no anomalous reversals across steps 6, 12, 18)

All three must pass. Failure of any single criterion FALSIFIES the primary hypothesis.

## Coupling-value sub-question

**Does the interaction itself add value, or is simple additive combination sufficient?**

Preregistered additive baseline: `C_additive = 0.25×E + 0.25×Et + 0.25×F + 0.25×(1-e)`

- If any scheme (geometric, linear, harmonic) beats `C_additive` by ≥ 0.01 AUC at step 12, answer: **YES, coupling adds value**
- Otherwise: **NO, simple addition sufficient**

This is a **secondary diagnostic**; failure does not FALSIFY the primary hypothesis but informs interpretation.

## Early-detection sub-question

**Can step-6 (25%) performance match or exceed step-18 (75%) trajectory-dynamics performance?**

- EXP-0010 trajectory-dynamics at step 18: 0.9651
- Success: At least one scheme achieves ≥ 0.9651 at step 6

This is a **preregistered secondary diagnostic**. Success supports the claim of genuine early coherence information.

## Validity criteria

- Exactly 240 trajectories (same scenario set as EXP-0010)
- Exactly 3 checkpoints (6, 12, 18)
- Dataset SHA matches EXP-0010: `752a333cc2a89eb554ea81761d4a64568f793d8ee940cbab5e03f9afe53fdbe6`
- Minority terminal class ≥ 15% (same as EXP-0010: 15%)
- No missing/non-finite AUC values
- Deterministic rerun produces identical results
- No post-execution coefficient, scheme, checkpoint, or criterion changes

## Classification

- **PRIMARY CLASSIFICATION:**
  - `SURVIVED` if validity passes AND all of H1, H2, H3 pass at step 12
  - `FALSIFIED` otherwise

- **COUPLING-VALUE DIAGNOSIS:**
  - `COUPLING_ADDS_VALUE` if any scheme beats additive by ≥ 0.01
  - `SIMPLE_ADDITION_SUFFICIENT` otherwise

- **EARLY-DETECTION DIAGNOSIS:**
  - `EARLY_DETECTION_ACHIEVED` if any scheme ≥ 0.9651 at step 6
  - `NOT_ACHIEVED` otherwise

## Scope exclusions

This experiment must not modify:

- Original EFGM notation
- EFGM v1/v2 equations, weights, thresholds, or provenance semantics
- Agent Governance v0.3
- AE/CUE definitions
- EXP-0008, EXP-0009, EXP-0010
- Any frozen baseline
- Autonomous-agent authorization or containment state

## Scientific custody

The first valid execution is authoritative. Any implementation defect discovered after execution may be corrected only if:

1. The original execution identity/result remains recorded
2. The correction demonstrably does not alter composite schemes, coefficients, checkpoints, or success criteria
3. Human review confirms the correction is necessary and does not rescue a FALSIFIED result

Negative results must be preserved. No post-hoc retuning to convert FALSIFIED to SURVIVED.

## Why this design is clean

- Reuses the same dataset to isolate the comparison (coupled state vs trajectory-history)
- Three independent aggregation schemes allow cross-validation of the hypothesis without overfitting
- Preregistered thresholds are explicit and auditable
- Sub-questions are diagnostic, not rescue criteria
- Results that FALSIFY the primary hypothesis are still scientifically informative (e.g., "all schemes robust but none beat single variables" falsifies coupling but supports variable importance)
