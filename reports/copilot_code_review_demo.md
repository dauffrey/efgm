# EFGM Coherent Flow Report

## Task

`copilot-code-review-demo`

## Score Summary

| Metric | Value |
|---|---:|
| T | 0.8000 |
| E | 0.9000 |
| Fq | 0.7175 |
| e | 0.2450 |
| F | 0.4149 |

## Classification

**Degraded but usable**

## Entropy Drivers

- Uncertainty variance

## Recommended Action

Verify assumptions and reduce entropy before relying on the result.

## Formula

```text
F = (T × E × Fq) / (1 + e)
```

## Interpretation

The coherent flow score represents the degree to which the evaluated system, workflow, or reasoning chain is maintaining useful alignment while entropy accumulates.

A lower score indicates that verification, context repair, or governance intervention may be required before relying on the result.
