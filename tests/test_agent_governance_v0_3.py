from __future__ import annotations

import copy

import pytest

from efgm.benchmark_v0_2 import (
    EXPECTED_DATASET_SHA256,
    FAMILIES,
    dataset_sha256,
    generate_cases,
)
from efgm.experiment_runner_v0_2 import case_to_v3_input, run_experiment
from efgm.scoring_v2 import IncompleteAssessmentError
from efgm.scoring_v3 import score_agent_governance


def test_benchmark_v0_2_is_frozen_and_agent_focused():
    cases = generate_cases()
    assert len(cases) == 132
    assert len(FAMILIES) == 11
    assert dataset_sha256(cases) == EXPECTED_DATASET_SHA256
    assert EXPECTED_DATASET_SHA256 == "d7495d203f8a9e37ab777b4f4bbf4395f43a4f7ed3e306f684dff65b41f4ca5b"
    assert all(
        case["black_hat_role"] == "empirical_inspiration_only_not_incident_reconstruction"
        for case in cases
    )


def test_v2_task_flow_cannot_distinguish_governance_only_mutations():
    result = run_experiment(sensitivity_trials=1, perturbation=0.0)
    v2 = result["results"]["all"]["v2_task_flow"]
    assert v2["wins"] == 0
    assert v2["ties"] == 66
    assert v2["losses"] == 0


@pytest.mark.parametrize(
    "model_name",
    [
        "governed_product",
        "risk_adjusted_product",
        "governed_linear",
        "independent_governance_checklist",
    ],
)
def test_governance_candidates_respond_to_all_controlled_pairs(model_name):
    result = run_experiment(sensitivity_trials=1, perturbation=0.0)
    metrics = result["results"]["all"][model_name]
    assert metrics["wins"] == 66
    assert metrics["ties"] == 0
    assert metrics["losses"] == 0


def test_high_flow_can_coexist_with_governance_deficit():
    cases = generate_cases()
    preferred = next(
        case
        for case in cases
        if case["pair_id"] == "coherent_unsafe_execution-04" and case["preferred"]
    )
    mutated = next(
        case
        for case in cases
        if case["pair_id"] == "coherent_unsafe_execution-04" and not case["preferred"]
    )

    preferred_result = score_agent_governance(case_to_v3_input(preferred), require_provenance=True)
    mutated_result = score_agent_governance(case_to_v3_input(mutated), require_provenance=True)

    assert preferred_result.task_flow == mutated_result.task_flow
    assert mutated_result.governance_integrity < preferred_result.governance_integrity
    assert mutated_result.uncontrolled_agency_risk > preferred_result.uncontrolled_agency_risk


def test_unknown_governance_observation_never_defaults_to_safe():
    case = generate_cases()[0]
    payload = case_to_v3_input(case).model_dump(mode="json")
    payload["observability"]["action_trace_coverage"] = {
        "value": None,
        "status": "unknown",
        "rationale": "Trace coverage was not observed.",
        "evidence_refs": [],
        "scorer_id": "test",
        "scorer_type": "human",
        "confidence": 0.0,
        "recorded_at": None,
    }
    altered = case_to_v3_input(case).__class__.model_validate(payload)

    with pytest.raises(IncompleteAssessmentError):
        score_agent_governance(altered)
