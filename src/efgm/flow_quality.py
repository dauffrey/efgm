from __future__ import annotations

from .schemas import FlowQualityMetrics


DEFAULT_FLOW_QUALITY_WEIGHTS = {
    "task_completion_consistency": 0.30,
    "reasoning_continuity": 0.25,
    "semantic_coherence": 0.25,
    "verification_success_rate": 0.20,
}


def weighted_flow_quality(metrics: FlowQualityMetrics, weights: dict[str, float] | None = None) -> float:
    weights = weights or DEFAULT_FLOW_QUALITY_WEIGHTS
    values = metrics.model_dump()
    total_weight = sum(weights.values())
    if total_weight <= 0:
        raise ValueError("Flow-quality weights must sum to a positive value.")

    score = sum(values[name] * weight for name, weight in weights.items()) / total_weight
    return round(score, 4)
