# Experimental Scoring Configurations

The packaged canonical v2 baseline is:

```text
src/efgm/config/efgm-v2.0-baseline.json
```

Place candidate experiment configurations under this directory with unique immutable IDs, for example:

```text
configs/efgm-v2.1-candidate-0001.json
```

Do not overwrite an old candidate file to represent a different experiment. A human-readable `config_id` is metadata, not sufficient identity: every experiment must also record the canonical SHA-256 of the configuration content returned in the v2 result.

Candidate configs are rejected when they contain invalid schema versions, missing/unexpected metric names, negative/non-finite weights, weight sections that do not sum to 1.0, non-positive epsilon values, out-of-range thresholds, or logically disordered DQ classification bands.

Record the candidate configuration ID, SHA-256, path, and repository code SHA in the experiment manifest. Use `efgm-score --config` or the Python scoring API to compare the candidate against the frozen baseline.

A candidate configuration is not canonical merely because it performs well on development data. It must survive validation, independent-baseline comparison, and externally sealed holdout evaluation before human promotion review.
