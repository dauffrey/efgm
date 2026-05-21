from __future__ import annotations

from .schemas import EntropyMetrics


DEFAULT_ENTROPY_WEIGHTS = {
    "contradiction_density": 0.25,
    "uncertainty_variance": 0.20,
    "memory_fragmentation": 0.20,
    "recursion_instability": 0.15,
    "context_decay": 0.20,
}


def weighted_entropy(metrics: EntropyMetrics, weights: dict[str, float] | None = None) -> float:
    weights = weights or DEFAULT_ENTROPY_WEIGHTS
    values = metrics.model_dump()
    total_weight = sum(weights.values())
    if total_weight <= 0:
        raise ValueError("Entropy weights must sum to a positive value.")

    score = sum(values[name] * weight for name, weight in weights.items()) / total_weight
    return round(score, 4)


def entropy_drivers(metrics: EntropyMetrics, threshold: float = 0.35) -> list[str]:
    labels = {
        "contradiction_density": "Contradiction density",
        "uncertainty_variance": "Uncertainty variance",
        "memory_fragmentation": "Memory fragmentation",
        "recursion_instability": "Recursion instability",
        "context_decay": "Context decay",
    }
    values = metrics.model_dump()
    return [labels[name] for name, value in values.items() if value >= threshold]
