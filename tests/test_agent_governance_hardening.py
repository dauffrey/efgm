from __future__ import annotations

from copy import deepcopy
from typing import get_args

import pytest

from efgm.benchmark_v0_2 import generate_cases
from efgm.experiment_runner_v0_2 import (
    MODEL_DIRECTIONS,
    case_to_v3_input,
    run_experiment,
)
from efgm.schemas_v3 import AgentGovernanceClassification, EFGMAgentGovernanceInput
from efgm.scoring_v3 import (
    classify_agent_state,
    load_agent_governance_config,
    score_agent_governance,
)
from efgm.temporal_v0_3 import (
    EFGMAgentState,
    ResidualStateAssessment,
    score_state_transition,
)


SEQUENCE_ID = "test-agent-sequence"
SUBJECT_ID = "test-governed-agent"


def _case(pair_id: str, preferred: bool):
    return next(
        case
        for case in generate_cases()
        if case["pair_id"] == pair_id and case["preferred"] is preferred
    )


def _identity_kwargs() -> dict:
    return {
        "governed_subject_id": SUBJECT_ID,
        "identity_evidence_refs": ["test://identity/test-governed-agent"],
        "identity_scorer_id": "test-reviewer",
        "identity_scorer_type": "human",
        "identity_confidence": 0.95,
    }


def _clear_residual_state(**overrides) -> ResidualStateAssessment:
    fields = {
        "credentials": "clear",
        "persistence": "clear",
        "environmental_memory": "clear",
        "coordination": "clear",
        "privileges": "clear",
        "scheduled_actions": "clear",
        "irreversible_side_effects": "not_applicable",
        "rollback_gaps": "clear",
    }
    fields.update(overrides)
    return ResidualStateAssessment.model_validate(
        {
            name: {
                "status": status,
                "rationale": f"Synthetic residual-state assessment for {name}: {status}.",
                "evidence_refs": (
                    []
                    if status == "unknown"
                    else [f"test://residual/{name}/{status}"]
                ),
                "scorer_id": "test-reviewer",
                "scorer_type": "human",
                "confidence": 0.9,
            }
            for name, status in fields.items()
        }
    )


def _state(*, state_id: str, phase: str, case, **kwargs) -> EFGMAgentState:
    identity = _identity_kwargs()
    identity.update(
        {
            key: kwargs.pop(key)
            for key in list(kwargs)
            if key in identity
        }
    )
    return EFGMAgentState(
        sequence_id=kwargs.pop("sequence_id", SEQUENCE_ID),
        state_id=state_id,
        phase=phase,
        assessment=case_to_v3_input(case),
        **identity,
        **kwargs,
    )


def test_agent_config_is_versioned_hashed_and_input_identified():
    case = generate_cases()[0]
    result = score_agent_governance(case_to_v3_input(case), require_provenance=True)
    config = load_agent_governance_config()

    assert result.agent_config_id == config["config_id"]
    assert len(result.agent_config_sha256) == 64
    assert len(result.input_sha256) == 64


def test_invalid_candidate_threshold_relationship_is_rejected():
    config = deepcopy(load_agent_governance_config())
    config["classification"]["elevated_agency_exposure_threshold"] = 0.20
    config["classification"]["elevated_coherent_unsafe_execution_threshold"] = 0.30

    with pytest.raises(ValueError, match="CUE cannot exceed AE"):
        load_agent_governance_config(config)


def test_insufficient_evidence_is_not_a_reachable_classification_label():
    assert "Insufficient evidence" not in get_args(AgentGovernanceClassification)


def test_classification_is_monotonic_across_governance_boundaries():
    thresholds = load_agent_governance_config()["classification"]

    labels = [
        classify_agent_state(0.80, gi, 0.10, 0.08, thresholds)
        for gi in (0.59, 0.60, 0.61, 0.74, 0.75, 0.76)
    ]

    assert labels[:4] == ["High-flow governance deficit"] * 4
    assert labels[4:] == ["Governed autonomous operation"] * 2


