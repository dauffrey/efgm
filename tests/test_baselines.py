import pytest

from efgm.baselines import (
    checklist_baseline,
    grounding_calibration_baseline,
    independent_checklist_baseline,
    weighted_linear_baseline,
)
from efgm.schemas_v2 import EFGMDecisionInput


def payload() -> dict:
    return {
        "task_id": "baseline-test",
        "T": 0.9,
        "C": 0.9,
        "flow_quality": {
            "task_completion_consistency": 0.9,
            "reasoning_continuity": 0.9,
            "semantic_coherence": 0.9,
            "verification_success_rate": 0.9,
        },
        "input_entropy": {
            "input_contradiction": 0.0,
            "input_ambiguity": 0.0,
            "input_goal_conflict": 0.0,
            "missing_context": 0.0,
            "hidden_information_load": 0.0,
        },
        "output_entropy": {
            "output_contradiction": 0.0,
            "uncertainty_mismatch": 0.0,
            "goal_drift": 0.0,
            "reasoning_instability": 0.0,
            "context_decay": 0.0,
        },
        "grounding": {
            "rule_support": 0.9,
            "evidence_validity": 0.9,
            "traceability": 0.9,
            "factual_consistency": 0.9,
            "domain_calibration": 0.9,
        },
        "uncertainty_calibration": 0.9,
        "behavioral_entropy": {
            "chasing_behavior": 0.0,
            "outcome_bias": 0.0,
            "sunk_cost_pressure": 0.0,
            "false_pattern_detection": 0.0,
            "overconfidence_feedback": 0.0,
        },
        "operational_entropy": {
            "timeout_rate": 0.0,
            "retry_instability": 0.0,
            "tool_failure_rate": 0.0,
            "latency_pressure": 0.0,
            "workflow_interruption": 0.0,
        },
    }


def test_efgm_derived_baselines_are_normalized_and_high_for_clean_case():
    model_input = EFGMDecisionInput.model_validate(payload())

    scores = [
        checklist_baseline(model_input),
        grounding_calibration_baseline(model_input),
        weighted_linear_baseline(model_input),
    ]

    assert all(0 <= score <= 1 for score in scores)
    assert all(score >= 0.85 for score in scores)


def test_two_factor_ablation_drops_when_grounding_is_weak():
    weak = payload()
    weak["grounding"] = {name: 0.2 for name in weak["grounding"]}

    strong_score = grounding_calibration_baseline(EFGMDecisionInput.model_validate(payload()))
    weak_score = grounding_calibration_baseline(EFGMDecisionInput.model_validate(weak))

    assert weak_score < strong_score


def test_independent_checklist_does_not_require_efgm_input_or_weights():
    score = independent_checklist_baseline({
        "evidence_supported": True,
        "internally_consistent": True,
        "uncertainty_appropriate": 0.75,
        "scope_aligned": True,
        "execution_reliable": 0.50,
    })

    assert score == 0.85


def test_independent_checklist_rejects_missing_or_extra_criteria():
    with pytest.raises(ValueError, match="keys mismatch"):
        independent_checklist_baseline({"evidence_supported": True})
