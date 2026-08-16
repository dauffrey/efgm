from __future__ import annotations

import hashlib
import json
from importlib.resources import files
from math import isfinite, prod
from pathlib import Path
from typing import Any, Iterable, Mapping

from .schemas_v2 import (
    BehavioralEntropyMetrics,
    DecisionClassification,
    EFGMDecisionInput,
    EFGMDecisionResult,
    FlowQualityMetricsV2,
    GroundingMetrics,
    InputEntropyMetrics,
    MetricObservation,
    OperationalEntropyMetrics,
    OutputEntropyMetrics,
)


DEFAULT_CONFIG_RESOURCE = "config/efgm-v2.0-baseline.json"


class IncompleteAssessmentError(ValueError):
    """Raised when an EFGM score would require silently guessing an unknown value."""


class ProvenanceError(ValueError):
    """Raised when research-grade provenance requirements are not satisfied."""


EXPECTED_WEIGHT_KEYS = {
    "input_entropy": set(InputEntropyMetrics.model_fields),
    "output_entropy": set(OutputEntropyMetrics.model_fields),
    "flow_quality": set(FlowQualityMetricsV2.model_fields),
    "grounding": set(GroundingMetrics.model_fields),
    "behavioral_entropy": set(BehavioralEntropyMetrics.model_fields),
    "operational_entropy": set(OperationalEntropyMetrics.model_fields),
}

EXPECTED_CLASSIFICATION_KEYS = {
    "critical_grounding_threshold",
    "coherent_dq_threshold",
    "coherent_grounding_threshold",
    "coherent_max_output_entropy",
    "weakly_grounded_dq_threshold",
    "weakly_grounded_grounding_threshold",
    "stable_dq_threshold",
    "degraded_dq_threshold",
    "high_entropy_dq_threshold",
}

EXPECTED_DRIVER_KEYS = {"low_score", "high_score"}


def canonical_sha256(value: Any) -> str:
    """Hash JSON-compatible content using a stable canonical representation."""
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        default=str,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _finite_number(name: str, value: Any, *, minimum: float | None = None, maximum: float | None = None) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a finite number")
    numeric = float(value)
    if not isfinite(numeric):
        raise ValueError(f"{name} must be finite")
    if minimum is not None and numeric < minimum:
        raise ValueError(f"{name} must be >= {minimum}")
    if maximum is not None and numeric > maximum:
        raise ValueError(f"{name} must be <= {maximum}")
    return numeric


def _validate_scoring_config(loaded: Mapping[str, Any]) -> dict[str, Any]:
    config = dict(loaded)

    if not isinstance(config.get("config_id"), str) or not config["config_id"].strip():
        raise ValueError("Scoring configuration must define a non-empty config_id.")
    if config.get("schema_version") != 1:
        raise ValueError("Scoring configuration schema_version must be 1.")

    epsilon = _finite_number("epsilon", config.get("epsilon"), minimum=0.0)
    if epsilon <= 0:
        raise ValueError("epsilon must be greater than zero.")

    weights = config.get("weights")
    if not isinstance(weights, Mapping) or set(weights) != set(EXPECTED_WEIGHT_KEYS):
        raise ValueError("Scoring configuration has missing or unexpected weight sections.")

    for section, expected_metrics in EXPECTED_WEIGHT_KEYS.items():
        section_weights = weights.get(section)
        if not isinstance(section_weights, Mapping) or set(section_weights) != expected_metrics:
            raise ValueError(f"Weights for {section} have missing or unexpected metric names.")
        numeric_weights = [
            _finite_number(f"weights.{section}.{name}", value, minimum=0.0)
            for name, value in section_weights.items()
        ]
        total = sum(numeric_weights)
        if total <= 0:
            raise ValueError(f"Weights for {section} must sum to a positive value.")
        if abs(total - 1.0) > 1e-9:
            raise ValueError(f"Weights for {section} must sum to 1.0; got {total}.")

    driver_thresholds = config.get("driver_thresholds")
    if not isinstance(driver_thresholds, Mapping) or set(driver_thresholds) != EXPECTED_DRIVER_KEYS:
        raise ValueError("driver_thresholds must define exactly low_score and high_score.")
    for name, value in driver_thresholds.items():
        _finite_number(f"driver_thresholds.{name}", value, minimum=0.0, maximum=1.0)

    classification = config.get("classification")
    if not isinstance(classification, Mapping) or set(classification) != EXPECTED_CLASSIFICATION_KEYS:
        raise ValueError("classification has missing or unexpected threshold names.")
    thresholds = {
        name: _finite_number(f"classification.{name}", value, minimum=0.0, maximum=1.0)
        for name, value in classification.items()
    }

    ordered_dq = [
        thresholds["coherent_dq_threshold"],
        thresholds["weakly_grounded_dq_threshold"],
        thresholds["stable_dq_threshold"],
        thresholds["degraded_dq_threshold"],
        thresholds["high_entropy_dq_threshold"],
    ]
    if ordered_dq != sorted(ordered_dq, reverse=True):
        raise ValueError("DQ classification thresholds must be monotonically non-increasing.")
    if thresholds["coherent_grounding_threshold"] < thresholds["critical_grounding_threshold"]:
        raise ValueError("coherent_grounding_threshold cannot be below critical_grounding_threshold.")
    if thresholds["weakly_grounded_grounding_threshold"] < thresholds["critical_grounding_threshold"]:
        raise ValueError("weakly_grounded_grounding_threshold cannot be below critical_grounding_threshold.")

    return config


