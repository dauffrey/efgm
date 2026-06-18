from __future__ import annotations

from math import prod

from .entropy import entropy_drivers, weighted_entropy
from .flow_quality import weighted_flow_quality
from .schemas import EFGMInput, EFGMResult, Classification


def classify_flow(score: float) -> Classification:
    if score >= 0.80:
        return "Coherent"
    if score >= 0.60:
        return "Stable with watch items"
    if score >= 0.40:
        return "Degraded but usable"
    if score >= 0.20:
        return "High entropy"
    return "Misaligned"


def recommended_action(classification: Classification) -> str:
    actions = {
        "Coherent": "Proceed. Continue normal monitoring.",
        "Stable with watch items": "Proceed with monitoring. Track watch items.",
        "Degraded but usable": "Verify assumptions and reduce entropy before relying on the result.",
        "High entropy": "Pause. Correct missing context, contradictions, or verification gaps.",
        "Misaligned": "Stop and escalate. Rebuild the reasoning or workflow from verified evidence.",
    }
    return actions[classification]


def geometric_mean(values: list[float]) -> float:
    """Return the geometric mean for normalized positive quality factors.

    EFGM uses this instead of raw multiplication so strong-but-imperfect
    factors do not collapse the final score too aggressively.
    """
    if not values:
        raise ValueError("At least one value is required for geometric mean.")
    if any(value < 0 for value in values):
        raise ValueError("Geometric mean values must be non-negative.")

    return prod(values) ** (1 / len(values))


def score_efgm(input_data: EFGMInput) -> EFGMResult:
    e = weighted_entropy(input_data.entropy)
    fq = weighted_flow_quality(input_data.flow_quality)

    quality_core = geometric_mean([input_data.T, input_data.E, fq])
    coherent_flow = quality_core / (1 + e)
    coherent_flow = round(coherent_flow, 4)

    classification = classify_flow(coherent_flow)

    return EFGMResult(
        task_id=input_data.task_id,
        T=input_data.T,
        E=input_data.E,
        Fq=fq,
        e=e,
        F=coherent_flow,
        classification=classification,
        recommended_action=recommended_action(classification),
        entropy_drivers=entropy_drivers(input_data.entropy),
    )
