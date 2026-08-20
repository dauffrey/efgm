"""EFGM-EXP-0011B superseding fresh deterministic holdout generation only.

This module intentionally does NOT implement AUC calculation, aggregation scoring,
or scientific classification. It only generates and fingerprints the prospectively
preregistered holdout so validity can be checked before scientific evaluation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import asdict, dataclass

EXPERIMENT_ID = "EFGM-EXP-0011B"
DATASET_VERSION = "coupled-state-superseding-holdout-v0.1"
DATASET_SEED = "EFGM-EXP-0011B-FRESH-HOLDOUT-2026-08-19"
SEED_START = 120001
SEED_END = 120288
HORIZON = 24
CHECKPOINTS = (6, 12, 18)
CAPABILITIES = (0.30, 0.42, 0.54, 0.66, 0.78, 0.90)
TRANSFER_POLICIES = (0.45, 0.62, 0.79, 0.96)
ENTROPY_BANDS = (0.10, 0.25, 0.40, 0.55, 0.70, 0.82)
REPLICATES = 2
CANONICAL_FLOAT_DECIMALS = 12


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
    scenario_seed: int
    checkpoint: int
    T: float
    E: float
    Et: float
    F: float
    e: float
    outcome: str
    final_progress: float
    final_reserve: float


def _unit_hash(*parts: object) -> float:
    material = "|".join(str(p) for p in (DATASET_SEED, *parts))
    digest = hashlib.sha256(material.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") / (2**64 - 1)


def _noise(scenario_seed: int, step: int) -> float:
    return (_unit_hash(scenario_seed, step, "noise") - 0.5) * 0.18


def _pulse(scenario_seed: int, step: int) -> float:
    center = 4 + int(_unit_hash(scenario_seed, "pulse-center") * 16)
    width = 1 + int(_unit_hash(scenario_seed, "pulse-width") * 3)
    amplitude = 0.08 + 0.22 * _unit_hash(scenario_seed, "pulse-amplitude")
    distance = abs(step - center)
    if distance > width:
        return 0.0
    return amplitude * (1.0 - distance / (width + 1.0))


def _factors_for_seed(scenario_seed: int) -> tuple[float, float, float, int]:
    index = scenario_seed - SEED_START
    if index < 0 or scenario_seed > SEED_END:
        raise ValueError("scenario seed outside frozen EXP-0011B interval")

    replicate = index % REPLICATES
    index //= REPLICATES
    entropy_band = ENTROPY_BANDS[index % len(ENTROPY_BANDS)]
    index //= len(ENTROPY_BANDS)
    transfer_policy = TRANSFER_POLICIES[index % len(TRANSFER_POLICIES)]
    index //= len(TRANSFER_POLICIES)
    capability = CAPABILITIES[index % len(CAPABILITIES)]
    return capability, transfer_policy, entropy_band, replicate


def _simulate(scenario_seed: int) -> tuple[str, list[StepState], str, float, float]:
    capability, transfer_policy, entropy_band, replicate = _factors_for_seed(scenario_seed)
    scenario_id = (
        f"EXP0011B-S{scenario_seed}-C{capability:.2f}-U{transfer_policy:.2f}"
        f"-D{entropy_band:.2f}-R{replicate}"
    )
    reserve = 1.0
    progress = 0.0
    total_transfer = 0.0
    states: list[StepState] = []

    for step in range(1, HORIZON + 1):
        disturbance = min(
            0.98,
            max(0.0, entropy_band + _noise(scenario_seed, step) + _pulse(scenario_seed, step)),
        )
        available = max(0.0, reserve)
        applied = min(available, capability * transfer_policy * 0.065)
        total_transfer += applied

        productive = applied * max(0.0, 1.0 - 0.78 * disturbance)
        progress += productive * (0.72 + 0.28 * capability)

        metabolic_cost = applied * (0.28 + 0.30 * disturbance)
        disturbance_cost = 0.014 + 0.030 * disturbance
        reserve = max(0.0, reserve - metabolic_cost - disturbance_cost)

        states.append(StepState(step, reserve, progress, total_transfer, disturbance))

    outcome = "A" if progress >= 0.50 and reserve >= 0.08 else "M"
    return scenario_id, states, outcome, progress, reserve


def _checkpoint_observation(
    scenario_id: str,
    scenario_seed: int,
    states: list[StepState],
    outcome: str,
    final_progress: float,
    final_reserve: float,
    checkpoint: int,
) -> CheckpointObservation:
    history = states[:checkpoint]
    current = history[-1]
    return CheckpointObservation(
        scenario_id=scenario_id,
        scenario_seed=scenario_seed,
        checkpoint=checkpoint,
        T=checkpoint / HORIZON,
        E=current.reserve,
        Et=min(1.0, current.transfer / (HORIZON * 0.065)),
        F=min(1.0, current.progress / 0.50),
        e=sum(s.disturbance for s in history) / checkpoint,
        outcome=outcome,
        final_progress=final_progress,
        final_reserve=final_reserve,
    )


def build_dataset() -> list[CheckpointObservation]:
    rows: list[CheckpointObservation] = []
    for scenario_seed in range(SEED_START, SEED_END + 1):
        scenario_id, states, outcome, final_progress, final_reserve = _simulate(scenario_seed)
        for checkpoint in CHECKPOINTS:
            rows.append(
                _checkpoint_observation(
                    scenario_id,
                    scenario_seed,
                    states,
                    outcome,
                    final_progress,
                    final_reserve,
                    checkpoint,
                )
            )
    return rows


def _canonical_payload(rows: list[CheckpointObservation]) -> list[dict]:
    payload: list[dict] = []
    for row in rows:
        record = asdict(row)
        for key, value in tuple(record.items()):
            if isinstance(value, float):
                record[key] = format(value, f".{CANONICAL_FLOAT_DECIMALS}f")
        payload.append(record)
    return payload


def dataset_manifest() -> dict:
    rows = build_dataset()
    scenario_ids = sorted({row.scenario_id for row in rows})
    seeds = sorted({row.scenario_seed for row in rows})
    terminal_by_id = {row.scenario_id: row.outcome for row in rows}
    aligned = sum(terminal_by_id[sid] == "A" for sid in scenario_ids)
    misaligned = len(scenario_ids) - aligned
    minority_fraction = min(aligned, misaligned) / len(scenario_ids)
    canonical = _canonical_payload(rows)
    dataset_sha256 = hashlib.sha256(
        json.dumps(canonical, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()

    return {
        "experiment_id": EXPERIMENT_ID,
        "dataset_version": DATASET_VERSION,
        "dataset_seed": DATASET_SEED,
        "dataset_sha256": dataset_sha256,
        "canonical_float_decimals": CANONICAL_FLOAT_DECIMALS,
        "scenario_count": len(scenario_ids),
        "observation_count": len(rows),
        "steps_per_scenario": HORIZON,
        "checkpoints": list(CHECKPOINTS),
        "seed_start": SEED_START,
        "seed_end": SEED_END,
        "seed_count": len(seeds),
        "aligned_count": aligned,
        "misaligned_count": misaligned,
        "minority_class_fraction": minority_fraction,
        "scientific_scoring_exposed": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate EXP-0011B superseding fresh holdout manifest without scientific scoring"
    )
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args()
    manifest = dataset_manifest()
    if args.format == "json":
        print(json.dumps(manifest, indent=2, sort_keys=True))
        return
    print("# EFGM-EXP-0011B superseding fresh holdout manifest")
    print()
    for key, value in manifest.items():
        print(f"- {key}: `{value}`")


if __name__ == "__main__":
    main()