def load_scoring_config(config: str | Path | Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Load and strictly validate a versioned v2 scoring configuration."""
    if config is None:
        text = files("efgm").joinpath(DEFAULT_CONFIG_RESOURCE).read_text(encoding="utf-8")
        loaded = json.loads(text)
    elif isinstance(config, Mapping):
        loaded = dict(config)
    else:
        loaded = json.loads(Path(config).read_text(encoding="utf-8"))
    return _validate_scoring_config(loaded)


def _metric_items(metrics: Any) -> Iterable[tuple[str, MetricObservation]]:
    for name in metrics.__class__.model_fields:
        yield name, getattr(metrics, name)


def _observation_value(observation: MetricObservation, path: str) -> float:
    if observation.status == "unknown":
        raise IncompleteAssessmentError(f"{path} is unknown; scoring cannot assume a favorable value.")
    if observation.status == "not_applicable":
        raise IncompleteAssessmentError(f"{path} is not_applicable but is required by the baseline formula.")
    assert observation.value is not None
    return observation.value


def weighted_score(
    metrics: Any,
    weights: Mapping[str, float],
    *,
    family_name: str = "metric family",
    allow_all_not_applicable: bool = False,
) -> float:
    """Score applicable observations, renormalizing weights around explicit N/A values.

    Unknown observations are never treated as zero. They block scoring until evidence is
    supplied. Explicit `not_applicable` values are excluded and remaining weights are
    renormalized. A whole entropy family may be explicitly N/A only when the caller
    opts into `allow_all_not_applicable`.
    """
    active: list[tuple[float, float]] = []
    for name, weight in weights.items():
        observation = getattr(metrics, name)
        if observation.status == "unknown":
            raise IncompleteAssessmentError(
                f"{family_name}.{name} is unknown; scoring cannot assume zero/no entropy."
            )
        if observation.status == "not_applicable":
            continue
        assert observation.value is not None
        active.append((observation.value, float(weight)))

    if not active:
        if allow_all_not_applicable:
            return 0.0
        raise IncompleteAssessmentError(f"All observations in {family_name} are not_applicable.")

    total_weight = sum(weight for _, weight in active)
    if total_weight <= 0:
        raise ValueError(f"Applicable weights for {family_name} must sum to a positive value.")
    score = sum(value * weight for value, weight in active) / total_weight
    return round(score, 4)


def low_score_drivers(metrics: Any, threshold: float = 0.60) -> list[str]:
    return [
        name
        for name, observation in _metric_items(metrics)
        if observation.status in {"observed", "inferred"}
        and observation.value is not None
        and observation.value < threshold
    ]


def high_score_drivers(metrics: Any, threshold: float = 0.35) -> list[str]:
    return [
        name
        for name, observation in _metric_items(metrics)
        if observation.status in {"observed", "inferred"}
        and observation.value is not None
        and observation.value >= threshold
    ]


def geometric_mean(values: list[float]) -> float:
    if not values:
        raise ValueError("At least one value is required for geometric mean.")
    if any(value < 0 for value in values):
        raise ValueError("Geometric mean values must be non-negative.")
    return prod(values) ** (1 / len(values))


def iter_observations(input_data: EFGMDecisionInput) -> Iterable[tuple[str, MetricObservation]]:
    yield "T", input_data.T
    yield "C", input_data.C
    yield "uncertainty_calibration", input_data.uncertainty_calibration
    families = {
        "flow_quality": input_data.flow_quality,
        "input_entropy": input_data.input_entropy,
        "output_entropy": input_data.output_entropy,
        "grounding": input_data.grounding,
        "behavioral_entropy": input_data.behavioral_entropy,
        "operational_entropy": input_data.operational_entropy,
    }
    for family_name, metrics in families.items():
        for name, observation in _metric_items(metrics):
            yield f"{family_name}.{name}", observation
    if input_data.outcome_quality is not None:
        yield "outcome_quality", input_data.outcome_quality


def research_provenance_issues(input_data: EFGMDecisionInput) -> list[str]:
    """Return issues that prevent an assessment from being research-grade/auditable."""
    issues: list[str] = []
    for path, observation in iter_observations(input_data):
        if observation.status == "unknown":
            issues.append(f"{path}: unknown observation")
            continue
        if not observation.rationale.strip():
            issues.append(f"{path}: missing rationale")
        if not observation.scorer_id:
            issues.append(f"{path}: missing scorer_id")
        if not observation.scorer_type:
            issues.append(f"{path}: missing scorer_type")
        if observation.status in {"observed", "inferred"}:
            if not observation.evidence_refs:
                issues.append(f"{path}: missing evidence_refs")
            if observation.confidence <= 0:
                issues.append(f"{path}: confidence must be > 0 for an applied value")
        elif observation.status == "not_applicable":
            if not observation.evidence_refs:
                issues.append(f"{path}: missing evidence_refs for not_applicable claim")
            if observation.confidence <= 0:
                issues.append(f"{path}: confidence must be > 0 for a not_applicable claim")
    return issues


def classify_decision(
    decision_quality: float,
    grounding: float,
    output_entropy: float,
    thresholds: Mapping[str, float],
) -> DecisionClassification:
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
    *,
    require_provenance: bool = False,
) -> EFGMDecisionResult:
    scoring_config = load_scoring_config(config)
    weights = scoring_config["weights"]

    provenance_issues = research_provenance_issues(input_data)
    if require_provenance and provenance_issues:
        raise ProvenanceError("Research-grade provenance validation failed: " + "; ".join(provenance_issues))

    Ei = weighted_score(input_data.input_entropy, weights["input_entropy"], family_name="input_entropy")
    Eo = weighted_score(input_data.output_entropy, weights["output_entropy"], family_name="output_entropy")
    Fq = weighted_score(input_data.flow_quality, weights["flow_quality"], family_name="flow_quality")
    G = weighted_score(input_data.grounding, weights["grounding"], family_name="grounding")
    Be = weighted_score(
        input_data.behavioral_entropy,
        weights["behavioral_entropy"],
        family_name="behavioral_entropy",
        allow_all_not_applicable=True,
    )
    Oe = weighted_score(
        input_data.operational_entropy,
        weights["operational_entropy"],
        family_name="operational_entropy",
        allow_all_not_applicable=True,
    )
    H = _observation_value(input_data.input_entropy.hidden_information_load, "input_entropy.hidden_information_load")
    U = _observation_value(input_data.uncertainty_calibration, "uncertainty_calibration")
    T = _observation_value(input_data.T, "T")
    C = _observation_value(input_data.C, "C")

    epsilon = float(scoring_config["epsilon"])
    CRC = round((Ei - Eo) / max(Ei, epsilon), 4)

    Q = round(geometric_mean([T, C, Fq, G, U]), 4)
    DQ = round(Q / (1 + Eo + Be + Oe), 4)
    outcome_confidence = round(DQ * (1 - H), 4)

    OQ = None
    if input_data.outcome_quality is not None and input_data.outcome_quality.status in {"observed", "inferred"}:
        assert input_data.outcome_quality.value is not None
        OQ = input_data.outcome_quality.value
    OD = round(OQ - DQ, 4) if OQ is not None else None

    classification = classify_decision(DQ, G, Eo, scoring_config["classification"])
    driver_thresholds = scoring_config["driver_thresholds"]
    input_dump = input_data.model_dump(mode="json", exclude_none=False)

    return EFGMDecisionResult(
        task_id=input_data.task_id,
        config_id=scoring_config["config_id"],
        config_sha256=canonical_sha256(scoring_config),
        input_sha256=canonical_sha256(input_dump),
        provenance_complete=not provenance_issues,
        provenance_issues=provenance_issues,
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