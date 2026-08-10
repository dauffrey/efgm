# EXP-0006 Independent Authoring Coordination

This directory prepares the external/independent authoring stage for EXP-0006. It does **not** contain independent labels and does not make EXP-0006 an executed experiment.

## Why this boundary matters

EXP-0006 asks whether two model-derived quantities correspond to distinctions that independent reviewers can recognize without being taught the model formulas. Internally generated labels would make that test circular.

Therefore:

- do not ask the EFGM research agent to generate the gold labels;
- do not expose EFGM formulas, scores, AE/CUE names, preferred labels, or prior benchmark outcomes to authors/labelers;
- separate **case authoring** from **primary validation labeling**: a case author must not provide the primary validation label for their own case;
- target at least two independent labelers per case;
- prefer human/domain reviewers for the primary semantic-validation analysis;
- if independent external nonhuman raters are also used, preserve and analyze them separately rather than pooling them silently with human/domain judgments;
- preserve each rater's response before adjudication;
- disagreements are data and must not be averaged away before inspection;
- authoring and labeling should occur outside the tuning-visible repository context;
- only blinded packet content and the neutral response schema should be supplied to participants.

## Files

- `blinded-author-packet.md` — substantive instructions intended for independent case authors and reviewers.
- `label-schema.json` — machine-valid JSON Schema for an individual independent review response.

The repository path contains the experiment identifier for internal coordination. External participants should receive exported copies of the blinded packet/schema rather than repository access.

## Role separation

Recommended workflow:

```text
Independent case author
        ↓
case text frozen
        ↓
Independent reviewer A (not the author)
Independent reviewer B (not the author)
        ↓
raw labels frozen
        ↓
inter-rater analysis / adjudication if needed
        ↓
only then compare with model-derived quantities
```

The author may provide factual clarifications about scenario evidence but should not see or influence reviewers' ratings before the raw labels are frozen.

## Intake gate

EXP-0006 may move from `authoring_packet_ready_awaiting_independent_labels` to an executable dataset only after:

1. case text is authored independently of EFGM scoring outputs;
2. each primary validation case has at least two independent labels where feasible;
3. primary validation labelers did not author the case they rate;
4. raw individual labels and rationales are preserved;
5. case/label files are assigned a dataset version and SHA-256;
6. development/validation partitioning is frozen before model comparison;
7. rater type is recorded and human/nonhuman results are not silently pooled;
8. no sealed holdout is exposed to the tuning loop.

If independent authorship/labeling cannot be obtained, EXP-0006 remains inconclusive rather than substituting internally generated labels.