def test_low_flow_deficit_is_explicit_instead_of_falling_into_elevated_risk():
    thresholds = load_agent_governance_config()["classification"]
    assert (
        classify_agent_state(0.40, 0.65, 0.10, 0.04, thresholds)
        == "Low-flow governance deficit"
    )


def test_all_na_coordination_family_is_excluded_and_coverage_is_visible():
    case = generate_cases()[0]
    payload = case_to_v3_input(case).model_dump(mode="json")
    for name in payload["coordination_governance"]:
        payload["coordination_governance"][name] = {
            "value": None,
            "status": "not_applicable",
            "rationale": "Strictly single-agent scenario; no peer/delegation surface applies.",
            "evidence_refs": [f"test://scope/coordination/{name}"],
            "scorer_id": "test-reviewer",
            "scorer_type": "human",
            "confidence": 0.9,
            "recorded_at": None,
        }

    assessment = EFGMAgentGovernanceInput.model_validate(payload)
    result = score_agent_governance(assessment, require_provenance=True)

    assert result.coordination_governance is None
    assert result.governance_family_count == 5
    assert "coordination_governance" in result.excluded_governance_families
    assert "coordination_governance" not in result.applicable_governance_families
    assert 0.0 <= result.governance_integrity <= 1.0


def test_observation_floor_does_not_turn_every_low_metric_into_a_prerequisite():
    case = generate_cases()[0]
    payload = case_to_v3_input(case).model_dump(mode="json")
    observation = payload["observability"]["action_trace_coverage"]
    observation["value"] = 0.0
    observation["rationale"] = "Synthetic low non-prerequisite observability metric."
    observation["evidence_refs"] = ["test://low-observability"]

    result = score_agent_governance(
        EFGMAgentGovernanceInput.model_validate(payload),
        require_provenance=True,
    )

    assert result.governance_observation_floor == 0.0
    assert "observability.action_trace_coverage" not in result.candidate_prerequisite_breaches
    assert "candidate_governance_prerequisite_breach" not in result.diagnostic_flags


def test_configured_candidate_prerequisite_breach_is_explicit():
    case = generate_cases()[0]
    payload = case_to_v3_input(case).model_dump(mode="json")
    observation = payload["boundary_integrity"]["trust_boundary_adherence"]
    observation["value"] = 0.0
    observation["rationale"] = "Synthetic trust-boundary collapse."
    observation["evidence_refs"] = ["test://candidate-prerequisite-collapse"]

    result = score_agent_governance(
        EFGMAgentGovernanceInput.model_validate(payload),
        require_provenance=True,
    )

    assert result.governance_observation_floor == 0.0
    assert "boundary_integrity.trust_boundary_adherence" in result.candidate_prerequisite_paths
    assert "boundary_integrity.trust_boundary_adherence" in result.candidate_prerequisite_breaches
    assert "candidate_governance_prerequisite_breach" in result.diagnostic_flags


def test_agency_exposure_is_separate_from_coherent_unsafe_execution():
    case = _case("coherent_unsafe_execution-04", preferred=False)
    result = score_agent_governance(case_to_v3_input(case), require_provenance=True)

    assert result.agency_exposure >= result.coherent_unsafe_execution
    assert result.uncontrolled_agency_risk == result.coherent_unsafe_execution
    assert result.coherent_unsafe_execution == round(
        result.task_flow * result.agency_exposure,
        4,
    )


def test_lower_task_flow_reduces_cue_without_reducing_agency_exposure():
    case = _case("coherent_unsafe_execution-04", preferred=False)
    baseline_input = case_to_v3_input(case)
    baseline = score_agent_governance(baseline_input, require_provenance=True)

    payload = baseline_input.model_dump(mode="json")
    payload["decision"]["T"]["value"] = 0.10
    payload["decision"]["T"]["rationale"] = (
        "Synthetic low-observation-maturity mutation; governance and agency are held constant."
    )
    payload["decision"]["T"]["evidence_refs"] = ["test://low-task-flow-mutation"]
    lower_flow_input = EFGMAgentGovernanceInput.model_validate(payload)
    lower_flow = score_agent_governance(lower_flow_input, require_provenance=True)

    assert lower_flow.task_flow < baseline.task_flow
    assert lower_flow.agency_exposure == baseline.agency_exposure
    assert lower_flow.coherent_unsafe_execution < baseline.coherent_unsafe_execution


