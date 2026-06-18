from __future__ import annotations

from math import prod
from typing import Any

from .schemas_v2 import (
    BehavioralEntropyMetrics,
    DecisionClassification,
    EFGMDecisionInput,
    EFGMDecisionResult,
    FlowQualityMetricsV2,
    GroundingMetrics,
    InputEntropyMetrics,
    OperationalEntropyMetrics,
    OutputEntropyMetrics,
)

EPSILON = 0.01

DEFAULT_INPUT_ENTROPY_WEIGHTS = {
    "input_contradiction": 0.20,
    "input_ambiguity": 0.20,
    "input_goal_conflict": 0.20,
    "missing_context": 0.20,
    "hidden_information_load": 0.20,
}

DEFAULT_OUTPUT_ENTROPY_WEIGHTS = {
    "output_contradiction": 0.25,
    "uncertainty_mismatch": 0.25,
    "goal_drift": 0.20,
    "reasoning_instability": 0.15,
    "context_decay": 0.15,
}

DEFAULT_FLOW_QUALITY_WEIGHTS = {
    "task_completion_consistency": 0.30,
    "reasoning_continuity": 0.25,
    "semantic_coherence": 0.25,
    "verification_success_rate": 0.20,
}

DEFAULT_GROUNDING_WEIGHTS = {
    "rule_support": 0.25,
    "evidence_validity": 0.25,
    "traceability": 0.20,
    "factual_consistency": 0.20,
    "domain_calibration": 0.10,
}

DEFAULT_BEHAVIORAL_ENTROPY_WEIGHTS = {
    "chasing_behavior": 0.25,
    "outcome_bias": 0.20,
    "sunk_cost_pressure": 0.20,
    "false_pattern_detection": 0.20,
    "overconfidence_feedback": 0.15,
}

DEFAULT_OPERATIONAL_ENTROPY_WEIGHTS = {
    "timeout_rate": 0.25,
    "retry_instability": 0.20,
    "tool_failure_rate": 0.25,
    "latency_pressure": 0.15,
    "workflow_interruption": 0.15,
}


def weighted_score(metrics: Any, weights: dict[str, float]) -> float:
    values = metrics.model_dump()
    total_weight = sum(weights.values())
    if total_weight <= 0:
        raise ValueError("Weights must sum to a positive value.")

    score = sum(values[name] * weight for name, weight in weights.items()) / total_weight
    return round(score, 4)


def low_score_drivers(metrics: Any, threshold: float = 0.60) -> list[str]:
    values = metrics.model_dump()
    return [name for name, value in values.items() if value < threshold]


def high_score_drivers(metrics: Any, threshold: float = 0.35) -> list[str]:
    values = metrics.model_dump()
    return [name for name, value in values.items() if value >= threshold]


def geometric_mean(values: list[float]) -> float:
    if not values:
        raise ValueError("At least one value is required for geometric mean.")
    if any(value < 0 for value in values):
        raise ValueError("Geometric mean values must be non-negative.")

    return prod(values) ** (1 / len(values))


def classify_decision(decision_quality: float, grounding: float, output_entropy: float) -> DecisionClassification:
    if decision_quality >= 0.80 and grounding >= 0.70 and output_entropy <= 0.20:
        return "Coherent and grounded"
    if decision_quality >= 0.70 and grounding < 0.70:
        return "Coherent but weakly grounded"
    if decision_quality >= 0.60:
        return "Stable with watch items"
    if decision_quality >= 0.40:
        return "Degraded but usable"
    if decision_quality >= 0.20:
        return "High entropy"
    return "Misaligned"


def recommended_action(classification: DecisionClassification) -> str:
    actions = {
        "Coherent and grounded": "Proceed. Continue normal monitoring.",
        "Coherent but weakly grounded": "Do not rely on coherence alone. Add evidence, tests, citations, or domain verification.",
        "Stable with watch items": "Proceed with monitoring. Track entropy, uncertainty, and grounding gaps.",
        "Degraded but usable": "Verify assumptions and reduce entropy before relying on the result.",
        "High entropy": "Pause. Correct contradictions, missing context, or verification gaps.",
        "Misaligned": "Stop and escalate. Rebuild from verified evidence.",
    }
    return actions[classification]


def score_decision_efgm(input_data: EFGMDecisionInput) -> EFGMDecisionResult:
    Ei = weighted_score(input_data.input_entropy, DEFAULT_INPUT_ENTROPY_WEIGHTS)
    Eo = weighted_score(input_data.output_entropy, DEFAULT_OUTPUT_ENTROPY_WEIGHTS)
    Fq = weighted_score(input_data.flow_quality, DEFAULT_FLOW_QUALITY_WEIGHTS)
    G = weighted_score(input_data.grounding, DEFAULT_GROUNDING_WEIGHTS)
    Be = weighted_score(input_data.behavioral_entropy, DEFAULT_BEHAVIORAL_ENTROPY_WEIGHTS)
    Oe = weighted_score(input_data.operational_entropy, DEFAULT_OPERATIONAL_ENTROPY_WEIGHTS)
    H = input_data.input_entropy.hidden_information_load
    U = input_data.uncertainty_calibration

    CRC = (Ei - Eo) / max(Ei, EPSILON)
    CRC = round(CRC, 4)

    Q = geometric_mean([input_data.T, input_data.C, Fq, G, U])
    Q = round(Q, 4)

    DQ = Q / (1 + Eo + Be + Oe)
    DQ = round(DQ, 4)

    outcome_confidence = round(DQ * (1 - H), 4)

    OQ = input_data.outcome_quality
    OD = round(OQ - DQ, 4) if OQ is not None else None

    classification = classify_decision(DQ, G, Eo)

    return EFGMDecisionResult(
        task_id=input_data.task_id,
        T=input_data.T,
        C=input_data.C,
        Fq=Fq,
        G=G,
        U=U,
        Ei=Ei,
        Eo=Eo,
        Be=Be,
        Oe=Oe,
        H=H,
        CRC=CRC,
        Q=Q,
        DQ=DQ,
        outcome_confidence=outcome_confidence,
        OQ=OQ,
        OD=OD,
        classification=classification,
        recommended_action=recommended_action(classification),
        input_entropy_drivers=high_score_drivers(input_data.input_entropy),
        output_entropy_drivers=high_score_drivers(input_data.output_entropy),
        grounding_drivers=low_score_drivers(input_data.grounding),
        behavioral_entropy_drivers=high_score_drivers(input_data.behavioral_entropy),
        operational_entropy_drivers=high_score_drivers(input_data.operational_entropy),
    )
