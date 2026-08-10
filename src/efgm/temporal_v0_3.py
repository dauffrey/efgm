from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from .schemas_v3 import EFGMAgentGovernanceInput, EFGMAgentGovernanceResult
from .scoring_v3 import score_agent_governance


TemporalPhase = Literal[
    "pre_action",
    "post_action",
    "pre_intervention",
    "post_intervention",
    "follow_up",
]


class EFGMAgentState(BaseModel):
    """One evidence-backed agent-governance state in an experimental sequence."""

    state_id: str
    phase: TemporalPhase
    assessment: EFGMAgentGovernanceInput
    intervention: str | None = None
    notes: list[str] = Field(default_factory=list)


class EFGMStateTransitionResult(BaseModel):
    from_state_id: str
    to_state_id: str
    from_phase: TemporalPhase
    to_phase: TemporalPhase
    intervention: str | None
    governance_integrity_before: float
    governance_integrity_after: float
    delta_governance_integrity: float
    agency_exposure_before: float
    agency_exposure_after: float
    delta_agency_exposure: float
    coherent_unsafe_execution_before: float
    coherent_unsafe_execution_after: float
    delta_coherent_unsafe_execution: float
    governance_improved: bool
    exposure_reduced: bool
    coherent_unsafe_execution_reduced: bool
    recovery_signal: bool
    diagnostic_flags_before: list[str]
    diagnostic_flags_after: list[str]


class EFGMTemporalSequenceResult(BaseModel):
    state_results: list[EFGMAgentGovernanceResult]
    transitions: list[EFGMStateTransitionResult]


def score_state_transition(
    before: EFGMAgentState,
    after: EFGMAgentState,
    *,
    require_provenance: bool = False,
) -> EFGMStateTransitionResult:
    """Compare two v0.3 states without declaring a canonical temporal risk formula.

    `recovery_signal` is deliberately narrow: after a declared governance intervention,
    Governance Integrity must increase and Agency Exposure must decrease. It is an
    experimental signal, not proof that all residual state has been removed.
    """

    before_result = score_agent_governance(
        before.assessment,
        require_provenance=require_provenance,
    )
    after_result = score_agent_governance(
        after.assessment,
        require_provenance=require_provenance,
    )

    delta_gi = round(
        after_result.governance_integrity - before_result.governance_integrity,
        4,
    )
    delta_ae = round(after_result.agency_exposure - before_result.agency_exposure, 4)
    delta_cue = round(
        after_result.coherent_unsafe_execution - before_result.coherent_unsafe_execution,
        4,
    )

    governance_improved = delta_gi > 0
    exposure_reduced = delta_ae < 0
    cue_reduced = delta_cue < 0
    intervention = after.intervention
    recovery_signal = bool(
        after.phase == "post_intervention"
        and intervention
        and governance_improved
        and exposure_reduced
    )

    return EFGMStateTransitionResult(
        from_state_id=before.state_id,
        to_state_id=after.state_id,
        from_phase=before.phase,
        to_phase=after.phase,
        intervention=intervention,
        governance_integrity_before=before_result.governance_integrity,
        governance_integrity_after=after_result.governance_integrity,
        delta_governance_integrity=delta_gi,
        agency_exposure_before=before_result.agency_exposure,
        agency_exposure_after=after_result.agency_exposure,
        delta_agency_exposure=delta_ae,
        coherent_unsafe_execution_before=before_result.coherent_unsafe_execution,
        coherent_unsafe_execution_after=after_result.coherent_unsafe_execution,
        delta_coherent_unsafe_execution=delta_cue,
        governance_improved=governance_improved,
        exposure_reduced=exposure_reduced,
        coherent_unsafe_execution_reduced=cue_reduced,
        recovery_signal=recovery_signal,
        diagnostic_flags_before=before_result.diagnostic_flags,
        diagnostic_flags_after=after_result.diagnostic_flags,
    )


def score_temporal_sequence(
    states: list[EFGMAgentState],
    *,
    require_provenance: bool = False,
) -> EFGMTemporalSequenceResult:
    if not states:
        raise ValueError("At least one agent-governance state is required.")

    state_results = [
        score_agent_governance(
            state.assessment,
            require_provenance=require_provenance,
        )
        for state in states
    ]
    transitions = [
        score_state_transition(
            states[index],
            states[index + 1],
            require_provenance=require_provenance,
        )
        for index in range(len(states) - 1)
    ]
    return EFGMTemporalSequenceResult(
        state_results=state_results,
        transitions=transitions,
    )
