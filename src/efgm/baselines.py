from __future__ import annotations

from math import sqrt
from typing import Mapping

from .schemas_v2 import EFGMDecisionInput
from .scoring_v2 import load_scoring_config, weighted_score


BASELINE_VERSION = "efgm-comparison-baselines-v0.2"
INDEPENDENT_CHECKS = {
    "evidence_supported",
    "internally_consistent",
    "uncertainty_appropriate",
    "scope_aligned",
    "execution_reliable",
}


def _components(input_data: EFGMDecisionInput) -> dict[str, float]:
    """EFGM-derived components used only for aggregation/ablation baselines."""
    config = load_scoring_config()
    weights = config["weights"]
    return {
        "T": input_data.T.value,
        "C": input_data.C.value,
        "Fq": weighted_score(input_data.flow_quality, weights["flow_quality"], family_name="flow_quality"),
        "G": weighted_score(input_data.grounding, weights["grounding"], family_name="grounding"),
        "U": input_data.uncertainty_calibration.value,
        "Eo": weighted_score(input_data.output_entropy, weights["output_entropy"], family_name="output_entropy"),
        "Be": weighted_score(
            input_data.behavioral_entropy,
            weights["behavioral_entropy"],
            family_name="behavioral_entropy",
            allow_all_not_applicable=True,
        ),
        "Oe": weighted_score(
            input_data.operational_entropy,
            weights["operational_entropy"],
            family_name="operational_entropy",
            allow_all_not_applicable=True,
        ),
    }


def checklist_baseline(input_data: EFGMDecisionInput) -> float:
    """EFGM-derived five-check ablation baseline.

    This is intentionally *not* an independent comparator: it uses EFGM composites
    and exists to test whether the full v2 aggregation adds value beyond simple
    thresholds over the same observations.
    """
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
    """EFGM-derived two-factor ablation testing whether G and U explain most ranking value."""
    c = _components(input_data)
    return round(sqrt(c["G"] * c["U"]), 4)


def weighted_linear_baseline(input_data: EFGMDecisionInput) -> float:
    """EFGM-derived linear aggregation baseline over the same major composites."""
    c = _components(input_data)
    positive_values = [value for value in (c["T"], c["C"], c["Fq"], c["G"], c["U"]) if value is not None]
    positive = sum(positive_values) / len(positive_values)
    degradation = (c["Eo"] + c["Be"] + c["Oe"]) / 3
    return round(max(0.0, min(1.0, positive - 0.50 * degradation)), 4)


def independent_checklist_baseline(checks: Mapping[str, bool | float | int]) -> float:
    """Independent five-criterion checklist that does not consume EFGM composite scores.

    Benchmark authors establish these criteria independently of EFGM before scoring.
    Values may be booleans or normalized [0,1] ratings. This comparator is intended
    to answer whether EFGM adds value beyond a small, directly judged checklist.
    """
    if set(checks) != INDEPENDENT_CHECKS:
        missing = sorted(INDEPENDENT_CHECKS - set(checks))
        extra = sorted(set(checks) - INDEPENDENT_CHECKS)
        raise ValueError(f"Independent checklist keys mismatch; missing={missing}, extra={extra}")

    values: list[float] = []
    for name in sorted(INDEPENDENT_CHECKS):
        value = checks[name]
        if isinstance(value, bool):
            values.append(1.0 if value else 0.0)
            continue
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            numeric = float(value)
            if 0.0 <= numeric <= 1.0:
                values.append(numeric)
                continue
        raise ValueError(f"Independent checklist value for {name} must be bool or normalized [0,1].")

    return round(sum(values) / len(values), 4)
