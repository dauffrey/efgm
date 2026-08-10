from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator

from .schemas_v2 import EFGMDecisionInput, MetricObservation

AgentGovernanceClassification = Literal[
    "Governed autonomous operation",
    "Governed but low-flow",
    "High-flow governance deficit",
    "Low-flow governance deficit",
    "Elevated uncontrolled-agency risk",
]


def _coerce_observation(value):
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return {
            "value": float(value),
            "status": "inferred",
            "rationale": "Legacy numeric input; provenance was not supplied.",
            "confidence": 0.50,
        }
    return value


class _ObservationSetV3(BaseModel):
    @field_validator("*", mode="before")
    @classmethod
    def coerce_numeric_observations(cls, value):
        return _coerce_observation(value)


class AlignmentMetrics(_ObservationSetV3):
    objective_scope_fidelity: MetricObservation
    authority_precedence: MetricObservation
    goal_update_compliance: MetricObservation
    prohibited_goal_avoidance: MetricObservation


class BoundaryIntegrityMetrics(_ObservationSetV3):
    trust_boundary_adherence: MetricObservation
    privilege_boundary_adherence: MetricObservation
    capability_scope_adherence: MetricObservation
    credential_scope_adherence: MetricObservation


class ObservabilityMetrics(_ObservationSetV3):
    action_trace_coverage: MetricObservation
    tool_call_traceability: MetricObservation
    state_change_traceability: MetricObservation
    cross_agent_traceability: MetricObservation


class EnvironmentalMemoryGovernanceMetrics(_ObservationSetV3):
    persistence_scope_control: MetricObservation
    write_surface_inventory: MetricObservation
    readback_traceability: MetricObservation
    shared_state_control: MetricObservation


class CoordinationGovernanceMetrics(_ObservationSetV3):
    peer_discovery_control: MetricObservation
    delegation_scope_control: MetricObservation
    message_traceability: MetricObservation
    shared_goal_control: MetricObservation


class ControlRecoverabilityMetrics(_ObservationSetV3):
    revocation_effectiveness: MetricObservation
    containment_effectiveness: MetricObservation
    state_cleanup_completeness: MetricObservation
    rollback_effectiveness: MetricObservation


class AgencyAmplificationMetrics(_ObservationSetV3):
    privilege: MetricObservation
    connectivity: MetricObservation
    persistence: MetricObservation
    coordination: MetricObservation
    action_velocity: MetricObservation


class EFGMAgentGovernanceInput(BaseModel):
    task_id: str
    decision: EFGMDecisionInput
    alignment: AlignmentMetrics
    boundary_integrity: BoundaryIntegrityMetrics
    observability: ObservabilityMetrics
    environmental_memory_governance: EnvironmentalMemoryGovernanceMetrics
    coordination_governance: CoordinationGovernanceMetrics
    control_recoverability: ControlRecoverabilityMetrics
    agency_amplification: AgencyAmplificationMetrics
    notes: list[str] = Field(default_factory=list)


class EFGMAgentGovernanceResult(BaseModel):
    task_id: str
    agent_config_id: str
    agent_config_sha256: str
    input_sha256: str
    task_flow: float
    cognitive_entropy: float
    alignment: float
    boundary_integrity: float
    observability: float
    environmental_memory_governance: float
    coordination_governance: float | None
    control_recoverability: float
    agency_amplification: float
    applicable_governance_families: list[str]
    excluded_governance_families: list[str]
    governance_family_count: int
    governance_integrity: float
    governance_observation_floor: float
    governance_low_percentile: float
    candidate_prerequisite_threshold: float
    candidate_prerequisite_paths: list[str]
    candidate_prerequisite_breaches: list[str]
    diagnostic_flags: list[str]
    governed_flow_product: float
    agency_exposure: float
    coherent_unsafe_execution: float
    risk_adjusted_flow: float
    governed_linear_score: float
    uncontrolled_agency_risk: float
    classification: AgentGovernanceClassification
    provenance_complete: bool
    provenance_issues: list[str]
