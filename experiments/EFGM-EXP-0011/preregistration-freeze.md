# EFGM-EXP-0011 Preregistration Freeze

Status: FROZEN FOR IMPLEMENTATION

## Frozen scientific contract

The reviewed preregistration is frozen at:

- preregistration path: `experiments/EFGM-EXP-0011/preregistration.md`
- preregistration commit: `41b95bf16d5f4fca9a8e03f38064137019bd7470`
- preregistration blob SHA: `332ad34180b6ff5f615a4541886f7a1021dc706c`
- source branch: `exp0011-coupled-state-early-coherence`
- base main at branch origin: `37b2ff2d2b577c9f383dd0d7c3083597627150ea`

## Review disposition

The second preregistration review found no remaining scientific blockers before implementation.

The freeze specifically locks:

- research question;
- fresh deterministic holdout requirement;
- seeds `110001..110240`;
- 240 scenarios × 24 steps;
- checkpoints `6, 12, 18`;
- terminal label rule inherited unchanged from EXP-0010;
- measurements `T, E, Et, F, e`;
- geometric, weighted-linear, harmonic, and additive formulas;
- all coefficients;
- single-variable comparators;
- H1, H2, and exact H3 ranking-stability rule;
- coupling-value diagnostic;
- early-detection diagnostic;
- validity criteria;
- SURVIVED/FALSIFIED/INVALID classification rules;
- no-peeking implementation/dataset freeze sequence;
- scope exclusions and scientific-custody rules.

## Change control

Scientific implementation may now be written against this frozen contract.

Any proposed change to a locked scientific element above requires a new explicit superseding preregistration before scientific execution. Implementation fixes that do not alter the frozen contract may proceed, but the first scientific evaluation remains prohibited until the separate implementation/dataset freeze required by the preregistration has been recorded and verified.

This file freezes the preregistration only. It does **not** authorize scientific execution and does **not** constitute the later implementation/dataset freeze.