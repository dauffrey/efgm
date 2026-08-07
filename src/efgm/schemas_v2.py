from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator


DecisionClassification = Literal[
    "Coherent and grounded",
    "Coherent but weakly grounded",
    "Weakly grounded - verification required",
    "Stable with watch items",
    "Degraded but usable",
    "High entropy",
    "Misaligned",
]

ObservationStatus = Literal["observed", "inferred", "unknown", "not_applicable"]
ScorerType = Literal["human", "model", "automated", "hybrid"]


class MetricObservation(BaseModel):
    """Auditable observation supporting one normalized EFGM metric value.

    `unknown` and `not_applicable` are intentionally distinct from a measured value of
    zero. Unknown/N/A observations therefore carry no numeric value and cannot be
    silently interpreted as favorable evidence by the scorer.
    """

    value: float | None = Field(default=None, ge=0, le=1)
    status: ObservationStatus = "inferred"
    rationale: str = ""
    evidence_refs: list[str] = Field(default_factory=list)
    scorer_id: str | None = None
    scorer_type: ScorerType | None = None
    confidence: float = Field(ge=0, le=1, default=0.50)
    recorded_at: datetime | None = None

    @model_validator(mode="after")
    def validate_status_value_pair(self):
        if self.status in {"observed", "inferred"} and self.value is None:
            raise ValueError(f"status={self.status!r} requires a numeric value")
        if self.status in {"unknown", "not_applicable"} and self.value is not None:
            raise ValueError(f"status={self.status!r} must not carry a numeric value")
        return self


def unknown_observation() -> MetricObservation:
    return MetricObservation(
        value=None,
        status="unknown",
        rationale="No observation supplied.",
        confidence=0.0,
    )


def _coerce_observation(value):
    """Preserve v0.2 numeric-input compatibility while making provenance explicit."""
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return {
            "value": float(value),
            "status": "inferred",
            "rationale": "Legacy numeric input; provenance was not supplied.",
            "confidence": 0.50,
        }
    return value


class _ObservationSet(BaseModel):
    @field_validator("*", mode="before")
    @classmethod
    def coerce_numeric_observations(cls, value):
        return _coerce_observation(value)


class InputEntropyMetrics(_ObservationSet):
    input_contradiction: MetricObservation = Field(default_factory=unknown_observation)
    input_ambiguity: MetricObservation = Field(default_factory=unknown_observation)
    input_goal_conflict: MetricObservation = Field(default_factory=unknown_observation)
    missing_context: MetricObservation = Field(default_factory=unknown_observation)
    hidden_information_load: MetricObservation = Field(default_factory=unknown_observation)


class OutputEntropyMetrics(_ObservationSet):
    output_contradiction: MetricObservation = Field(default_factory=unknown_observation)
    uncertainty_mismatch: MetricObservation = Field(default_factory=unknown_observation)
    goal_drift: MetricObservation = Field(default_factory=unknown_observation)
    reasoning_instability: MetricObservation = Field(default_factory=unknown_observation)
    context_decay: MetricObservation = Field(default_factory=unknown_observation)


class FlowQualityMetricsV2(_ObservationSet):
    task_completion_consistency: MetricObservation = Field(default_factory=unknown_observation)
    reasoning_continuity: MetricObservation = Field(default_factory=unknown_observation)
    semantic_coherence: MetricObservation = Field(default_factory=unknown_observation)
    verification_success_rate: MetricObservation = Field(default_factory=unknown_observation)


class GroundingMetrics(_ObservationSet):
    rule_support: MetricObservation = Field(default_factory=unknown_observation)
    evidence_validity: MetricObservation = Field(default_factory=unknown_observation)
    traceability: MetricObservation = Field(default_factory=unknown_observation)
    factual_consistency: MetricObservation = Field(default_factory=unknown_observation)
    domain_calibration: MetricObservation = Field(default_factory=unknown_observation)


class BehavioralEntropyMetrics(_ObservationSet):
    chasing_behavior: MetricObservation = Field(default_factory=unknown_observation)
    outcome_bias: MetricObservation = Field(default_factory=unknown_observation)
    sunk_cost_pressure: MetricObservation = Field(default_factory=unknown_observation)
    false_pattern_detection: MetricObservation = Field(default_factory=unknown_observation)
    overconfidence_feedback: MetricObservation = Field(default_factory=unknown_observation)


class OperationalEntropyMetrics(_ObservationSet):
    timeout_rate: MetricObservation = Field(default_factory=unknown_observation)
    retry_instability: MetricObservation = Field(default_factory=unknown_observation)
    tool_failure_rate: MetricObservation = Field(default_factory=unknown_observation)
    latency_pressure: MetricObservation = Field(default_factory=unknown_observation)
    workflow_interruption: MetricObservation = Field(default_factory=unknown_observation)


class EFGMDecisionInput(BaseModel):
    task_id: str
    T: MetricObservation
    C: MetricObservation
    flow_quality: FlowQualityMetricsV2
    input_entropy: InputEntropyMetrics
    output_entropy: OutputEntropyMetrics
    grounding: GroundingMetrics
    uncertainty_calibration: MetricObservation
    behavioral_entropy: BehavioralEntropyMetrics = Field(default_factory=BehavioralEntropyMetrics)
    operational_entropy: OperationalEntropyMetrics = Field(default_factory=OperationalEntropyMetrics)
    outcome_quality: MetricObservation | None = None
    notes: list[str] = Field(default_factory=list)

    @field_validator("T", "C", "uncertainty_calibration", "outcome_quality", mode="before")
    @classmethod
    def coerce_scalar_observations(cls, value):
        if value is None:
            return None
        return _coerce_observation(value)


class EFGMDecisionResult(BaseModel):
    task_id: str
    config_id: str
    config_sha256: str
    input_sha256: str
    provenance_complete: bool
    provenance_issues: list[str]
    T: float
    C: float
    Fq: float
    G: float
    U: float
    Ei: float
    Eo: float
    Be: float
    Oe: float
    H: float
    CRC: float
    Q: float
    DQ: float
    outcome_confidence: float
    OQ: float | None
    OD: float | None
    classification: DecisionClassification
    recommended_action: str
    input_entropy_drivers: list[str]
    output_entropy_drivers: list[str]
    grounding_drivers: list[str]
    behavioral_entropy_drivers: list[str]
    operational_entropy_drivers: list[str]
