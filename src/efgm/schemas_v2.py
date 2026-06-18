from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


DecisionClassification = Literal[
    "Coherent and grounded",
    "Coherent but weakly grounded",
    "Stable with watch items",
    "Degraded but usable",
    "High entropy",
    "Misaligned",
]


class InputEntropyMetrics(BaseModel):
    input_contradiction: float = Field(ge=0, le=1, default=0)
    input_ambiguity: float = Field(ge=0, le=1, default=0)
    input_goal_conflict: float = Field(ge=0, le=1, default=0)
    missing_context: float = Field(ge=0, le=1, default=0)
    hidden_information_load: float = Field(ge=0, le=1, default=0)


class OutputEntropyMetrics(BaseModel):
    output_contradiction: float = Field(ge=0, le=1, default=0)
    uncertainty_mismatch: float = Field(ge=0, le=1, default=0)
    goal_drift: float = Field(ge=0, le=1, default=0)
    reasoning_instability: float = Field(ge=0, le=1, default=0)
    context_decay: float = Field(ge=0, le=1, default=0)


class FlowQualityMetricsV2(BaseModel):
    task_completion_consistency: float = Field(ge=0, le=1, default=0)
    reasoning_continuity: float = Field(ge=0, le=1, default=0)
    semantic_coherence: float = Field(ge=0, le=1, default=0)
    verification_success_rate: float = Field(ge=0, le=1, default=0)


class GroundingMetrics(BaseModel):
    rule_support: float = Field(ge=0, le=1, default=0)
    evidence_validity: float = Field(ge=0, le=1, default=0)
    traceability: float = Field(ge=0, le=1, default=0)
    factual_consistency: float = Field(ge=0, le=1, default=0)
    domain_calibration: float = Field(ge=0, le=1, default=0)


class BehavioralEntropyMetrics(BaseModel):
    chasing_behavior: float = Field(ge=0, le=1, default=0)
    outcome_bias: float = Field(ge=0, le=1, default=0)
    sunk_cost_pressure: float = Field(ge=0, le=1, default=0)
    false_pattern_detection: float = Field(ge=0, le=1, default=0)
    overconfidence_feedback: float = Field(ge=0, le=1, default=0)


class OperationalEntropyMetrics(BaseModel):
    timeout_rate: float = Field(ge=0, le=1, default=0)
    retry_instability: float = Field(ge=0, le=1, default=0)
    tool_failure_rate: float = Field(ge=0, le=1, default=0)
    latency_pressure: float = Field(ge=0, le=1, default=0)
    workflow_interruption: float = Field(ge=0, le=1, default=0)


class EFGMDecisionInput(BaseModel):
    task_id: str
    T: float = Field(ge=0, le=1)
    C: float = Field(ge=0, le=1)
    flow_quality: FlowQualityMetricsV2
    input_entropy: InputEntropyMetrics
    output_entropy: OutputEntropyMetrics
    grounding: GroundingMetrics
    uncertainty_calibration: float = Field(ge=0, le=1)
    behavioral_entropy: BehavioralEntropyMetrics = Field(default_factory=BehavioralEntropyMetrics)
    operational_entropy: OperationalEntropyMetrics = Field(default_factory=OperationalEntropyMetrics)
    outcome_quality: float | None = Field(ge=0, le=1, default=None)
    notes: list[str] = Field(default_factory=list)


class EFGMDecisionResult(BaseModel):
    task_id: str
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
