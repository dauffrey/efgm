# EFGM-EXP-0009 — Direct Deterministic Test of the Original EFGM Formulation

## Preserved original

```text
T × E = Et ~ F ± e = A|M
```

This experiment does **not** rewrite that expression as a literal algebraic equation. It asks a narrower falsifiable question: when the historical variables are measured on controlled synthetic trajectories, does their joint relationship discriminate terminal alignment/stability (`A`) from misalignment/degradation (`M`) better than simpler individual-variable explanations?

## Why this experiment exists

The repository now cleanly distinguishes the original EFGM formulation from v1, canonical v2, and Agent Governance v0.3. EXP-0009 therefore tests the original conceptual variables directly without changing any later model.

The experiment is deterministic, synthetic, non-autonomous, network-free, and safe to execute in ordinary CI. It is separate from paused EXP-0008 Phase-3 autonomy.

## Synthetic environment

Each trajectory lasts at most eight steps and has three frozen factors:

- capability `E`;
- transfer-policy intensity controlling how much capability is applied;
- an externally generated entropy/disturbance band.

A frozen SHA-256-derived perturbation produces deterministic within-band disturbance variation. The state contains only synthetic progress and synthetic reserve.

The terminal label is defined independently of any EFGM score:

```text
A = progress >= 0.55 AND reserve >= 0.10
M = otherwise
```

## Experiment-only operational definitions

For this experiment only:

- `T` = fraction of the planned horizon completed;
- `E` = frozen capability setting;
- `Et` = normalized cumulative capability actually transferred into action;
- `F` = normalized realized productive progress;
- `e` = mean external disturbance burden;
- `A|M` = terminal outcome defined above.

To test the variables jointly without pretending the original notation was algebra, the experiment freezes this monotonic proxy:

```text
C* = (T × E × Et × F)^(1/4) / (1 + e)
```

`C*` is **not** the original EFGM formula and is **not** a candidate canonical model. It is only the preregistered joint-variable comparator for EXP-0009.

## Comparators

The joint proxy is compared with:

```text
T only
E only
Et only
F only
1 - e only
```

ROC-AUC is used because it tests ranking without tuning an outcome threshold after observing the data.

## Frozen decision criteria

The dataset is valid only if the minority terminal class is at least 15% of trajectories.

The strict hypothesis **SURVIVES** only if all three tests pass:

1. joint-proxy ROC-AUC >= 0.75;
2. joint-proxy AUC exceeds the better of `E`-only and entropy-only by at least 0.05;
3. joint-proxy AUC exceeds `F`-only by at least 0.02.

If the dataset is valid and any criterion fails, the hypothesis is **FALSIFIED**. No coefficients, thresholds, trajectory factors, labels, or disturbance seed may be changed after the first execution to rescue the result.

## Interpretation boundaries

A survival result would show only that the original-variable relationship has incremental discriminative value in this synthetic system. A falsification would show that this operationalization does not add the preregistered value, including the possibility that one simpler variable such as realized flow explains the outcome better.

Neither result proves or disproves the original EFGM as a universal theory, and neither changes EFGM v2 or Agent Governance v0.3.
