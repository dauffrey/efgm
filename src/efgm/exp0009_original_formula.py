"""EFGM-EXP-0009: deterministic direct test of the original EFGM variables.

This experiment does not alter or reinterpret the preserved original expression:
    T × E = Et ~ F ± e = A|M

It operationalizes the variables only for this synthetic falsification test and
compares a frozen joint coherence proxy against simpler single-variable baselines.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from dataclasses import asdict, dataclass
from typing import Iterable

EXPERIMENT_ID = "EFGM-EXP-0009"
DATASET_VERSION = "original-formula-synthetic-v0.1"
DATASET_SEED = "EFGM-EXP-0009-FROZEN-SEED-2026-08-18"
HORIZON = 8
CAPABILITIES = (0.30, 0.45, 0.60, 0.75, 0.90)
TRANSFER_POLICIES = (0.45, 0.65, 0.85, 1.00)
ENTROPY_BANDS = (0.10, 0.25, 0.40, 0.55, 0.70)
REPLICATES = 2


@dataclass(frozen=True)
class Observation:
    scenario_id: str
    T: float
    E: float
    Et: float
    F: float
    e: float
    outcome: str
    final_progress: float
    final_reserve: float
    coherence_proxy: float


def _noise(scenario_id: str, step: int) -> float:
    digest = hashlib.sha256(f"{DATASET_SEED}|{scenario_id}|{step}".encode()).digest()
    unit = int.from_bytes(digest[:8], "big") / (2**64 - 1)
    return (unit - 0.5) * 0.16


def _trajectory(capability: float, transfer_policy: float, entropy_band: float, replicate: int) -> Observation:
    scenario_id = f"E{capability:.2f}-U{transfer_policy:.2f}-D{entropy_band:.2f}-R{replicate}"
    reserve = 1.0
    progress = 0.0
    total_transfer = 0.0
    entropies: list[float] = []
    executed = 0

    for step in range(HORIZON):
        if reserve <= 0.0:
            break
        disturbance = min(0.95, max(0.0, entropy_band + _noise(scenario_id, step)))
        entropies.append(disturbance)
        applied = min(reserve, capability * transfer_policy * 0.18)
        total_transfer += applied
        productive = applied * max(0.0, 1.0 - 0.75 * disturbance)
        progress += productive * (0.70 + 0.30 * capability)
        reserve = max(0.0, reserve - applied * (0.35 + 0.25 * disturbance) - 0.05 * disturbance)
        executed += 1

    T = executed / HORIZON
    E = capability
    Et = min(1.0, total_transfer / (HORIZON * 0.18))
    F = min(1.0, progress / 0.55)
    e = sum(entropies) / len(entropies) if entropies else 1.0
    outcome = "A" if progress >= 0.55 and reserve >= 0.10 else "M"

    # Frozen experiment-only operational proxy. This is NOT the original EFGM
    # formula and is not proposed as a canonical model change.
    coherence_proxy = (max(T * E * Et * F, 0.0) ** 0.25) / (1.0 + e)

    return Observation(
        scenario_id=scenario_id,
        T=T,
        E=E,
        Et=Et,
        F=F,
        e=e,
        outcome=outcome,
        final_progress=progress,
        final_reserve=reserve,
        coherence_proxy=coherence_proxy,
    )


def build_dataset() -> list[Observation]:
    return [
        _trajectory(E, u, d, r)
        for E in CAPABILITIES
        for u in TRANSFER_POLICIES
        for d in ENTROPY_BANDS
        for r in range(REPLICATES)
    ]


def _auc(values: Iterable[tuple[float, bool]]) -> float:
    pairs = list(values)
    pos = [v for v, y in pairs if y]
    neg = [v for v, y in pairs if not y]
    if not pos or not neg:
        raise ValueError("AUC requires both outcome classes")
    wins = sum((p > n) + 0.5 * (p == n) for p in pos for n in neg)
    return wins / (len(pos) * len(neg))


def evaluate() -> dict:
    rows = build_dataset()
    aligned = sum(row.outcome == "A" for row in rows)
    misaligned = len(rows) - aligned
    class_fraction = min(aligned, misaligned) / len(rows)

    aucs = {
        "joint_proxy": _auc((r.coherence_proxy, r.outcome == "A") for r in rows),
        "T_only": _auc((r.T, r.outcome == "A") for r in rows),
        "E_only": _auc((r.E, r.outcome == "A") for r in rows),
        "Et_only": _auc((r.Et, r.outcome == "A") for r in rows),
        "F_only": _auc((r.F, r.outcome == "A") for r in rows),
        "entropy_only": _auc((1.0 - r.e, r.outcome == "A") for r in rows),
    }

    h1 = aucs["joint_proxy"] >= 0.75
    h2 = aucs["joint_proxy"] >= max(aucs["E_only"], aucs["entropy_only"]) + 0.05
    h3 = aucs["joint_proxy"] >= aucs["F_only"] + 0.02
    valid = class_fraction >= 0.15
    classification = "SURVIVED" if valid and h1 and h2 and h3 else ("INVALID" if not valid else "FALSIFIED")

    dataset_payload = [asdict(r) for r in rows]
    dataset_sha256 = hashlib.sha256(
        json.dumps(dataset_payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()

    return {
        "experiment_id": EXPERIMENT_ID,
        "dataset_version": DATASET_VERSION,
        "dataset_seed": DATASET_SEED,
        "dataset_sha256": dataset_sha256,
        "trajectory_count": len(rows),
        "aligned_count": aligned,
        "misaligned_count": misaligned,
        "minimum_class_fraction": class_fraction,
        "aucs": aucs,
        "criteria": {
            "H1_joint_auc_at_least_0_75": h1,
            "H2_joint_beats_E_and_entropy_by_0_05": h2,
            "H3_joint_beats_F_by_0_02": h3,
            "validity_minority_class_at_least_0_15": valid,
        },
        "classification": classification,
        "claim_boundary": "Synthetic deterministic evidence only; no canonical EFGM model change.",
    }


def _markdown(result: dict) -> str:
    a = result["aucs"]
    c = result["criteria"]
    return "\n".join([
        f"# {EXPERIMENT_ID} — Original-formula direct deterministic test",
        "",
        f"- trajectories: **{result['trajectory_count']}**",
        f"- A / M: **{result['aligned_count']} / {result['misaligned_count']}**",
        f"- dataset SHA-256: `{result['dataset_sha256']}`",
        f"- joint proxy AUC: **{a['joint_proxy']:.4f}**",
        f"- T-only AUC: **{a['T_only']:.4f}**",
        f"- E-only AUC: **{a['E_only']:.4f}**",
        f"- Et-only AUC: **{a['Et_only']:.4f}**",
        f"- F-only AUC: **{a['F_only']:.4f}**",
        f"- entropy-only AUC: **{a['entropy_only']:.4f}**",
        "",
        "## Frozen criteria",
        f"- H1 joint AUC >= 0.75: **{c['H1_joint_auc_at_least_0_75']}**",
        f"- H2 joint beats E-only and entropy-only by >= 0.05: **{c['H2_joint_beats_E_and_entropy_by_0_05']}**",
        f"- H3 joint beats F-only by >= 0.02: **{c['H3_joint_beats_F_by_0_02']}**",
        f"- validity minority class >= 15%: **{c['validity_minority_class_at_least_0_15']}**",
        "",
        f"## Scientific classification: **{result['classification']}**",
        "",
        result["claim_boundary"],
    ])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    args = parser.parse_args()
    result = evaluate()
    print(json.dumps(result, indent=2, sort_keys=True) if args.format == "json" else _markdown(result))


if __name__ == "__main__":
    main()
