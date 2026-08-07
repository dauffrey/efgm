# Experimental Scoring Configurations

The packaged canonical v2 baseline is:

```text
src/efgm/config/efgm-v2.0-baseline.json
```

Place candidate experiment configurations under this directory with unique immutable IDs, for example:

```text
configs/efgm-v2.1-candidate-0001.json
```

Do not overwrite an old candidate file to represent a different experiment. Record the candidate configuration ID/path in the experiment manifest and use `efgm-score --config` or the Python scoring API to compare it against the frozen baseline.

A candidate configuration is not canonical merely because it performs well on development data.
