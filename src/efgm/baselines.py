from __future__ import annotations

from math import sqrt

from .schemas_v2 import EFGMDecisionInput
from .scoring_v2 import load_scoring_config, weighted_score


BASELINE_VERSION = "efgm-comparison-baselines-v0.1"


def _components(input_data: EFGMDecisionInput) -> dict[str, float]:
    config = load_scoring_config()
    weights = config["weights"]
    return {
        "T": input_data.T.value,
        "C": input_data.C.value,
        "Fq": weighted_score(input_data.flow_quality, weights["flow_quality"]),
        "G": weighted_score(input_data.grounding, weights["grounding"]),
        "U": input_data.uncertainty_calibration.value,
        "Eo": weighted_score(input_data.output_entropy, weights["output_entropy"]),
        "Be": weighted_score(input_data.behavioral_entropy, weights["behavioral_entropy"]),
        "Oe": weighted_score(input_data.operational_entropy, weights["operational_entropy"]),
    }


def checklist_baseline(input_data: EFGMDecisionInput) -> float:
    """Deliberately simple five-check baseline for complexity comparison."""
    c = _components(input_data)
    checks = [
        c["G"] >= 0.60,
        c["U"] >= 0.60,
        c["Fq"] >= 0.60,
        c["Eo"] <= 0.35,
        c["Oe"] <= 0.35,
    ]
    return round(sum(checks) / len(checks), 4)


def grounding_calibration_baseline(input_data: EFGMDecisionInput) -> float:
    """Two-factor baseline testing whether G and U explain most ranking value."""
    c = _components(input_data)
    return round(sqrt(c["G"] * c["U"]), 4)


def weighted_linear_baseline(input_data: EFGMDecisionInput) -> float:
    """Transparent linear baseline using the same major composites without EFGM's formula."""
    c = _components(input_data)
    positive = (c["T"] + c["C"] + c["Fq"] + c["G"] + c["U"]) / 5
    degradation = (c["Eo"] + c["Be"] + c["Oe"]) / 3
    return round(max(0.0, min(1.0, positive - 0.50 * degradation)), 4)
