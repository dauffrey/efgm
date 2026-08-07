from efgm.baselines import (
    checklist_baseline,
    grounding_calibration_baseline,
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
        "input_entropy": {},
        "output_entropy": {},
        "grounding": {
            "rule_support": 0.9,
            "evidence_validity": 0.9,
            "traceability": 0.9,
            "factual_consistency": 0.9,
            "domain_calibration": 0.9,
        },
        "uncertainty_calibration": 0.9,
    }


def test_simple_baselines_are_normalized_and_high_for_clean_case():
    model_input = EFGMDecisionInput.model_validate(payload())

    scores = [
        checklist_baseline(model_input),
        grounding_calibration_baseline(model_input),
        weighted_linear_baseline(model_input),
    ]

    assert all(0 <= score <= 1 for score in scores)
    assert all(score >= 0.85 for score in scores)


def test_two_factor_baseline_drops_when_grounding_is_weak():
    weak = payload()
    weak["grounding"] = {name: 0.2 for name in weak["grounding"]}

    strong_score = grounding_calibration_baseline(EFGMDecisionInput.model_validate(payload()))
    weak_score = grounding_calibration_baseline(EFGMDecisionInput.model_validate(weak))

    assert weak_score < strong_score
