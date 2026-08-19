"""EFGM-EXP-0010: deterministic trajectory-coherence and early-warning test.

Preserved historical expression:
    T × E = Et ~ F ± e = A|M

This module implements the preregistered synthetic experiment without modifying
canonical EFGM models. All coefficients, checkpoints, trajectory factors and
classification criteria are frozen in source before first scientific execution.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from dataclasses import asdict, dataclass
from typing import Iterable

EXPERIMENT_ID = "EFGM-EXP-0010"
DATASET_VERSION = "trajectory-coherence-synthetic-v0.1"
DATASET_SEED = "EFGM-EXP-0010-FROZEN-SEED-2026-08-18"
HORIZON = 24
CHECKPOINTS = (6, 12, 18)
CAPABILITIES = (0.30, 0.42, 0.54, 0.66, 0.78, 0.90)
TRANSFER_POLICIES = (0.45, 0.62, 0.79, 0.96)
ENTROPY_BANDS = (0.10, 0.25, 0.40, 0.55, 0.70)
REPLICATES = 2
CANONICAL_FLOAT_DECIMALS = 12
EPSILON = 1e-12

# Frozen experiment-only trajectory score weights. These are not EFGM v1/v2.
W_F = 0.22
W_E = 0.18
W_TRANSFER_EFFICIENCY = 0.18
W_FLOW_SLOPE = 0.14
W_RECOVERY = 0.12
W_ENTROPY_COMPLEMENT = 0.10
W_ENTROPY_SLOPE_COMPLEMENT = 0.06


@dataclass(frozen=True)
class StepState:
    step: int
    reserve: float
    progress: float
    transfer: float
    disturbance: float


@dataclass(frozen=True)
class CheckpointObservation:
    scenario_id: str
    checkpoint: int
    T: float
    E: float
    Et: float
    F: float
    e: float
    flow_slope: float
    entropy_slope: float
    recovery: float
    reserve_drawdown: float
    transfer_efficiency: float
    entropy_adjusted_flow_margin: float
    trajectory_score: float
    outcome: str
    final_progress: float
    final_reserve: float


def _unit_hash(*parts: object) -> float:
    material = "|".join(str(p) for p in (DATASET_SEED, *parts))
    digest = hashlib.sha256(material.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") / (2**64 - 1)


def _noise(scenario_id: str, step: int) -> float:
    return (_unit_hash(scenario_id, step, "noise") - 0.5) * 0.18


def _pulse(scenario_id: str, step: int) -> float:
    """Frozen deterministic transient disturbance component.

    Pulses create recovery opportunities while remaining independent of outcomes
    and detector scores. Pulse timing/amplitude derive only from scenario identity.
    """
    center = 4 + int(_unit_hash(scenario_id, "pulse-center") * 16)
    width = 1 + int(_unit_hash(scenario_id, "pulse-width") * 3)
    amplitude = 0.08 + 0.22 * _unit_hash(scenario_id, "pulse-amplitude")
    distance = abs(step - center)
    if distance > width:
        return 0.0
    return amplitude * (1.0 - distance / (width + 1.0))


def _simulate(capability: float, transfer_policy: float, entropy_band: float, replicate: int) -> tuple[str, list[StepState], str, float, float]:
    scenario_id = f"C{capability:.2f}-U{transfer_policy:.2f}-D{entropy_band:.2f}-R{replicate}"
    reserve = 1.0
    progress = 0.0
    total_transfer = 0.0
    states: list[StepState] = []

    for step in range(1, HORIZON + 1):
        disturbance = min(0.98, max(0.0, entropy_band + _noise(scenario_id, step) + _pulse(scenario_id, step)))
        available = max(0.0, reserve)
        applied = min(available, capability * transfer_policy * 0.065)
        total_transfer += applied

        productive = applied * max(0.0, 1.0 - 0.78 * disturbance)
        progress += productive * (0.72 + 0.28 * capability)

        metabolic_cost = applied * (0.28 + 0.30 * disturbance)
        disturbance_cost = 0.014 + 0.030 * disturbance
        reserve = max(0.0, reserve - metabolic_cost - disturbance_cost)

        states.append(
            StepState(
                step=step,
                reserve=reserve,
                progress=progress,
                transfer=total_transfer,
                disturbance=disturbance,
            )
        )

    outcome = "A" if progress >= 0.50 and reserve >= 0.08 else "M"
    return scenario_id, states, outcome, progress, reserve


def _linear_slope(values: list[float]) -> float:
    n = len(values)
    if n < 2:
        return 0.0
    x_bar = (n - 1) / 2.0
    y_bar = sum(values) / n
    numerator = sum((i - x_bar) * (y - y_bar) for i, y in enumerate(values))
    denominator = sum((i - x_bar) ** 2 for i in range(n))
    return numerator / denominator if denominator else 0.0


def _recovery_metric(history: list[StepState]) -> float:
    if not history:
        return 0.0
    peak_index = max(range(len(history)), key=lambda i: history[i].disturbance)
    if peak_index >= len(history) - 1:
        return 0.0
    peak_progress = history[peak_index].progress
    later_progress = history[-1].progress
    available_steps = len(history) - peak_index - 1
    return max(0.0, min(1.0, (later_progress - peak_progress) / max(0.02 * available_steps, EPSILON)))


def _checkpoint_observation(
    scenario_id: str,
    states: list[StepState],
    outcome: str,
    final_progress: float,
    final_reserve: float,
    checkpoint: int,
) -> CheckpointObservation:
    history = states[:checkpoint]
    current = history[-1]
    window = max(2, checkpoint // 4)
    recent = history[-window:]

    T = checkpoint / HORIZON
    E = current.reserve
    Et = min(1.0, current.transfer / (HORIZON * 0.065))
    F = min(1.0, current.progress / 0.50)
    e = sum(s.disturbance for s in history) / checkpoint

    flow_values = [s.progress for s in recent]
    entropy_values = [s.disturbance for s in recent]
    raw_flow_slope = _linear_slope(flow_values)
    raw_entropy_slope = _linear_slope(entropy_values)

    # Normalize frozen history features into approximately [0,1] comparators.
    flow_slope = max(0.0, min(1.0, raw_flow_slope / 0.035))
    entropy_slope = max(-1.0, min(1.0, raw_entropy_slope / 0.12))
    recovery = _recovery_metric(history)
    reserve_drawdown = 1.0 - E
    transfer_efficiency = max(0.0, min(1.0, current.progress / max(current.transfer, EPSILON)))
    entropy_adjusted_flow_margin = F - e

    entropy_slope_complement = max(0.0, min(1.0, (1.0 - entropy_slope) / 2.0))
    trajectory_score = (
        W_F * F
        + W_E * E
        + W_TRANSFER_EFFICIENCY * transfer_efficiency
        + W_FLOW_SLOPE * flow_slope
        + W_RECOVERY * recovery
        + W_ENTROPY_COMPLEMENT * (1.0 - e)
        + W_ENTROPY_SLOPE_COMPLEMENT * entropy_slope_complement
    )

    return CheckpointObservation(
        scenario_id=scenario_id,
        checkpoint=checkpoint,
        T=T,
        E=E,
        Et=Et,
        F=F,
        e=e,
        flow_slope=flow_slope,
        entropy_slope=entropy_slope,
        recovery=recovery,
        reserve_drawdown=reserve_drawdown,
        transfer_efficiency=transfer_efficiency,
        entropy_adjusted_flow_margin=entropy_adjusted_flow_margin,
        trajectory_score=trajectory_score,
        outcome=outcome,
        final_progress=final_progress,
        final_reserve=final_reserve,
    )


def build_dataset() -> list[CheckpointObservation]:
    rows: list[CheckpointObservation] = []
    for capability in CAPABILITIES:
        for transfer_policy in TRANSFER_POLICIES:
            for entropy_band in ENTROPY_BANDS:
                for replicate in range(REPLICATES):
                    scenario_id, states, outcome, final_progress, final_reserve = _simulate(
                        capability, transfer_policy, entropy_band, replicate
                    )
                    for checkpoint in CHECKPOINTS:
                        rows.append(
                            _checkpoint_observation(
                                scenario_id,
                                states,
                                outcome,
                                final_progress,
                                final_reserve,
                                checkpoint,
                            )
                        )
    return rows


def _auc(values: Iterable[tuple[float, bool]]) -> float:
    pairs = list(values)
    pos = [v for v, y in pairs if y]
    neg = [v for v, y in pairs if not y]
    if not pos or not neg:
        raise ValueError("AUC requires both outcome classes")
    wins = sum((p > n) + 0.5 * (p == n) for p in pos for n in neg)
    return wins / (len(pos) * len(neg))


def _current_state_score(row: CheckpointObservation) -> float:
    # Frozen equal-weight geometric composite of current E, Et, F and 1-e.
    product = max(row.E, 0.0) * max(row.Et, 0.0) * max(row.F, 0.0) * max(1.0 - row.e, 0.0)
    return product ** 0.25


def _canonical_payload(rows: list[CheckpointObservation]) -> list[dict]:
    payload: list[dict] = []
    for row in rows:
        record = asdict(row)
        for key, value in tuple(record.items()):
            if isinstance(value, float):
                record[key] = format(value, f".{CANONICAL_FLOAT_DECIMALS}f")
        payload.append(record)
    return payload


def evaluate() -> dict:
    rows = build_dataset()
    trajectories = sorted({r.scenario_id for r in rows})
    terminal_by_id = {r.scenario_id: r.outcome for r in rows}
    aligned = sum(terminal_by_id[sid] == "A" for sid in trajectories)
    misaligned = len(trajectories) - aligned
    minority_fraction = min(aligned, misaligned) / len(trajectories)

    checkpoint_results: dict[str, dict[str, float]] = {}
    for checkpoint in CHECKPOINTS:
        subset = [r for r in rows if r.checkpoint == checkpoint]
        checkpoint_results[str(checkpoint)] = {
            "trajectory_dynamics": _auc((r.trajectory_score, r.outcome == "A") for r in subset),
            "F_only": _auc((r.F, r.outcome == "A") for r in subset),
            "E_only": _auc((r.E, r.outcome == "A") for r in subset),
            "entropy_only": _auc((1.0 - r.e, r.outcome == "A") for r in subset),
            "current_state_joint": _auc((_current_state_score(r), r.outcome == "A") for r in subset),
        }

    primary = checkpoint_results["12"]
    best_single = max(primary["E_only"], primary["F_only"], primary["entropy_only"])
    h1 = primary["trajectory_dynamics"] >= 0.75
    h2 = primary["trajectory_dynamics"] >= primary["F_only"] + 0.05
    h3 = primary["trajectory_dynamics"] >= best_single + 0.03
    early_supported = checkpoint_results["6"]["trajectory_dynamics"] >= 0.70

    valid = (
        len(trajectories) == 240
        and len(rows) == 240 * len(CHECKPOINTS)
        and minority_fraction >= 0.15
        and all(
            math.isfinite(value)
            for row in rows
            for key, value in asdict(row).items()
            if isinstance(value, float)
        )
    )

    classification = "SURVIVED" if valid and h1 and h2 and h3 else ("INVALID" if not valid else "FALSIFIED")
    canonical_payload = _canonical_payload(rows)
    dataset_sha256 = hashlib.sha256(
        json.dumps(canonical_payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()

    return {
        "experiment_id": EXPERIMENT_ID,
        "dataset_version": DATASET_VERSION,
        "dataset_seed": DATASET_SEED,
        "dataset_sha256": dataset_sha256,
        "canonical_float_decimals": CANONICAL_FLOAT_DECIMALS,
        "trajectory_count": len(trajectories),
        "observation_count": len(rows),
        "steps_per_trajectory": HORIZON,
        "aligned_count": aligned,
        "misaligned_count": misaligned,
        "minority_class_fraction": minority_fraction,
        "checkpoints": checkpoint_results,
        "criteria": {
            "validity": valid,
            "H1_step12_trajectory_auc_at_least_0_75": h1,
            "H2_step12_beats_F_by_0_05": h2,
            "H3_step12_beats_best_single_by_0_03": h3,
            "early_warning_step6_auc_at_least_0_70": early_supported,
        },
        "classification": classification,
        "early_warning_classification": "SUPPORTED" if early_supported else "NOT SUPPORTED",
        "frozen_weights": {
            "F": W_F,
            "E": W_E,
            "transfer_efficiency": W_TRANSFER_EFFICIENCY,
            "flow_slope": W_FLOW_SLOPE,
            "recovery": W_RECOVERY,
            "entropy_complement": W_ENTROPY_COMPLEMENT,
            "entropy_slope_complement": W_ENTROPY_SLOPE_COMPLEMENT,
        },
        "claim_boundary": "Synthetic deterministic trajectory evidence only; no canonical EFGM model change.",
    }


def _markdown(result: dict) -> str:
    lines = [
        f"# {EXPERIMENT_ID} — Trajectory Coherence and Early Transition Detection",
        "",
        f"- trajectories: **{result['trajectory_count']}**",
        f"- observations: **{result['observation_count']}**",
        f"- A / M: **{result['aligned_count']} / {result['misaligned_count']}**",
        f"- canonical dataset SHA-256: `{result['dataset_sha256']}`",
        "",
        "| Checkpoint | Trajectory dynamics | F only | E only | Entropy only | Current-state joint |",
        "|---:|---:|---:|---:|---:|---:|",
    ]
    for checkpoint in CHECKPOINTS:
        r = result["checkpoints"][str(checkpoint)]
        lines.append(
            f"| {checkpoint} | {r['trajectory_dynamics']:.4f} | {r['F_only']:.4f} | {r['E_only']:.4f} | {r['entropy_only']:.4f} | {r['current_state_joint']:.4f} |"
        )
    c = result["criteria"]
    lines.extend([
        "",
        "## Frozen criteria",
        f"- validity: **{c['validity']}**",
        f"- H1 step-12 trajectory AUC >= 0.75: **{c['H1_step12_trajectory_auc_at_least_0_75']}**",
        f"- H2 step-12 trajectory beats F-only by >= 0.05: **{c['H2_step12_beats_F_by_0_05']}**",
        f"- H3 step-12 trajectory beats best E/F/e single variable by >= 0.03: **{c['H3_step12_beats_best_single_by_0_03']}**",
        f"- early warning step-6 AUC >= 0.70: **{c['early_warning_step6_auc_at_least_0_70']}**",
        "",
        f"## Primary scientific classification: **{result['classification']}**",
        f"## Early-warning classification: **{result['early_warning_classification']}**",
        "",
        result["claim_boundary"],
    ])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    args = parser.parse_args()
    result = evaluate()
    print(json.dumps(result, indent=2, sort_keys=True) if args.format == "json" else _markdown(result))


if __name__ == "__main__":
    main()
