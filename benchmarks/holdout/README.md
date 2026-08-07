# Sealed Holdout Benchmark Partition

This partition is reserved for final evaluation of a **frozen** candidate.

## Rules

- Do not inspect holdout case contents while designing or tuning that candidate.
- Do not use holdout results to iteratively tune the same candidate and then report the retest as independent validation.
- Once exposed for a candidate-selection cycle, treat those cases as spent for that purpose and create/obtain a new sealed holdout for future major tuning.
- Record who/what accessed the holdout and when.
- Preserve labels established independently of EFGM.

The presence of this README in Git does not itself make future cases sealed; operational access controls or external custody are preferred for truly blind validation.
