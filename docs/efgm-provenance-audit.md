# EFGM Provenance Audit

## Purpose

This audit separates four layers that must not be conflated:

1. the original EFGM conceptual formulation;
2. later conceptual restatements and the v1 coherent-flow implementation lineage;
3. the canonical EFGM v2 decision-integrity model;
4. experimental extensions such as Agent Governance and later artificial-homeostasis work.

The original formulation is preserved separately in [`original-efgm-formula.md`](original-efgm-formula.md):

```text
T × E = Et ~ F ± e = A|M
```

with the historical meanings Time, Energy/Capability, Energy Transfer, Flow, Entropy, and Alignment/Misalignment.

## Audit findings

### 1. `docs/efgm-white-paper.md` — correction required

The white paper currently says the original EFGM concept used:

```text
T × E → Et → F ± e → A|M
```

That arrow form is a later conceptual restatement. It must not be described as the original notation. The white paper should cite the exact original expression and then identify the arrow form and v1 equations as later interpretive/operational descendants.

### 2. `docs/legacy/model-definition-v1.md` — correction required

The file labels the arrow expression as the "Historical conceptual model." This is too broad and can be read as the original formulation. It should instead be labelled as a later v1-lineage conceptual restatement and link to the preserved original formula.

### 3. `docs/README_v0.2_insert.md` — correction required

The sentence "The original v0.1 equation" currently refers to:

```text
F = (T × E × Fq) / (1 + e)
```

That equation is an early operational prototype, not the original EFGM conceptual formula. The document should say "early v1 operational prototype equation" and explicitly distinguish it from the original conceptual expression.

### 4. `docs/EFGM_v0.2_recommendations.md` — clarification required

The phrase "transition from the original coherent-flow model" conflates the original concept with the later v1 operational model. It should say the document records the transition from the early v1 coherent-flow implementation lineage to v2, while the original conceptual provenance is preserved separately.

### 5. `docs/glossary.md` — clarification required

The glossary already separates v1, v2, package identity, and Agent Governance correctly, but it omits a separate "Original EFGM formulation" layer. Add that layer so historical symbols such as `T`, `E`, `Et`, `F`, `e`, and `A|M` are not silently interpreted through later v1 or v2 semantics.

### 6. `README.md` — clarification recommended

The README correctly identifies EFGM v2 as the canonical operational model and Agent Governance v0.3 as experimental. Preserve that authority. Add only a concise historical-origin section pointing to the original formula and explicitly stating that the original concept is provenance, not the current scoring equation.

### 7. `docs/executive-level-statement.md` — clarification recommended

The statement correctly presents v2 as canonical and the coherent-flow equation as historical v1. Add one sentence noting that an earlier original conceptual expression predates the v1 operational equation, with a link to the provenance record.

### 8. `docs/model-definition.md` — no semantic correction required

This file already correctly states that v2 is canonical and v1 is historical. A provenance link may be added for navigation, but its current model authority is sound.

### 9. Agent Governance v0.3 — no rollback required

Agent Governance is consistently described as an experimental extension rather than the original EFGM formula or the canonical v2 baseline. Its current equations (`GI`, `AE`, `CUE`) and temporal-governance constructs should remain untouched by this provenance audit.

### 10. Experimental results — no retroactive insertion into the original formula

Later findings about governance integrity, temporal recovery, containment, regulation, uncertainty, or artificial homeostasis may motivate new hypotheses, but they must be documented as evidence-derived extensions. They must not be rewritten into the historical original expression as though they were present from inception.

## Provenance rule

Use the following language consistently:

- **Original EFGM formulation** — the historical conceptual expression `T × E = Et ~ F ± e = A|M`.
- **Later conceptual restatement** — arrow-form narrative interpretations such as `T × E → Et → F ± e → A|M`.
- **EFGM v1** — early coherent-flow operational equations, including raw-product and later geometric-mean implementations.
- **EFGM v2** — current canonical decision-integrity research model.
- **Agent Governance / artificial-homeostasis work** — experimental extensions and separate research programs informed by EFGM, not parts of the original formula unless independently established and explicitly versioned.

## Scope

This audit is documentation/provenance work only. It does not alter executable scoring, versioned parameters, frozen experiment results, Agent Governance semantics, or the canonical EFGM v2 baseline.
