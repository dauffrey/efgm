# Sealed Holdout Benchmark Partition

This repository directory contains **metadata only**. Real holdout case contents and preferred labels must not be committed here if an autonomous researcher can read the repository.

## Required custody model

- Store holdout cases and labels outside the tuning-visible repository or behind access controls unavailable to the autonomous research loop.
- Commit only a manifest containing non-revealing metadata such as dataset ID, case count, label authority, creation date, custodian, and a cryptographic dataset hash.
- Open the holdout only after a candidate is frozen and its experiment manifest/success criteria are recorded.
- Record who/what accessed the holdout, when, and for which frozen candidate.
- Do not use holdout results to tune the same candidate and then report a retest as independent validation.
- Once exposed for a candidate-selection cycle, treat those cases as spent for that purpose and obtain a new sealed holdout for a future major tuning cycle.
- Preserve labels established independently of EFGM.

## Repository contents

Allowed here:

```text
README.md
.gitignore
holdout-manifest.template.json
<non-revealing manifest files only>
```

Not allowed here:

```text
case text
prompts/responses
preferred labels
scoring keys
hidden test fixtures
anything from which the answer key can be reconstructed
```

A Git directory is not a seal when the research robot can read Git. External custody or equivalent access control is mandatory for claims of blind holdout performance.
