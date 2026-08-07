from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator


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
    """Auditable observation supporting one normalized EFGM metric value."""

    value: float = Field(ge=0, le=1)
    status: ObservationStatus = "inferred"
    rationale: str = ""
    evidence_refs: list[str] = Field(default_factory=list)
    scorer_id: str | None = None
    scorer_type: ScorerType | None = None
    confidence: float = Field(ge=0, le=1, default=0.50)
    recorded_at: datetime | None = None


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
    input_contradiction: MetricObservation = Field(default_factory=lambda: MetricObservation(value=0))
    input_ambiguity: MetricObservation = Field(default_factory=lambda: MetricObservation(value=0))
    input_goal_conflict: MetricObservation = Field(default_factory=lambda: MetricObservation(value=0))
    missing_context: MetricObservation = Field(default_factory=lambda: MetricObservation(value=0))
    hidden_information_load: MetricObservation = Field(default_factory=lambda: MetricObservation(value=0))


class OutputEntropyMetrics(_ObservationSet):
    output_contradiction: MetricObservation = Field(default_factory=lambda: MetricObservation(value=0))
    uncertainty_mismatch: MetricObservation = Field(default_factory=lambda: MetricObservation(value=0))
    goal_drift: MetricObservation = Field(default_factory=lambda: MetricObservation(value=0))
    reasoning_instability: MetricObservation = Field(default_factory=lambda: MetricObservation(value=0))
    context_decay: MetricObservation = Field(default_factory=lambda: MetricObservation(value=0))


class FlowQualityMetricsV2(_ObservationSet):
    task_completion_consistency: MetricObservation = Field(default_factory=lambda: MetricObservation(value=0))
    reasoning_continuity: MetricObservation = Field(default_factory=lambda: MetricObservation(value=0))
    semantic_coherence: MetricObservation = Field(default_factory=lambda: MetricObservation(value=0))
    verification_success_rate: MetricObservation = Field(default_factory=lambda: MetricObservation(value=0))


class GroundingMetrics(_ObservationSet):
    rule_support: MetricObservation = Field(default_factory=lambda: MetricObservation(value=0))
    evidence_validity: MetricObservation = Field(default_factory=lambda: MetricObservation(value=0))
    traceability: MetricObservation = Field(default_factory=lambda: MetricObservation(value=0))
    factual_consistency: MetricObservation = Field(default_factory=lambda: MetricObservation(value=0))
    domain_calibration: MetricObservation = Field(default_factory=lambda: MetricObservation(value=0))


class BehavioralEntropyMetrics(_ObservationSet):
    chasing_behavior: MetricObservation = Field(default_factory=lambda: MetricObservation(value=0))
    outcome_bias: MetricObservation = Field(default_factory=lambda: MetricObservation(value=0))
    sunk_cost_pressure: MetricObservation = Field(default_factory=lambda: MetricObservation(value=0))
    false_pattern_detection: MetricObservation = Field(default_factory=lambda: MetricObservation(value=0))
    overconfidence_feedback: MetricObservation = Field(default_factory=lambda: MetricObservation(value=0))


class OperationalEntropyMetrics(_ObservationSet):
    timeout_rate: MetricObservation = Field(default_factory=lambda: MetricObservation(value=0))
    retry_instability: MetricObservation = Field(default_factory=lambda: MetricObservation(value=0))
    tool_failure_rate: MetricObservation = Field(default_factory=lambda: MetricObservation(value=0))
    latency_pressure: MetricObservation = Field(default_factory=lambda: MetricObservation(value=0))
    workflow_interruption: MetricObservation = Field(default_factory=lambda: MetricObservation(value=0))


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
