# Model Definition

This path is retained to avoid breaking existing links.

## Current model

The canonical EFGM v2 decision-integrity definition is:

- [`model-specification-v2.md`](model-specification-v2.md)
- [`scoring-rubric-v2.md`](scoring-rubric-v2.md)
- executable implementation: `src/efgm/scoring_v2.py`
- versioned baseline parameters: `src/efgm/config/efgm-v2.0-baseline.json`

Do not use the former `F = (T × E × Fq) / (1 + e)` text at this path as the current EFGM model. That equation belongs to the historical v1/coherent-flow line.

Historical material:

- [`legacy/model-definition-v1.md`](legacy/model-definition-v1.md) — concise legacy summary;
- [`legacy/v1/model-definition.md`](legacy/v1/model-definition.md) — verbatim pre-v2 model document preserved from the PR base commit.
