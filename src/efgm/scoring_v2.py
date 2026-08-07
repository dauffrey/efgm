from __future__ import annotations

import json
from importlib.resources import files
from math import prod
from pathlib import Path
from typing import Any, Mapping

from .schemas_v2 import DecisionClassification, EFGMDecisionInput, EFGMDecisionResult


DEFAULT_CONFIG_DIR = "config"
DEFAULT_CONFIG_NAME = "efgm-v2.0-baseline.json"


def load_scoring_config(config: str | Path | Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Load a versioned v2 scoring configuration.

    The default configuration is packaged with EFGM. Experimental configurations may
    be passed as a path or mapping so weight/threshold changes remain reproducible.
    """
    if config is None:
        resource = files("efgm").joinpath(DEFAULT_CONFIG_DIR).joinpath(DEFAULT_CONFIG_NAME)
        loaded = json.loads(resource.read_text(encoding="utf-8"))
    elif isinstance(config, Mapping):
        loaded = dict(config)
    else:
        loaded = json.loads(Path(config).read_text(encoding="utf-8"))

    required_sections = {
        "input_entropy",
        "output_entropy",
        "flow_quality",
        "grounding",
        "behavioral_entropy",
        "operational_entropy",
    }
    if not loaded.get("config_id"):
        raise ValueError("Scoring configuration must define config_id.")
    if set(loaded.get("weights", {})) != required_sections:
        raise ValueError("Scoring configuration has missing or unexpected weight sections.")
    for section, weights in loaded["weights"].items():
        if not weights or sum(weights.values()) <= 0:
            raise ValueError(f"Weights for {section} must sum to a positive value.")
    if "classification" not in loaded or "driver_thresholds" not in loaded:
        raise ValueError("Scoring configuration must define classification and driver_thresholds.")
    return loaded


def weighted_score(metrics: Any, weights: dict[str, float]) -> float:
    total_weight = sum(weights.values())
    if total_weight <= 0:
        raise ValueError("Weights must sum to a positive value.")

    score = sum(getattr(metrics, name).value * weight for name, weight in weights.items()) / total_weight
    return round(score, 4)


def low_score_drivers(metrics: Any, threshold: float = 0.60) -> list[str]:
    return [
        name
        for name in metrics.__class__.model_fields
        if getattr(metrics, name).value < threshold
    ]


def high_score_drivers(metrics: Any, threshold: float = 0.35) -> list[str]:
    return [
        name
        for name in metrics.__class__.model_fields
        if getattr(metrics, name).value >= threshold
    ]


def geometric_mean(values: list[float]) -> float:
    if not values:
        raise ValueError("At least one value is required for geometric mean.")
    if any(value < 0 for value in values):
        raise ValueError("Geometric mean values must be non-negative.")

    return prod(values) ** (1 / len(values))


def classify_decision(
    decision_quality: float,
    grounding: float,
    output_entropy: float,
    thresholds: Mapping[str, float],
) -> DecisionClassification:
    # Grounding is a validity gate: sufficiently weak real-world support must not be
    # masked by a strong aggregate DQ score or polished internal coherence.
    if grounding < thresholds["critical_grounding_threshold"]:
        return "Weakly grounded - verification required"
    if (
        decision_quality >= thresholds["coherent_dq_threshold"]
        and grounding >= thresholds["coherent_grounding_threshold"]
        and output_entropy <= thresholds["coherent_max_output_entropy"]
    ):
        return "Coherent and grounded"
    if (
        decision_quality >= thresholds["weakly_grounded_dq_threshold"]
        and grounding < thresholds["weakly_grounded_grounding_threshold"]
    ):
        return "Coherent but weakly grounded"
    if decision_quality >= thresholds["stable_dq_threshold"]:
        return "Stable with watch items"
    if decision_quality >= thresholds["degraded_dq_threshold"]:
        return "Degraded but usable"
    if decision_quality >= thresholds["high_entropy_dq_threshold"]:
        return "High entropy"
    return "Misaligned"


def recommended_action(classification: DecisionClassification) -> str:
    actions = {
        "Coherent and grounded": "Proceed. Continue normal monitoring.",
        "Coherent but weakly grounded": "Do not rely on coherence alone. Add evidence, tests, citations, or domain verification.",
        "Weakly grounded - verification required": "Pause reliance on the result. Establish valid evidence and traceability before proceeding.",
        "Stable with watch items": "Proceed with monitoring. Track entropy, uncertainty, and grounding gaps.",
        "Degraded but usable": "Verify assumptions and reduce entropy before relying on the result.",
        "High entropy": "Pause. Correct contradictions, missing context, or verification gaps.",
        "Misaligned": "Stop and escalate. Rebuild from verified evidence.",
    }
    return actions[classification]


def score_decision_efgm(
    input_data: EFGMDecisionInput,
    config: str | Path | Mapping[str, Any] | None = None,
) -> EFGMDecisionResult:
    scoring_config = load_scoring_config(config)
    weights = scoring_config["weights"]

    Ei = weighted_score(input_data.input_entropy, weights["input_entropy"])
    Eo = weighted_score(input_data.output_entropy, weights["output_entropy"])
    Fq = weighted_score(input_data.flow_quality, weights["flow_quality"])
    G = weighted_score(input_data.grounding, weights["grounding"])
    Be = weighted_score(input_data.behavioral_entropy, weights["behavioral_entropy"])
    Oe = weighted_score(input_data.operational_entropy, weights["operational_entropy"])
    H = input_data.input_entropy.hidden_information_load.value
    U = input_data.uncertainty_calibration.value
    T = input_data.T.value
    C = input_data.C.value

    epsilon = float(scoring_config.get("epsilon", 0.01))
    CRC = round((Ei - Eo) / max(Ei, epsilon), 4)

    Q = round(geometric_mean([T, C, Fq, G, U]), 4)
    DQ = round(Q / (1 + Eo + Be + Oe), 4)

    outcome_confidence = round(DQ * (1 - H), 4)

    OQ = input_data.outcome_quality.value if input_data.outcome_quality is not None else None
    OD = round(OQ - DQ, 4) if OQ is not None else None

    classification = classify_decision(DQ, G, Eo, scoring_config["classification"])
    driver_thresholds = scoring_config["driver_thresholds"]

    return EFGMDecisionResult(
        task_id=input_data.task_id,
        config_id=scoring_config["config_id"],
        T=T,
        C=C,
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
        input_entropy_drivers=high_score_drivers(input_data.input_entropy, driver_thresholds["high_score"]),
        output_entropy_drivers=high_score_drivers(input_data.output_entropy, driver_thresholds["high_score"]),
        grounding_drivers=low_score_drivers(input_data.grounding, driver_thresholds["low_score"]),
        behavioral_entropy_drivers=high_score_drivers(input_data.behavioral_entropy, driver_thresholds["high_score"]),
        operational_entropy_drivers=high_score_drivers(input_data.operational_entropy, driver_thresholds["high_score"]),
    )