def test_agent_benchmark_records_config_identity_and_risk_directions():
    pair = "coherent_unsafe_execution-04"
    cases = [_case(pair, True), _case(pair, False)]
    result = run_experiment(cases=cases, sensitivity_trials=1, code_sha="test-code-sha")

    assert len(result["candidate_config_sha256"]) == 64
    assert result["code_sha"] == "test-code-sha"
    assert MODEL_DIRECTIONS["agency_exposure"] == "lower"
    assert MODEL_DIRECTIONS["coherent_unsafe_execution"] == "lower"
    assert result["results"]["all"]["agency_exposure"]["direction"] == "lower"
    assert result["results"]["all"]["coherent_unsafe_execution"]["direction"] == "lower"
    assert result["results"]["validation"]["agency_exposure"]["pairs"] == 0
    assert result["results"]["validation"]["agency_exposure"]["strict_win_rate"] is None


def test_transition_rejects_unrelated_sequences():
    degraded = _case("coherent_unsafe_execution-04", preferred=False)
    governed = _case("coherent_unsafe_execution-04", preferred=True)

    before = _state(state_id="s1", phase="pre_intervention", case=degraded)
    after = _state(
        state_id="s2",
        phase="post_intervention",
        case=governed,
        sequence_id="different-sequence",
        intervention="Synthetic intervention.",
        residual_state=_clear_residual_state(),
    )

    with pytest.raises(ValueError, match="same sequence_id"):
        score_state_transition(before, after, require_provenance=True)


def test_recovery_progress_requires_pre_to_post_intervention_phase():
    degraded = _case("coherent_unsafe_execution-04", preferred=False)
    governed = _case("coherent_unsafe_execution-04", preferred=True)

    before = _state(state_id="s1", phase="pre_action", case=degraded)
    after = _state(
        state_id="s2",
        phase="post_intervention",
        case=governed,
        intervention="Synthetic intervention.",
        residual_state=_clear_residual_state(),
    )

    transition = score_state_transition(before, after, require_provenance=True)

    assert not transition.phase_transition_valid_for_recovery
    assert not transition.recovery_progress_signal
    assert not transition.verified_recovery_signal


def test_recovery_progress_is_not_verified_without_residual_state_evidence():
    degraded = _case("coherent_unsafe_execution-04", preferred=False)
    governed = _case("coherent_unsafe_execution-04", preferred=True)

    before = _state(state_id="s1-degraded", phase="pre_intervention", case=degraded)
    after = _state(
        state_id="s2-governed",
        phase="post_intervention",
        case=governed,
        intervention="Restore authorized governance state.",
    )

    transition = score_state_transition(before, after, require_provenance=True)

    assert transition.recovery_progress_signal
    assert not transition.residual_state_complete
    assert not transition.verified_recovery_signal


def test_not_applicable_residual_without_evidence_blocks_verified_recovery():
    degraded = _case("coherent_unsafe_execution-04", preferred=False)
    governed = _case("coherent_unsafe_execution-04", preferred=True)
    residual = _clear_residual_state().model_dump(mode="json")
    residual["irreversible_side_effects"]["evidence_refs"] = []

    before = _state(state_id="s1", phase="pre_intervention", case=degraded)
    after = _state(
        state_id="s2",
        phase="post_intervention",
        case=governed,
        intervention="Synthetic intervention.",
        residual_state=ResidualStateAssessment.model_validate(residual),
    )

    transition = score_state_transition(before, after, require_provenance=True)

    assert transition.recovery_progress_signal
    assert any("irreversible_side_effects: missing evidence_refs" in item for item in transition.residual_state_issues)
    assert not transition.verified_recovery_signal


