from __future__ import annotations

from typing import get_args

from efgm.benchmark_v0_2 import generate_cases
from efgm.experiment_runner_v0_2 import case_to_v3_input
from efgm.schemas_v3 import AgentGovernanceClassification, EFGMAgentGovernanceInput
from efgm.scoring_v3 import load_agent_governance_config, score_agent_governance
from efgm.temporal_v0_3 import EFGMAgentState, score_state_transition


def _case(pair_id: str, preferred: bool):
    return next(
        case
        for case in generate_cases()
        if case["pair_id"] == pair_id and case["preferred"] is preferred
    )


def test_agent_config_is_versioned_and_hashed():
    case = generate_cases()[0]
    result = score_agent_governance(case_to_v3_input(case), require_provenance=True)
    config = load_agent_governance_config()

    assert result.agent_config_id == config["config_id"]
    assert len(result.agent_config_sha256) == 64


def test_insufficient_evidence_is_not_a_reachable_classification_label():
    assert "Insufficient evidence" not in get_args(AgentGovernanceClassification)


def test_all_na_coordination_family_is_excluded_from_gi():
    case = generate_cases()[0]
    payload = case_to_v3_input(case).model_dump(mode="json")
    for name in payload["coordination_governance"]:
        payload["coordination_governance"][name] = {
            "value": None,
            "status": "not_applicable",
            "rationale": "Strictly single-agent scenario; no peer/delegation surface applies.",
            "evidence_refs": [],
            "scorer_id": "test-reviewer",
            "scorer_type": "human",
            "confidence": 0.9,
            "recorded_at": None,
        }

    assessment = EFGMAgentGovernanceInput.model_validate(payload)
    result = score_agent_governance(assessment, require_provenance=True)

    assert result.coordination_governance is None
    assert 0.0 <= result.governance_integrity <= 1.0


def test_sparse_critical_failure_is_exposed_by_noncompensatory_diagnostic():
    case = generate_cases()[0]
    payload = case_to_v3_input(case).model_dump(mode="json")
    observation = payload["boundary_integrity"]["trust_boundary_adherence"]
    observation["value"] = 0.0
    observation["rationale"] = "Synthetic critical trust-boundary collapse."
    observation["evidence_refs"] = ["test://critical-boundary-collapse"]

    assessment = EFGMAgentGovernanceInput.model_validate(payload)
    result = score_agent_governance(assessment, require_provenance=True)

    assert result.governance_prerequisite_floor == 0.0
    assert "boundary_integrity.trust_boundary_adherence" in result.prerequisite_breaches
    assert "critical_governance_prerequisite_breach" in result.diagnostic_flags


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


def test_governance_intervention_transition_exposes_recovery_signal():
    degraded = _case("coherent_unsafe_execution-04", preferred=False)
    governed = _case("coherent_unsafe_execution-04", preferred=True)

    before = EFGMAgentState(
        state_id="s1-degraded",
        phase="pre_intervention",
        assessment=case_to_v3_input(degraded),
    )
    after = EFGMAgentState(
        state_id="s2-governed",
        phase="post_intervention",
        intervention="Revoke out-of-scope capability and restore authorized governance state.",
        assessment=case_to_v3_input(governed),
    )

    transition = score_state_transition(before, after, require_provenance=True)

    assert transition.governance_improved
    assert transition.exposure_reduced
    assert transition.recovery_signal
