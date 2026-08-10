# EXP-0006 Independent Authoring Coordination

This directory prepares the external/independent authoring stage for EXP-0006. It does **not** contain independent labels and does not make EXP-0006 an executed experiment.

## Why this boundary matters

EXP-0006 asks whether two model-derived quantities correspond to distinctions that independent reviewers can recognize without being taught the model formulas. Internally generated labels would make that test circular.

Therefore:

- do not ask the EFGM research agent to generate the gold labels;
- do not expose EFGM formulas, scores, AE/CUE names, preferred labels, or prior benchmark outcomes to authors/labelers;
- use at least two independent raters per case where practical;
- preserve each rater's response before adjudication;
- disagreements are data and must not be averaged away before inspection;
- authoring and labeling should occur outside the tuning-visible repository context;
- only blinded packet content and neutral response schema should be supplied to external authors/labelers.

## Files

- `blinded-author-packet.md` — the only substantive instructions intended for independent case authors/labelers.
- `label-schema.json` — neutral response structure for independent labels.

The repository path itself contains the experiment identifier for internal coordination. External participants should receive exported copies of the blinded packet/schema rather than repository access.

## Intake gate

EXP-0006 may move from `authoring_packet_ready_awaiting_independent_labels` to an executable dataset only after:

1. case text is authored independently of EFGM scoring outputs;
2. each case has at least two independent responses where feasible;
3. raw individual labels and rationales are preserved;
4. case/label files are assigned a dataset version and SHA-256;
5. development/validation partitioning is frozen before model comparison;
6. no sealed holdout is exposed to the tuning loop.

If independent authorship cannot be obtained, EXP-0006 remains inconclusive rather than substituting internally generated labels.