def test_present_residual_state_blocks_verified_recovery():
    degraded = _case("coherent_unsafe_execution-04", preferred=False)
    governed = _case("coherent_unsafe_execution-04", preferred=True)

    before = _state(state_id="s1-degraded", phase="pre_intervention", case=degraded)
    after = _state(
        state_id="s2-governed",
        phase="post_intervention",
        case=governed,
        intervention="Revoke primary credential.",
        residual_state=_clear_residual_state(credentials="present"),
    )

    transition = score_state_transition(before, after, require_provenance=True)

    assert transition.recovery_progress_signal
    assert "credentials" in transition.residual_state_present
    assert not transition.verified_recovery_signal


def test_remaining_candidate_prerequisite_breach_blocks_verified_recovery():
    degraded = _case("coherent_unsafe_execution-04", preferred=False)
    governed_input = case_to_v3_input(_case("coherent_unsafe_execution-04", preferred=True))
    payload = governed_input.model_dump(mode="json")
    observation = payload["boundary_integrity"]["trust_boundary_adherence"]
    observation["value"] = 0.0
    observation["rationale"] = "Residual trust-boundary failure after intervention."
    observation["evidence_refs"] = ["test://residual-trust-boundary"]

    before = _state(state_id="s1-degraded", phase="pre_intervention", case=degraded)
    after = EFGMAgentState(
        sequence_id=SEQUENCE_ID,
        state_id="s2-partial",
        phase="post_intervention",
        intervention="Partial governance restoration.",
        residual_state=_clear_residual_state(),
        assessment=EFGMAgentGovernanceInput.model_validate(payload),
        **_identity_kwargs(),
    )

    transition = score_state_transition(before, after, require_provenance=True)

    assert transition.recovery_progress_signal
    assert "boundary_integrity.trust_boundary_adherence" in transition.candidate_prerequisite_breaches_after
    assert not transition.verified_recovery_signal


def test_governance_deficit_post_state_blocks_verified_recovery():
    degraded = _case("coherent_unsafe_execution-04", preferred=False)
    governed = _case("coherent_unsafe_execution-04", preferred=True)
    config = deepcopy(load_agent_governance_config())
    config["classification"]["governed_integrity_threshold"] = 0.99

    before = _state(state_id="s1", phase="pre_intervention", case=degraded)
    after = _state(
        state_id="s2",
        phase="post_intervention",
        case=governed,
        intervention="Synthetic intervention.",
        residual_state=_clear_residual_state(),
    )

    transition = score_state_transition(
        before,
        after,
        require_provenance=True,
        config=config,
    )

    assert transition.recovery_progress_signal
    assert not transition.post_state_governed
    assert not transition.verified_recovery_signal


def test_complete_residual_evidence_can_produce_verified_recovery_signal():
    degraded = _case("coherent_unsafe_execution-04", preferred=False)
    governed = _case("coherent_unsafe_execution-04", preferred=True)

    before = _state(state_id="s1-degraded", phase="pre_intervention", case=degraded)
    after = _state(
        state_id="s2-governed",
        phase="post_intervention",
        case=governed,
        intervention="Revoke out-of-scope capability and verify residual state.",
        residual_state=_clear_residual_state(),
    )

    transition = score_state_transition(before, after, require_provenance=True)

    assert transition.sequence_id == SEQUENCE_ID
    assert transition.identity_continuity_valid
    assert transition.governed_subject_id == SUBJECT_ID
    assert len(transition.agent_config_sha256) == 64
    assert len(transition.before_input_sha256) == 64
    assert len(transition.after_input_sha256) == 64
    assert transition.residual_state_sha256 is not None
    assert len(transition.residual_state_sha256) == 64
    assert transition.recovery_progress_signal
    assert transition.post_state_governed
    assert transition.residual_state_complete
    assert not transition.residual_state_present
    assert transition.verified_recovery_signal
